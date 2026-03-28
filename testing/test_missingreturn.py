def strip_prefix(text, prefix):
    if text.startswith(prefix):
        text[len(prefix):]  # BUG: missing return; result is discarded


def test_strip_prefix():
    result = strip_prefix("ERROR: disk full", "ERROR: ")
    assert result == "disk full"
