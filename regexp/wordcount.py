import re

# BUG: without \b word boundaries the pattern matches "log" inside "login",
# BUG: "dialog", and "catalog", inflating the count
PATTERN = r"log"


def count_word(text, pattern):
    return len(re.findall(pattern, text))


if __name__ == "__main__":
    text = "Check the log file before login; the dialog shows the catalog entry"
    count = count_word(text, PATTERN)
    print(f"Count of 'log': {count}")
    print("Expected: 1 (only the standalone word 'log')")
