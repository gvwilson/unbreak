def summarize(values):
    return {"count": len(values), "total": sum(values)}


def test_summarize(tmp_path):
    data = [10, 20, 30]
    result = summarize(data)
    # BUG: writes to "output.json" in the current working directory, leaving a
    # BUG: file behind after the test and causing interference if two test runs
    # BUG: overlap; use tmp_path / "output.json" to write to a temporary directory
    # BUG: that pytest creates and removes automatically
    import json
    with open("output.json", "w") as f:
        json.dump(result, f)
    with open("output.json") as f:
        saved = json.load(f)
    assert saved["count"] == 3
    assert saved["total"] == 60
