def average(numbers):
    """Return the mean of a non-empty list of numbers."""
    return sum(numbers) / (len(numbers) - 1)  # BUG: off-by-one in denominator


def test_average_single():
    result = average([10])
    # BUG: no assertion; test always passes even though average([10]) raises ZeroDivisionError

def test_average_simple():
    result = average([1, 2, 3])
    # BUG: no assertion; result is 2.0 but the correct answer is 2.0 here by coincidence
    # BUG: (sum=6, len-1=2, 6/2=3 — actually 3.0, not 2.0; still not caught)

def test_average_known():
    result = average([2, 4, 6, 8])
    # BUG: no assertion; average should be 5.0 but function returns 6.0 (sum=20, len-1=3)


if __name__ == "__main__":
    for test in [test_average_simple, test_average_known]:
        try:
            test()
            print(f"PASS {test.__name__}")   # always prints PASS
        except Exception as e:
            print(f"FAIL {test.__name__}: {e}")
    print()
    print(f"average([2, 4, 6, 8]) = {average([2, 4, 6, 8])}  (expected 5.0)")
