import sys
import time


def most_common_slow(text):
    """Return the most common word using a repeated full-text scan per word."""
    words = text.split()
    unique = set(words)
    best_word, best_count = None, 0
    for word in unique:
        count = text.count(word)  # BUG: scans the entire text for every unique word
        if count > best_count:
            best_count, best_word = count, word
    return best_word, best_count


def generate_text(num_words=50_000, vocab_size=500):
    """Generate a reproducible text with a known vocabulary for timing tests."""
    import random
    random.seed(42)
    vocab = [f"word{i}" for i in range(vocab_size)]
    return " ".join(random.choice(vocab) for _ in range(num_words))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            text = f.read()
        print(f"Loaded {len(text.split())} words from {sys.argv[1]}")
    else:
        print("No file given; generating 50,000-word test text…")
        text = generate_text()

    start = time.perf_counter()
    word, count = most_common_slow(text)
    elapsed = time.perf_counter() - start

    print(f"Most common: {word!r} ({count} times)")
    print(f"Slow method: {elapsed:.3f}s")
    print()
    print("Fix: replace the loop with collections.Counter(text.split()).most_common(1)")
