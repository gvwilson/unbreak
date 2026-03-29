def squared_sorted(numbers):
    """Return a sorted list of squares of the input numbers."""
    squared = [x**2 for x in numbers]
    squared = squared.sort()  # BUG: list.sort() returns None; result is discarded
    return squared


if __name__ == "__main__":
    result = squared_sorted([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"Result: {result}")  # BUG: prints None
