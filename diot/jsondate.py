import json
from datetime import datetime


def make_report(title, value):
    """Build a report dict including the current timestamp."""
    return {
        "title": title,
        "value": value,
        "generated_at": datetime.now(),  # BUG: datetime is not JSON-serializable
    }


if __name__ == "__main__":
    report = make_report("monthly_sales", 48291.75)
    print(f"Report dict: {report}")
    print("Serializing to JSON...")
    print(json.dumps(report))  # BUG: TypeError: Object of type datetime is not JSON serializable
