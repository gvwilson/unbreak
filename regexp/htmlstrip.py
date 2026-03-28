import re

# BUG: [<>] matches angle-bracket characters themselves, not everything between
# BUG: them; no normal HTML tag contains only < or > so nothing is replaced
PATTERN = r"<[<>]+>"


def strip_tags(html):
    return re.sub(PATTERN, "", html)


if __name__ == "__main__":
    html = "<b>Hello</b>, <i>world</i>!"
    result = strip_tags(html)
    print(f"Result:   {result!r}")
    print("Expected: 'Hello, world!'")
