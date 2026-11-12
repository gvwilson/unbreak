def pair(names, scores):
    # BUG: zip stops at the shorter iterable, so the last name is silently
    # BUG: dropped when scores has fewer entries than names
    return list(zip(names, scores))


names = ["Alice", "Bob", "Carol"]
scores = [90, 85]
print(pair(names, scores))  # expect 3 pairs, get [('Alice', 90), ('Bob', 85)]
