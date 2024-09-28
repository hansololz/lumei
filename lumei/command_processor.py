import os
import subprocess

from lumei.query_param import CommandQueryParam


def process_commands(
        input_file_path: str,
        commands: list[CommandQueryParam],
) -> dict[str, any]:
    results: dict[str, any] = {}

    for command in commands:
        print_variable_command_parts: list[str] = []
        result_names: list[str] = []

        for name, variable_name in command.names.items():
            print_variable_command_parts.append(f" ${variable_name} ")
            result_names.append(name)

        delimiter = "LUMEI_VARIABLE_DELIMITER"

        print_all_variable_command = (f"echo \"LUMEI_VARIABLE_START{delimiter.join(print_variable_command_parts)}"
                                      f"LUMEI_VARIABLE_END\"")

        replaced_command = command.command.replace("%input_file_path%", input_file_path)
        prepared_command = f"{replaced_command} && {print_all_variable_command}"
        command_output = subprocess.run(prepared_command, shell=True, capture_output=True, text=True)

        output_start_split = command_output.stdout.split("LUMEI_VARIABLE_START ")

        if len(output_start_split) == 2:
            variable_values = output_start_split[1].removesuffix(" LUMEI_VARIABLE_END\n").split(f" {delimiter} ")
        else:
            continue

        if len(result_names) != len(variable_values):
            continue
        else:
            for index in range(len(result_names)):
                results[result_names[index]] = variable_values[index]

    return results
