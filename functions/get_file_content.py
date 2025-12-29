import os
from functions.utils import valid_target_path
from config import CHARACTER_LIMIT
from google.genai import types

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target_path: str | None = valid_target_path(working_directory, file_path)
        if not target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_path, mode="r") as f:
            content: str = f.read(CHARACTER_LIMIT)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
            return content
    except Exception as e:
        return f'Error: {e}'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get contents of a specified file relative to the working directory, providing the file content as string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get the content from, relative to the working directory.",
            ),
        },
    ),
)