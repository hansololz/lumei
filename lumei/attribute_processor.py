from datetime import datetime

from lumei.query_param import QueryParamAttribute


def get_attribute_results(
        attribute_query: dict[str, QueryParamAttribute],
        input_file_path: str,
        start_time: datetime,
        end_time: datetime,
) -> dict[str, any]:
    result: dict[str, any] = {}
    print("HERE 2")
    print(attribute_query)

    for key, attribute in attribute_query.items():
        if attribute is QueryParamAttribute.FILE_PATH:
            result[key] = input_file_path
        elif attribute is QueryParamAttribute.START_TIMESTAMP:
            result[key] = start_time.timestamp()
        elif attribute is QueryParamAttribute.START_DATETIME:
            result[key] = start_time.strftime('%Y-%m-%d %H:%M:%S')
        elif attribute is QueryParamAttribute.END_TIMESTAMP:
            result[key] = end_time.timestamp()
        elif attribute is QueryParamAttribute.END_DATETIME:
            result[key] = end_time.strftime('%Y-%m-%d %H:%M:%S')

    return result
