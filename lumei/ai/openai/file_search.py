import json
import re
from typing import Optional

from openai.types import FileObject
from openai.types.beta import Thread
from openai.types.beta.threads import Run

from lumei.ai.openai.agent import Agent


def file_search(agent: Agent, file_path: str, query: [str, str]) -> [Optional[dict[str, str]], Optional[str]]:
    file: Optional[FileObject] = None
    vector_store_id: Optional[str] = None
    thread: Optional[Thread] = None
    run: Optional[Run] = None

    try:
        file = agent.client.files.create(
            file=open(file_path, "rb"),
            purpose="assistants",
        )
    except Exception as e:
        return None, f"Failed to upload file: {file_path}. {e}"

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
            assistant_id=agent.id,
            temperature=0,
        )
    except Exception as e:
        clean_up_request(agent, file, vector_store_id)
        return None, f"Failed to process request with thread: {run}. {e}"

    try:
        messages = list(agent.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
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


def format_result(result_text: str) -> Optional[dict[str, str]]:
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
            print(f"Failed to delete file: {file.id}. {e}")

    if vector_store_id:
        try:
            agent.client.beta.vector_stores.delete(
                vector_store_id=vector_store_id
            )
        except Exception as e:
            print(f"Failed to delete store: {vector_store_id}. {e}")
