import ast
from enum import Enum
from typing import Optional


class QueryParamAttribute(str, Enum):
    FILE_PATH = "FILE_PATH"
    START_TIMESTAMP = "START_TIMESTAMP"
    END_TIMESTAMP = "END_TIMESTAMP"
    START_DATETIME = "START_DATETIME"
    END_DATETIME = "END_DATETIME"


class QueryParam:
    def __init__(
            self, name: str,
            search: Optional[str],
            attribute: Optional[QueryParamAttribute],
    ):
        self.name = name
        self.search = search
        self.attribute = attribute


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
        attribute = query_object.get("attribute")

        if not name:
            return None, f"Query parameter name is required: {query_string}"

        if name in seen_param_names:
            return None, f"Found duplicate query parameter name: {name}"

        seen_param_names.append(name)

        if search and attribute:
            return None, f"Query parameter should only have either `search` or `attribute`: {query_object}"
        elif search:
            query.append(
                QueryParam(
                    name=name,
                    search=search,
                    attribute=None,
                )
            )
        elif attribute:
            if attribute not in QueryParamAttribute:
                return None, f"Query parameter attribute not supported: {attribute}"

            query.append(
                QueryParam(
                    name=name,
                    search=None,
                    attribute=QueryParamAttribute(attribute),
                )
            )
        else:
            return None, f"Query parameter `search instruction` or `attribute` required: {query_string}"

    return query, None
