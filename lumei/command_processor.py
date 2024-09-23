import subprocess


class CommandQueryParam:
    def __init__(
            self,
            name: str,
            command: str
    ):
        self.name = name
        self.command = command


def process_commands(
        input_file_path: str,
        commands: list[CommandQueryParam],
) -> dict[str, str | int]:
    results: dict[str, str | int] = {}

    for command in commands:
        prepared_command = command.command.replace("%input_file_path%", input_file_path)
        result = subprocess.run(prepared_command, shell=True, capture_output=True, text=True)
        results[command.name] = result.stdout

    return results
