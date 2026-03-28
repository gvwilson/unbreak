import sys


def parse_scores(filename):
    """Return a list of (name, city, score) triples from a CSV file."""
    records = []
    with open(filename) as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split(",")
            name = parts[0]
            city = parts[1]        # BUG: when city contains a comma and is quoted,
            score = int(parts[2])  # BUG: parts[1] is only the first half of the city
            records.append((name, city, score))
    return records


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "quotecsv.csv"
    for name, city, score in parse_scores(filename):
        print(f"{name} ({city}): {score}")
