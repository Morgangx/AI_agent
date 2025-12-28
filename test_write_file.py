from functions.write_file import write_file

test_cases: list[tuple[str, str, str]] = [
    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed")
]
for tpl in test_cases:
    print(write_file(*tpl))