def filter_negatives(numbers):
    """Return a new list containing only the non-negative values."""
    result = []
    for n in numbers:
        if n >= 0:
            result.append(n)
    # BUG: missing 'return result'


if __name__ == "__main__":
    data = [-3, 1, -1, 4, -1, 5, -9, 2, -6]
    filtered = filter_negatives(data)
    print(f"Result:   {filtered}")   # BUG: prints None
    print(f"Expected: [1, 4, 5, 2]")
