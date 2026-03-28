def collect_items(new_items, result=[]):  # BUG: mutable default argument
    """Append new_items to result and return it."""
    for item in new_items:
        result.append(item)
    return result


if __name__ == "__main__":
    first = collect_items(["a", "b"])
    print(f"First call:  {first}")    # ['a', 'b']

    second = collect_items(["c"])
    print(f"Second call: {second}")   # expected ['c'], got ['a', 'b', 'c']

    print(f"First again: {first}")    # also now ['a', 'b', 'c'] — same object
