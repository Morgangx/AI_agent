from functions.run_python_file import run_python_file
from typing import Any

test_cases: list[Any] = [
    ("calculator", "main.py"),
    ("calculator", "main.py", ["3 + 5"]),
    ("calculator", "tests.py"),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py"),
    ("calculator", "lorem.txt")
]
for tpl in test_cases:
    print(f"Running 'run_python_file{tpl}")
    print(run_python_file(*tpl))