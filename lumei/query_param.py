import ast
from enum import Enum
from typing import Optional


class QueryParamAttribute(str, Enum):
    FILE_PATH = "FILE_PATH"
    START_TIMESTAMP = "START_TIMESTAMP"
    END_TIMESTAMP = "END_TIMESTAMP"
    START_DATETIME = "START_DATETIME"
    END_DATETIME = "END_DATETIME"


class FileSearchQueryParam:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class CommandQueryParam:
    def __init__(
            self,
            name: str,
            command: str
    ):
        self.name = name
        self.command = command


class QueryParam:
    def __init__(
            self, name: str,
            search: Optional[str],
            attribute: Optional[QueryParamAttribute],
            command: Optional[str],
    ):
        self.name = name
        self.search = search
        self.attribute = attribute
        self.command = command


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
        command = query_object.get("command")

        if not name:
            return None, f"Query parameter name is required: {query_string}"

        if name in seen_param_names:
            return None, f"Found duplicate query parameter name: {name}"

        seen_param_names.append(name)

        if search and not attribute and not command:
            query.append(
                QueryParam(
                    name=name,
                    search=search,
                    attribute=None,
                    command=None,
                )
            )
        elif not search and attribute and not command:
            query.append(
                QueryParam(
                    name=name,
                    search=None,
                    attribute=QueryParamAttribute(attribute),
                    command=None,
                )
            )
        elif not search and not attribute and command:
            query.append(
                QueryParam(
                    name=name,
                    search=None,
                    attribute=None,
                    command=command,
                )
            )
        else:
            return None, (f"Error, query parameter should only have one of `search`, `attribute`, or `command`: "
                          f"{query_object}")

    return query, None
