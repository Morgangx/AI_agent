import os
from functions.utils import valid_target_path
from google.genai import types

def get_files_info(working_directory: str, directory: str=".") -> str:
    try:
        target_dir: str | None = valid_target_path(working_directory, directory)
        if not target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        files_info: str = ""
        for file_name in os.listdir(target_dir):
            full_path: str = os.path.join(target_dir, file_name)
            if os.path.isdir(full_path):
                size: int = get_dir_size(full_path)
                is_dir: bool = True
            else:
                size: int = os.path.getsize(full_path)
                is_dir = False
            files_info += f"- {file_name}: file_size={size} bytes, is_dir={is_dir}\n"
        return files_info.removesuffix("\n")
    except Exception as e:
        return f"Error: {e}"

def get_dir_size(path: str='.') -> int:
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp: str = os.path.join(dirpath, f)
            # skip if it is symbolic link to avoid infinite loops/double counting
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

