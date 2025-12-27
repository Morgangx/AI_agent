import os

def valid_target_path(working_directory:str, subpath: str) -> None | str:
    working_dir_abs: str = os.path.abspath(working_directory)
    target_file_path: str = os.path.normpath(os.path.join(working_dir_abs, subpath))
    valid_target_path: bool = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
    if not valid_target_path:
        return None
    return target_file_path