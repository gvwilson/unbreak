def total(values):
    return sum(values)


# BUG: pytest only discovers test functions whose names start with "test_".
# BUG: This function is named "check_total", so pytest never collects or runs
# BUG: it, and `pytest test_discovery.py` reports "no tests ran" instead of
# BUG: exercising total(). Rename it to test_total().
def check_total():
    assert total([1, 2, 3]) == 6
    assert total([1, 2, 3, 4]) == 10
