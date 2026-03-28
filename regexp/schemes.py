import re

# BUG: "http" appears before "https" in the alternation and is a prefix of it;
# BUG: the engine matches "http" at the start of "https://..." and stops there
PATTERN = r"http|https"


def get_scheme(url):
    m = re.match(PATTERN, url)
    return m.group(0) if m else None


if __name__ == "__main__":
    urls = [
        "http://example.com/page",
        "https://secure.example.com/login",
    ]
    for url in urls:
        print(f"scheme={get_scheme(url)!r}  url={url!r}")
