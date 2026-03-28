import sys


def count_words(filename):
    """Return a dictionary mapping each word to its frequency."""
    counts = {}
    with open(filename) as f:
        for line in f:
            for word in line.split():
                counts[word] += 1  # BUG: KeyError on first occurrence of each word
    return counts


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "nokey.txt"
    counts = count_words(filename)
    for word, count in sorted(counts.items(), key=lambda x: -x[1])[:5]:
        print(f"{word}: {count}")
