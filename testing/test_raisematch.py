import pytest


def parse_count(value):
    if value is None:
        raise ValueError("count cannot be None")
    if not str(value).isdigit():
        raise ValueError("count must be an integer")
    return int(value)


def test_parse_count_rejects_none():
    # BUG: pytest.raises checks only the exception type, not its message.
    # BUG: omitting match= means a ValueError raised for a different reason
    # BUG: (here "count must be an integer") also passes; add
    # BUG: match="cannot be None" to pin down the expected message.
    with pytest.raises(ValueError):
        parse_count("abc")
