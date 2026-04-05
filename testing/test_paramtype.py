import pytest


@pytest.mark.parametrize("values,expected", [
    ([3, 1, 2], [1, 2, 3]),
    ([9, 5, 7], [5, 7, 9]),
    ([4, 4, 1], [1, 4, 4]),
])
def test_sort_returns_sorted_list(values, expected):
    # BUG: list.sort() sorts in place and returns None; the assertion compares
    # BUG: None against the expected list and fails; use sorted(values) instead
    # BUG: to get a new sorted list without modifying the original
    result = values.sort()
    assert result == expected
