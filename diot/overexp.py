import re

# BUG: pattern is too permissive — no anchors, allows any word chars on both sides,
# BUG: no requirement for a valid TLD, matches things like "foo@bar" or "x@y"
EMAIL_PATTERN = r"\w+@\w+"


def extract_emails(text):
    """Return all email addresses found in text."""
    return re.findall(EMAIL_PATTERN, text)


if __name__ == "__main__":
    tests = [
        ("alice@example.com",        True),   # valid
        ("bob.smith@uni.edu",        True),   # valid (but dots in local part missed)
        ("not-an-email",             False),  # should not match
        ("foo@bar",                  False),  # no TLD — should not match
        ("user@host with spaces",    False),  # malformed — should not match
        ("x@y",                      False),  # too short — should not match
    ]
    for text, should_match in tests:
        found = extract_emails(text)
        matched = bool(found)
        status = "OK  " if matched == should_match else "FAIL"
        print(f"{status}  {text!r:35s} -> {found}")
