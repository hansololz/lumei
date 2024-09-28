import os
import subprocess

from lumei.query_param import CommandQueryParam


def process_commands(
        input_file_path: str,
        commands: list[CommandQueryParam],
) -> dict[str, any]:
    results: dict[str, any] = {}

    for command in commands:
        # print_variable_command = "LUMEI_VARIABLE_OUTPUT_START "

        # for names, _ in command.names.items():
        #     print_variable_command += f"${environment_variable}"
        #     print_variable_command += " LUMEI_VARIABLE_OUTPUT "

        prepared_command = command.command.replace("%input_file_path%", input_file_path)
        command_output = subprocess.run(prepared_command, shell=True, capture_output=True, text=True)

        print(command_output.stdout)

        for name, environment_variable in command.names.items():
            results[name] = os.getenv(environment_variable, None)

    return results
