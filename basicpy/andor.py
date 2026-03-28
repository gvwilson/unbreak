def is_valid_password(password):
    """Return True if password is at least 8 characters and contains a digit."""
    has_length = len(password) >= 8
    has_digit = any(c.isdigit() for c in password)
    if not has_length and not has_digit:  # BUG: should be 'or'; only rejects if BOTH fail
        return False
    return True


if __name__ == "__main__":
    tests = [
        ("abc",      False),  # too short, no digit      — should be rejected
        ("abcdefgh", False),  # long enough but no digit — should be rejected
        ("abc1",     False),  # has digit but too short  — should be rejected
        ("abcdefg1", True),   # valid: long enough and has a digit
    ]
    for password, expected in tests:
        result = is_valid_password(password)
        status = "OK  " if result == expected else "FAIL"
        print(f"{status} is_valid_password({password!r}) = {result} (expected {expected})")
