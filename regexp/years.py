import re

# BUG: the capturing group around the year causes re.findall to return only the
# BUG: captured portion, so the results contain years instead of full dates
PATTERN = r"(\d{4})-\d{2}-\d{2}"


def find_dates(text):
    return re.findall(PATTERN, text)


if __name__ == "__main__":
    text = "Events scheduled for 2024-01-15 and 2024-03-22."
    dates = find_dates(text)
    print(f"Dates: {dates}")
    print("Expected: ['2024-01-15', '2024-03-22']")
