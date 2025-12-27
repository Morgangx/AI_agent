import os
from config import CHARACTER_LIMIT

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file_path: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir: bool = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file_path, mode="r") as f:
            content: str = f.read(CHARACTER_LIMIT)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
            return content
    except Exception as e:
        return f'Error: {e}'
    