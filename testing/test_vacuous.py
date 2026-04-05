def total(values):
    return sum(values)


def test_total():
    result = total([1, 2, 3])
    # BUG: no assertion; the test always passes regardless of what total() returns
    # BUG: because pytest only reports failure when an assertion fails or an exception
    # BUG: is raised; add assert result == 6 to actually check the result
