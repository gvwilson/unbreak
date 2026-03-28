import re

# BUG: \d{4} matches exactly four digits, but US ZIP codes have five, so valid
# BUG: ZIP codes are not found and four-digit apartment numbers are matched instead
PATTERN = r"\b\d{4}\b"


def find_zipcodes(text):
    return re.findall(PATTERN, text)


if __name__ == "__main__":
    text = "Ship to 90210 or 02134; apartment number is 4201"
    found = find_zipcodes(text)
    print(f"ZIP codes found: {found}")
    print("Expected: ['90210', '02134']")
