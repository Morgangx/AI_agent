from functions.get_file_content import get_file_content

test_cases: list[tuple[str, str]] = [
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/")
]
for tpl in test_cases:
    print("____________________________________")
    print(f"Running get_file_content{tpl}:")
    print(get_file_content(*tpl))
