from typing import Optional

from openai import OpenAI


class Agent:
    def __init__(self, assistant_id: str, open_ai_client: OpenAI):
        self.id = assistant_id
        self.client = open_ai_client


default_instructions = """"
    You are a file search assistant.
    You are given a file and a list of data to extract from the data. For each data, the user will specify a name for the data and a description of what the data is. 
    The list of data to extract is in the form of a JSON object. The key is the name for the data and value is the description for the data.
    All the data that you should extract is in the file. If the data is not in the file, then do not return any information for that data. Do not hallucinate.
    All responses should be returned in the format of a proper JSON object. The keys for the JSON are the name for the data and the value is the extracted data. There should be no key in the response that is not found in the JSON object that holds the list of data to extract.
    Please and thank you.
"""

default_model = "gpt-4o"


def create_agent(
        openai_api_key: str,
        instructions: Optional[str] = default_instructions,
        model: Optional[str] = default_model,
        assistant_id: Optional[str] = None,
) -> [Optional[Agent], Optional[str]]:
    try:
        open_ai_client = OpenAI(
            api_key=openai_api_key
        )
    except Exception as e:
        return None, f"Failed to create OpenAI client: {e}"

    if not assistant_id:
        try:
            assistant = open_ai_client.beta.assistants.create(
                name="File Search",
                instructions=instructions,
                model=model,
                tools=[
                    {
                        "type": "file_search"
                    }
                ],
            )
            new_assistant_id = assistant.id
        except Exception as e:
            return None, f"Failed to create agent: {e}"
    else:
        new_assistant_id = assistant_id

    return Agent(
        assistant_id=new_assistant_id,
        open_ai_client=open_ai_client,
    ), None
