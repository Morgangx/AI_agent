from functions.utils import valid_target_path
import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        target_path: str | None = valid_target_path(working_directory, file_path)
        if not target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir: str = os.path.dirname(file_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(target_path, mode="w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrite content of specified file with the given content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path the specified file, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to overwrite the file with."
            )
        },
    ),
)