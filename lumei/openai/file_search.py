import json
import re
from typing import Optional

from openai.types import FileObject
from openai.types.beta import Thread
from openai.types.beta.threads import Run

from lumei.openai.agent import Agent
from lumei.query_param import FileSearchQueryParam


def file_search(
        agent: Agent,
        input_file_path: str,
        file_search_query_params: list[FileSearchQueryParam]
) -> [Optional[dict[str, any]], Optional[str]]:
    vector_store_id: Optional[str] = None
    thread: Optional[Thread] = None
    run: Optional[Run] = None
    query = {}

    for param in file_search_query_params:
        query[param.name] = param.description

    try:
        file = agent.client.files.create(
            file=open(input_file_path, "rb"),
            purpose="assistants",
        )
    except Exception as e:
        return None, f"Failed to upload file: {input_file_path}. {e}"

    try:
        thread = agent.client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": json.dumps(query),
                    "attachments": [
                        {
                            "file_id": file.id,
                            "tools": [
                                {
                                    "type": "file_search"
                                }
                            ]
                        }
                    ],
                }
            ]
        )

        vector_store_id = thread.tool_resources.file_search.vector_store_ids[0]
    except Exception as e:
        clean_up_request(agent, file, vector_store_id)
        return None, f"Failed to create thread or vector store: {thread}. {e}"

    try:
        run = agent.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=agent.assistant_id,
            temperature=0,
        )
    except Exception as e:
        clean_up_request(agent, file, vector_store_id)
        return None, f"Failed to process request with thread: {run}. {e}"

    try:
        messages = list(agent.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        if not messages or not messages[0].content:
            return None, "Could not get message from OpenAI."

        message_content = messages[0].content[0].text.value
    except Exception as e:
        clean_up_request(agent, file, vector_store_id)
        return None, f"Failed to extract result text from thread. {e}"

    clean_up_request(agent, file, vector_store_id)

    formatted_result = format_result(message_content)

    if formatted_result:
        return formatted_result, None
    else:
        return None, f"Failed to extract data from response: {formatted_result}"


def format_result(result_text: str) -> Optional[dict[str, any]]:
    match = re.search(r'\{.*}', result_text, re.DOTALL)
    if match:
        result_json = match.group()
        try:
            return json.loads(result_json)
        except json.JSONDecodeError:
            return None
    return None


def clean_up_request(agent: Agent, file: Optional[FileObject], vector_store_id: Optional[str]):
    if file:
        try:
            agent.client.files.delete(
                file_id=file.id
            )
        except Exception as e:
            print(f"Failed to delete file: {file.id}. Error: {e}")

    if vector_store_id:
        try:
            agent.client.beta.vector_stores.delete(
                vector_store_id=vector_store_id
            )
        except Exception as e:
            print(f"Failed to delete vector store: {vector_store_id}. Error: {e}")
