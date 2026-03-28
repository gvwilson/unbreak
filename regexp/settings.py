import re

# BUG: the capturing group makes re.findall return only the matched group (the
# BUG: value after "="), not the full "key=value" string
PATTERN = r"\w+=(\w+)"


def list_values(text):
    return re.findall(PATTERN, text)


if __name__ == "__main__":
    config = "host=localhost port=8080 debug=true"
    values = list_values(config)
    print(f"Found: {values}")
    print("Expected: ['host=localhost', 'port=8080', 'debug=true']")
