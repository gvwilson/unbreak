import re

# BUG: re.match only checks at the very start of the string, so a date that
# BUG: appears after other text is never found
PATTERN = r"\d{4}-\d{2}-\d{2}"


def contains_date(line):
    return bool(re.match(PATTERN, line))


if __name__ == "__main__":
    lines = [
        "2024-01-15: server started",
        "ERROR on 2024-01-15: disk full",
        "no date in this line",
    ]
    for line in lines:
        label = "has date" if contains_date(line) else "no date "
        print(f"{label}: {line!r}")
