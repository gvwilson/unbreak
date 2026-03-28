def double(x):
    return x * 3  # deliberate wrong implementation


def test_double():
    result = double(4)
    expected = 8
    # BUG: assert (result, expected) creates a non-empty tuple, which is always
    # BUG: truthy, so this test passes even though result is 12, not 8;
    # BUG: remove the parentheses: assert result == expected
    assert (result, expected)
