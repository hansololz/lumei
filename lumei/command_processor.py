import os
import subprocess

from lumei.query_param import CommandQueryParam


def process_commands(
        input_file_path: str,
        commands: list[CommandQueryParam],
) -> dict[str, any]:
    results: dict[str, any] = {}

    for command in commands:
        prepared_command = command.command.replace("%input_file_path%", input_file_path)
        subprocess.run(prepared_command, shell=True, capture_output=True, text=True)

        for name, environment_variable in command.names.items():
            results[name] = os.getenv(environment_variable, None)

    return results
