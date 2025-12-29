import os
import subprocess
from functions.utils import valid_target_path
from google.genai import types

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
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python file relative to the working director with optional parameters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path the python file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Aditional parametes for the python script, default is None (no aditional parameters)."
            ),
        },
    ),
)