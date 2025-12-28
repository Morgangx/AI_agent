import os
import subprocess
from functions.utils import valid_target_path

def run_python_file(working_directory: str, file_path: str, args: None | tuple[str] = None) -> str:
    try:
        target_path: str | None = valid_target_path(working_directory, file_path)
        print(target_path)
        if not target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command: list[str] = ["python", target_path]
        if args:
            command.extend(args)
        completed_process: subprocess.CompletedProcess[str] = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30
            )
        output: str = ""
        if completed_process.returncode != 0:
            output += "Process exited with code X\n"
        if completed_process.stdout == '' and completed_process.stderr == '':
            output += "No output created\n"
        else:
            output += f'STDOUT: {completed_process.stdout}\n'
            output += f'STDERR: {completed_process.stderr}\n'
        return output.removesuffix("\n")
    except Exception as e:
        return f"Error: executing Python file: {e}"