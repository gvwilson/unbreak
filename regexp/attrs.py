import re

# BUG: \w* matches zero or more word characters, so id="" (an empty attribute)
# BUG: is also matched and returned as an empty string in the results
PATTERN = r'id="(\w*)"'


def find_ids(html):
    return re.findall(PATTERN, html)


if __name__ == "__main__":
    html = '<div id="main"><p id="">text</p><span id="footer"></span>'
    ids = find_ids(html)
    print(f"IDs: {ids}")
    print("Expected only non-empty IDs: ['main', 'footer']")
