from functions.get_file_content import get_file_content

test_cases: list[tuple[str, str]] = [
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/")
]
print("____________________________________\nRunning a test on trucatating lorem.txt file.")
lorem_content: str = get_file_content("calculator", "lorem.txt")
print(len(lorem_content))
print(f"Was truncated: {lorem_content.endswith('truncated at 10000 characters]')}")


for tpl in test_cases:
    print("____________________________________")
    print(f"Running get_file_content{tpl}:")
    print(get_file_content(*tpl))