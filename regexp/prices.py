import re

# BUG: .* is greedy and matches from the first <amount> tag to the last </amount>
# BUG: tag, collapsing all prices into a single match
PATTERN = r"<amount>(.*)</amount>"


def extract_amounts(html):
    return re.findall(PATTERN, html)


if __name__ == "__main__":
    html = "<amount>9.99</amount><tax>1.00</tax><amount>14.99</amount>"
    amounts = extract_amounts(html)
    print(f"Amounts: {amounts}")
    print(f"Expected 2 amounts, got {len(amounts)}")
