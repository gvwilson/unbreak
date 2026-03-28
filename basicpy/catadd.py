import sys


def average_scores(filename):
    """Return the average of numeric scores stored one per line."""
    total = 0
    count = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                total = total + line  # BUG: string concatenation, not numeric addition
                count += 1
    return total / count


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "catadd.txt"
    print(f"Average: {average_scores(filename)}")
