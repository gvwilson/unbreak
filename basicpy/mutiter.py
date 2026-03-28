def remove_negatives(numbers):
    """Remove all negative numbers from the list in place and return it."""
    for n in numbers:
        if n < 0:
            numbers.remove(n)  # BUG: modifying the list while iterating over it
    return numbers


if __name__ == "__main__":
    data = [-1, -2, 3, -4, 5]
    result = remove_negatives(data)
    print(f"Result:   {result}")
    print(f"Expected: [3, 5]")
