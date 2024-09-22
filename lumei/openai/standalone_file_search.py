from typing import Optional

from lumei import create_agent, FileSearchQueryParam, file_search


class FileSearchException(Exception):
    pass


def openai_file_search(
        openai_api_key: str,
        input_file_path: str,
        file_search_query: dict[str, str]
) -> Optional[dict[str, str]]:
    agent, error = create_agent(
        openai_api_key=openai_api_key
    )

    if error:
        print(error)
        return None

    params = []

    for key, value in file_search_query.items():
        params.append(
            FileSearchQueryParam(
                name=key,
                description=value,
            )
        )

    result, error = file_search(
        agent=agent,
        input_file_path=input_file_path,
        file_search_query_params=params
    )

    if error:
        raise FileSearchException(f"File search query failed with error: {error}")

    return result
