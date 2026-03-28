import sys


def top_scorer(filename):
    """Return the (name, score) pair with the highest score."""
    best_name = None
    best_score = -1
    with open(filename) as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split(",")
            name = parts[0]
            score = int(parts[1])  # BUG: ValueError when name contains a comma,
            if score > best_score:  #      because parts[1] is then part of the name
                best_score = score
                best_name = name
    return best_name, best_score


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "commas.csv"
    name, score = top_scorer(filename)
    print(f"Top scorer: {name} ({score})")
