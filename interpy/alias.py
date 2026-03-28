def reversed_copy(data):
    """Return a reversed copy of data, leaving the original unchanged."""
    data.reverse()  # BUG: reverse() mutates in place; caller's list is also reversed
    return data


if __name__ == "__main__":
    original = [1, 2, 3, 4, 5]
    result = reversed_copy(original)
    print(f"Result:   {result}")
    print(f"Original: {original}")  # also reversed — same object, not a copy
