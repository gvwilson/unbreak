import re

# BUG: re.search finds the pattern anywhere in the string, so a sentence that
# BUG: contains a phone number passes even though it is not a phone number
PATTERN = r"\d{3}-\d{3}-\d{4}"


def is_valid_phone(text):
    return bool(re.search(PATTERN, text))


if __name__ == "__main__":
    tests = [
        "555-867-5309",
        "call 555-867-5309 now",
        "555-867-53090000",
        "not a number",
    ]
    for t in tests:
        print(f"{'Valid' if is_valid_phone(t) else 'Invalid':8s}: {t!r}")
