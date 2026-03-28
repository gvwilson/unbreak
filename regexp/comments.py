import re

# BUG: the pattern is case-sensitive, so "todo" and "Todo" are not matched
PATTERN = r"# TODO:"


def find_todos(source):
    return re.findall(PATTERN, source)


if __name__ == "__main__":
    source = (
        "x = 1  # TODO: replace with config value\n"
        "y = 2  # todo: remove this line\n"
        "z = 3  # Todo: clean up before release\n"
    )
    found = find_todos(source)
    print(f"Found {len(found)} TODO comment(s), expected 3")
