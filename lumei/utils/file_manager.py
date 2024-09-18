import csv
import os
import re
from typing import Optional

import pandas as pd

file_search_query_example = """
[
    { "name": "Student Name", "description": "Name of the student." },
    { "name": "School", "description": "Student's school" },
    { "name": "Major", "description": "Student's major." }
]
"""


class DataDescription:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


def create_data_description(query: dict[str, str]) -> [Optional[DataDescription], Optional[str]]:
    name = query['name']
    description = query['description']

    if not name:
        return None, f"Missing name field for file search query. Example of correct query: {file_search_query_example}"

    if not description:
        return None, f"Missing description field for file search query. Example of correct query: {file_search_query_example}"

    return DataDescription(name, description), None


def check_if_can_create_file(output_file) -> Optional[str]:
    if not output_file.endswith((".csv", ".xlsx", ".json")):
        return "Only \".csv\", \".xlsx\", or \".json\" file types are supported."

    try:
        with open(output_file, "w"):
            pass
    except PermissionError:
        return f"Permission denied for creating output file: \"{output_file}\"."
    except Exception as e:
        return f"An error occurred: {e}"

    return None


def save_result(output_file: str, dataset: [DataDescription], results: [dict[str, str]]) -> Optional[str]:
    rows: [dict[str, str]] = []

    for result in results:
        row = []

        for data in dataset:
            if result[data.name]:
                row.append(result[data.name])
            else:
                row.append(None)
        rows.append(row)

    try:
        with open(output_file, "w", newline=""):
            df = pd.DataFrame(results)

            if output_file.endswith(".csv"):
                df.to_csv(output_file, index=False)
            if output_file.endswith(".xlsx"):
                df.to_excel(output_file, index=False)
            if output_file.endswith(".json"):
                df.to_json(output_file, orient='records', lines=False, indent=4)
        return None
    except Exception as e:
        return f"Failed to write result to output file {e}"


def setup_output_file(output_file: str, dataset: [DataDescription]) -> Optional[str]:
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", newline="") as file:
        column_headers = [data.name for data in dataset]
        writer = csv.writer(file)
        writer.writerow(column_headers)

    return None


def find_matched_files(input_string: str) -> [Optional[list[str]], Optional[str]]:
    parts = re.split(r"[,\n]+", input_string)
    cleaned_parts = [part.strip() for part in parts if part.strip()]

    files = []

    for part in cleaned_parts:
        files += find_matched_files_for_pattern(part)

    if not files:
        return None, f"No file found given locations: {input_string}"

    return files, None


def find_matched_files_for_pattern(pattern) -> [str]:
    if os.path.isdir(pattern):
        return [os.path.join(pattern, f) for f in os.listdir(pattern) if os.path.isfile(os.path.join(pattern, f))]

    if os.path.isfile(pattern):
        return [pattern]

    directory, file_pattern = os.path.split(pattern)
    if not directory:
        directory = "."

    matched_files = []
    for filename in os.listdir(directory):
        if re.match(file_pattern, filename):
            matched_files.append(os.path.join(directory, filename))

    return matched_files
