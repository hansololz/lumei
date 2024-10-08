from datetime import datetime

from lumei.attribute_processor import get_attribute_results
from lumei.command_processor import process_commands
from lumei.file_manager import save_result, find_matched_files, setup_output_file, \
    check_if_can_create_file
from lumei.openai.agent import create_agent
from lumei.openai.file_search import file_search, FileSearchQueryParam
from lumei.query_param import parse_query_string, QueryParamAttribute, CommandQueryParam


def execute_query_and_store_results(
        openai_api_key: str,
        input_files: str,
        output_file: str,
        file_search_query_string: str
) -> int:
    error = check_if_can_create_file(output_file)

    if error:
        print(error)
        return 1

    print("Verified permission to create file.")

    query, error = parse_query_string(file_search_query_string)

    if error:
        print(error)
        return 1

    file_search_query = []
    attribute_query: dict[str, QueryParamAttribute] = {}
    command_query: list[CommandQueryParam] = []
    query_param_names: list[str] = []
    for query_param in query:
        if query_param.name and query_param.search:
            query_param_names.append(query_param.name)
            file_search_query.append(
                FileSearchQueryParam(
                    name=query_param.name,
                    description=query_param.search,
                )
            )
        elif query_param.name and query_param.attribute:
            query_param_names.append(query_param.name)
            attribute_query[query_param.name] = query_param.attribute
        elif query_param.names and query_param.command:
            for name in query_param.names:
                query_param_names.append(name)

            command_query.append(CommandQueryParam(
                names=query_param.names,
                command=query_param.command,
            ))

    print("Parsed list of names and data descriptions for file search.")

    files, error = find_matched_files(input_files)

    if error:
        print(error)
        return 1

    print(f"Created list of files to process. Found {len(files)} files.")

    agent, error = create_agent(openai_api_key)

    if error:
        print(error)
        return 1

    print(f"Created agent with assistant id: {agent.assistant_id}.")

    print(f"Begun processing files.")

    results: [dict[str, str]] = []

    for file in files:
        start_time = datetime.now()
        result: dict[str, any] = {}
        file_search_results, error = file_search(agent, file, file_search_query)
        end_time = datetime.now()

        if file_search_results:
            result.update(file_search_results)

            command_results = process_commands(
                input_file_path=file,
                commands=command_query
            )

            result.update(command_results)

            attribute_results = get_attribute_results(
                attribute_query=attribute_query,
                input_file_path=file,
                start_time=start_time,
                end_time=end_time,
            )

            result.update(attribute_results)

            results.append(result)
            print(f"    {file} SUCCESS")
        elif error:
            print(f"    {file} FAILED: {error}")
        else:
            print(f"    {file} FAILED")

    print(f"Finished processing files.")

    error = setup_output_file(output_file)

    if error:
        print(error)
        return 1

    print(f"Created output file: {output_file}.")

    error = save_result(output_file, query_param_names, results)

    if error:
        print(error)
        return 1

    print(f"Wrote result to file: {output_file}.")

    return 0
