import sys


def find_value(filename, target):
    """Return the value for the matching region name in a pipe-delimited file."""
    with open(filename) as f:
        for line in f:
            parts = line.rstrip("\n").split("|")
            if len(parts) >= 2:
                region = parts[0]
                value = parts[1].strip()
                if region == target:  # BUG: region may have trailing space from export
                    return value
    return None


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "trailing.txt"
    for target in ["North", "South", "East", "West"]:
        result = find_value(filename, target)
        if result is None:
            print(f"{target!r}: not found")
        else:
            print(f"{target!r}: {result}")
