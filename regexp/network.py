import re

# BUG: the dots between octets are not escaped, so they match any character and
# BUG: strings like "192X168X1X1" pass the check
PATTERN = r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}"


def is_ip_address(text):
    return bool(re.fullmatch(PATTERN, text))


if __name__ == "__main__":
    candidates = [
        "192.168.1.1",
        "192X168X1X1",
        "10.0.0.256",
        "not-an-ip",
    ]
    for c in candidates:
        print(f"{'Valid' if is_ip_address(c) else 'Invalid':8s}: {c!r}")
