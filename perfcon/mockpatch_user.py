from mockpatch_source import fetch_data


def process():
    """Fetch records and return them uppercased."""
    return [item.upper() for item in fetch_data()]
