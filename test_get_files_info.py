from functions.get_files_info import get_files_info

test_cases: list[tuple[str, str]] = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../")
]
for tpl in test_cases:
    print(f"Running get_files_info{tpl}:")
    print(get_files_info(*tpl))
