import re

# BUG: without re.MULTILINE, ^ matches only the very start of the entire string,
# BUG: not the start of each line, so headings after the first line are missed
PATTERN = r"^#{1,3} .+"


def find_headings(text):
    return re.findall(PATTERN, text)


if __name__ == "__main__":
    doc = "# Introduction\n## Background\n### Methods\nParagraph text.\n## Results"
    headings = find_headings(doc)
    print(f"Found {len(headings)} heading(s): {headings}")
    print("Expected 4 headings")
