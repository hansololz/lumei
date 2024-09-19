import ast
from typing import Optional


class QueryParam:
    def __init__(self, name: str, search: str):
        self.name = name
        self.search = search


def parse_query_string(query_string: str) -> [Optional[list[QueryParam]], Optional[str]]:
    try:
        query_objects = ast.literal_eval(query_string)
    except Exception as e:
        return None, f"Failed to parse query with string: {e}"

    if query_objects is list:
        return None, f"Query must be an array of objects, got string: {query_string}"

    seen_param_names = []

    query = []

    for query_object in query_objects:
        name = query_object.get("name")
        search = query_object.get("search")

        if not name:
            return None, f"Query parameter name is required: {query_string}"

        if not search:
            return None, f"Query parameter search instruction required: {query_string}"

        if name in seen_param_names:
            return None, f"Found duplicate query parameter name: {name}"

        seen_param_names.append(name)

        query.append(
            QueryParam(
                name=name,
                search=search,
            )
        )

    return query, None
