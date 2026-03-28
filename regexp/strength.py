import re

# BUG: the pattern checks that a digit exists (via the lookahead) but does not
# BUG: check for an uppercase letter, so "password1" and "12345678" both pass
PATTERN = r"(?=.*\d)[A-Za-z\d]{8,}"


def is_strong(password):
    return bool(re.fullmatch(PATTERN, password))


if __name__ == "__main__":
    passwords = ["Password1", "password1", "PASSWORD1", "12345678"]
    for pw in passwords:
        print(f"{'Strong' if is_strong(pw) else 'Weak':8s}: {pw!r}")
