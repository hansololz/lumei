from typing import Optional

from lumei import create_agent, FileSearchQueryParam, file_search
from lumei.openai.agent import default_model


class FileSearchException(Exception):
    pass


def openai_file_search(
        openai_api_key: str,
        input_files: list[str],
        file_search_query: dict[str, str],
        model: Optional[str] = default_model,
        assistant_id: Optional[str] = None,
) -> list[dict[str, str] | FileSearchException]:
    agent, error = creatasse_agent(
        openai_api_key=openai_api_key,
        model=model,
        assistant_id=assistant_id,
    )

    if error:
        raise FileSearchException(f"File search query failed with error: {error}")

    params = []

    for key, value in file_search_query.items():
        params.append(
            FileSearchQueryParam(
                name=key,
                description=value,
            )
        )

    results: list[dict[str, str] | FileSearchException] = []

    for input_file in input_files:
        result, error = file_search(
            agent=agent,
            input_file_path=input_file,
            file_search_query_params=params
        )

        if error:
            results.append(FileSearchException(f"File search query failed with error: {error}"))
        else:
            results.append(result)

    return results
