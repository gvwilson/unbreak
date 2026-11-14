def normalize(values):
    mean = sum(values) / len(values)
    return [v - mean for v in values]


def test_has_no_nan():
    result = [0.0, 0.0, float("nan")]
    # BUG: float("nan") is not equal to anything, including itself, so
    # BUG: `nan in result` uses == and is always False; this assertion passes
    # BUG: even though result contains a NaN; use math.isnan to detect it
    assert float("nan") not in result
