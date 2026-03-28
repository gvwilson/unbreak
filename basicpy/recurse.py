def factorial(n):
    """Return n! for non-negative n."""
    if n > 0:                        # BUG: should be >= 0; n=0 falls through with no return
        return n * factorial(n - 1)
    # n == 0 reaches here and returns None implicitly,
    # so factorial(1) = 1 * factorial(0) = 1 * None → TypeError


if __name__ == "__main__":
    for n in [5, 3, 1, 0]:
        print(f"{n}! = {factorial(n)}")
