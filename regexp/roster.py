import re

# BUG: group 1 captures the last name and group 2 captures the first name, but
# BUG: the replacement \1 \2 keeps them in the original order instead of swapping
PATTERN = r"(\w+),\s*(\w+)"


def reformat_name(name):
    return re.sub(PATTERN, r"\1 \2", name)


if __name__ == "__main__":
    names = ["Smith, Alice", "Jones, Bob", "Garcia, Carmen"]
    for name in names:
        print(f"{name!r} -> {reformat_name(name)!r}")
