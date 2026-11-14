def classify(n):
    if n < 0:
        return "negative"
    if n == 0:
        return "zero"
    return "positive"


def test_classify():
    assert classify(-5) == "negative"
    # BUG: this early return exits the test before the remaining assertions
    # BUG: run, so the zero and positive cases are never checked and the
    # BUG: test always passes; remove the return to run every assertion
    return
    assert classify(0) == "zero"
    assert classify(5) == "positive"
