import re

# BUG: without re.DOTALL, the dot does not match newlines, so the pattern never
# BUG: captures exception messages that span more than one line
PATTERN = r"EXCEPTION: (.+) END"


def find_exceptions(log):
    return re.findall(PATTERN, log)


if __name__ == "__main__":
    log = "EXCEPTION: ValueError\n  line 42 in process\n  line 10 in main\n END"
    results = find_exceptions(log)
    print(f"Found {len(results)} exception(s), expected 1")
    print(f"Matches: {results}")
