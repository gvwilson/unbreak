import pytest


def parse_positive(value):
    if value <= 0:
        raise ValueError(f"{value} is not positive")
    return value


def test_parse_positive_rejects_zero():
    with pytest.raises(ValueError):
        result = parse_positive(0)
        # BUG: this assertion is never reached because parse_positive(0) raises
        # BUG: before it can execute; pytest.raises catches the exception and exits
        # BUG: the with block, so assertions on result must be placed after the
        # BUG: with block, not inside it
        assert result is None
