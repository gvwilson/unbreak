import json
import sys


def is_allowed(user_id, allowed_file):
    """Return True if user_id appears in the allowed list in allowed_file."""
    with open(allowed_file) as f:
        data = json.load(f)
    return user_id in data["allowed_ids"]  # BUG: user_id is a str; IDs in JSON are int


if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else "42"
    # BUG: user_id is a string (from the command line); JSON IDs are integers
    result = is_allowed(user_id, "streq.json")
    print("Access granted." if result else "Access denied.")
