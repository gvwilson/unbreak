import pytest


def parse_count(value):
    # BUG in source: raises TypeError for None, not ValueError
    return int(value)


def test_parse_count_rejects_none():
    with pytest.raises(Exception):
        # BUG: pytest.raises(Exception) catches any exception, including TypeError;
        # BUG: the test passes even though parse_count raises TypeError instead of
        # BUG: the expected ValueError; use pytest.raises(ValueError) to be specific
        parse_count(None)
