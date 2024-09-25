import subprocess

from lumei.query_param import CommandQueryParam


def process_commands(
        input_file_path: str,
        commands: list[CommandQueryParam],
) -> dict[str, str | int]:
    results: dict[str, any] = {}

    for command in commands:
        prepared_command = command.command.replace("%input_file_path%", input_file_path)
        result = subprocess.run(prepared_command, shell=True, capture_output=True, text=True)
        results[command.name] = result.stdout.removesuffix("\n")

    return results
