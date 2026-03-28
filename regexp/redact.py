import re

PATTERN = r"(SSN|DOB):\s*\S+"


def redact(text):
    # BUG: "\1" in a regular (non-raw) string is the SOH control character
    # BUG: (ASCII value 1), not a backreference; the label is lost in the output
    return re.sub(PATTERN, "\1: [redacted]", text)


if __name__ == "__main__":
    text = "Patient SSN: 123-45-6789, DOB: 1990-01-01"
    result = redact(text)
    print(repr(result))
    print("Expected: 'Patient SSN: [redacted], DOB: [redacted]'")
