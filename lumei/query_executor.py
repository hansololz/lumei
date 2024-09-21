import ast
from typing import Optional

from lumei.file_manager import save_result, DataDescription, find_matched_files, setup_output_file, \
    check_if_can_create_file, create_data_description
from lumei.openai.agent import create_agent
from lumei.openai.file_search import file_search, FileSearchQueryParam
from lumei.query_param import parse_query_string


def execute_query_and_store_results(
        openai_api_key: str,
        input_files: str,
        output_file: str,
        file_search_query_string: str
) -> int:
    err = check_if_can_create_file(output_file)

    if err:
        print(err)
        return 1

    print("Verified permission to create file.")

    file_search_query, err = parse_query_string(file_search_query_string)

    if err:
        print(err)
        return 1

    query = []
    query_param_names: list[str] = []
    for query_param in file_search_query:
        query_param_names.append(query_param.name)
        query.append(
            FileSearchQueryParam(
                name=query_param.name,
                description=query_param.search,
            )
        )

    print("Parsed list of names and data descriptions for file search.")

    files, err = find_matched_files(input_files)

    if err:
        print(err)
        return 1

    print(f"Created list of files to process. Found {len(files)} files.")

    agent, err = create_agent(openai_api_key)

    if err:
        print(err)
        return 1

    print(f"Created agent with assistant id: {agent.assistant_id}.")

    print(f"Begun processing files.")

    results: [dict[str, str]] = []

    for file in files:
        result, error = file_search(agent, file, query)

        if result:
            print(f"    {file} SUCCESS")
            results.append(result)
        elif error:
            print(f"    {file} FAILED: {error}")
        else:
            print(f"    {file} FAILED")

    print(f"Finished processing files.")

    err = setup_output_file(output_file)

    if err:
        print(err)
        return 1

    print(f"Created output file: {output_file}.")

    err = save_result(output_file, query_param_names, results)

    if err:
        print(err)
        return 1

    print(f"Wrote result to file: {output_file}.")

    return 0


def convert_file_search_query_to_objects(file_search_query: str) -> [Optional[list[DataDescription]], Optional[str]]:
    try:
        queries = ast.literal_eval(file_search_query)
        descriptions: [list[DataDescription]] = []

        for query in queries:
            description, err = create_data_description(query)
            if err:
                return None, f"Failed to parse file search query: {query}"
            descriptions += [description]

        return descriptions, None
    except Exception as e:
        return None, f"Could not parse file search query json input: {e}"
