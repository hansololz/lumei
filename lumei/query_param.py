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
            names: dict[str, str],
            command: str
    ):
        self.names = names
        self.command = command


class QueryParam:
    def __init__(
            self,
            name: Optional[str],
            names: Optional[str],
            search: Optional[str],
            attribute: Optional[QueryParamAttribute],
            command: Optional[str],
    ):
        self.name = name
        self.names = names
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
        names = query_object.get("names")
        search = query_object.get("search")
        attribute = query_object.get("attribute")
        command = query_object.get("command")

        if not name and not names:
            return None, f"Query parameter name is required: {query_string}"

        if name in seen_param_names:
            return None, f"Found duplicate query parameter name: {name}"
        else:
            seen_param_names.append(name)

        # print(f"HERE {name} AND {names}")

        if names:
            for environment_name in names.items():
                if environment_name in seen_param_names:
                    return None, f"Found duplicate command query parameter name: {environment_name}"
                else:
                    seen_param_names.append(environment_name)

        if name and search and not attribute and not command:
            query.append(
                QueryParam(
                    name=name,
                    names=None,
                    search=search,
                    attribute=None,
                    command=None,
                )
            )
        elif name and not search and attribute and not command:
            query.append(
                QueryParam(
                    name=name,
                    names=None,
                    search=None,
                    attribute=QueryParamAttribute(attribute),
                    command=None,
                )
            )
        elif names and not search and not attribute and command:
            print("HERE 5")

            query.append(
                QueryParam(
                    name=None,
                    names=names,
                    search=None,
                    attribute=None,
                    command=command,
                )
            )
        else:
            return None, (f"Error, query parameter should only have one of `search`, `attribute`, or `command`: "
                          f"{query_object}")

    return query, None
