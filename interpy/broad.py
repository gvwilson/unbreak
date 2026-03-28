from urllib.parse import urlparse


URLS = [
    "https://example.com/page1",
    "https://example.com/page2",
    "not-a-valid-url",            # BUG: malformed: no scheme
    "https://example.com/page4",
    "https://example.com/page5",
]


def fetch_title(url):
    """Return a simulated page title; raises ValueError for malformed URLs."""
    parsed = urlparse(url)
    if not parsed.scheme:
        raise ValueError(f"Invalid URL: {url!r}")
    return f"Title from {parsed.netloc}{parsed.path}"


def scrape_all(urls):
    """Fetch a title for each URL and return the list of results."""
    titles = []
    try:
        for url in urls:                   # BUG: try/except wraps the entire loop;
            title = fetch_title(url)       # BUG: first ValueError exits the loop
            titles.append(title)           # BUG: and silently discards remaining URLs
    except Exception:
        pass
    return titles


if __name__ == "__main__":
    results = scrape_all(URLS)
    valid = sum(1 for u in URLS if urlparse(u).scheme)
    print(f"Got {len(results)} titles (expected {valid}):")
    for t in results:
        print(f"  {t}")
