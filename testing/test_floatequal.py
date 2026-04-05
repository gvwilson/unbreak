import pytest


def running_total(values):
    total = 0.0
    for v in values:
        total += v
    return total


def test_running_total():
    result = running_total([0.1, 0.2, 0.3])
    # BUG: floating-point addition is not exact; 0.1 + 0.2 + 0.3 accumulates
    # BUG: rounding error and does not equal 0.6 in IEEE 754;
    # BUG: use pytest.approx: assert result == pytest.approx(0.6)
    assert result == 0.6
