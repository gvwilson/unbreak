def positive_numbers(data):
    """Yield each positive number from data."""
    return (x for x in data if x > 0)


if __name__ == "__main__":
    data = [-1, 2, -3, 4, -5, 6, -7, 8]

    gen = positive_numbers(data)
    total = sum(gen)               # consumes the generator
    count = sum(1 for _ in gen)    # BUG: gen is exhausted; count is always 0

    print(f"Total: {total}")
    print(f"Count: {count}")       # prints 0 instead of 4

    if count > 0:
        print(f"Mean:  {total / count}")
    else:
        print("Cannot compute mean: generator was exhausted before count was taken")
