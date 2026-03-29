import re
import sys


def extract_prices(html):
    """Return all prices found in the HTML as a list of floats."""
    # BUG: pattern matches class="price" but the page uses class="product-price";
    # BUG: re.findall returns [] with no error, so the caller never knows it failed
    pattern = r'<span class="price">\$([\d.]+)</span>'
    matches = re.findall(pattern, html)
    return [float(m) for m in matches]


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "missparse.html"
    with open(filename) as f:
        html = f.read()
    prices = extract_prices(html)
    if prices:
        print(f"Prices: {prices}")
        print(f"Total:  ${sum(prices):.2f}")
    else:
        print("No prices found.")   # BUG: silently wrong; three prices are in the file
