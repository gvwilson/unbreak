import re

# BUG: the pattern is compiled without re.IGNORECASE, so column names that start
# BUG: with a capital letter are not recognized
COLUMN_RE = re.compile(r"name|email|phone")


def find_columns(header):
    return [col for col in header.split(",") if COLUMN_RE.search(col)]


if __name__ == "__main__":
    header = "Name,Email,Phone,Address"
    found = find_columns(header)
    print(f"Recognized columns: {found}")
    print("Expected: ['Name', 'Email', 'Phone']")
