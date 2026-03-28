from unittest.mock import patch

import mockpatch_user


def test_process():
    # BUG: patching fetch_data in mockpatch_source, but mockpatch_user already
    # holds its own reference to the real function from the 'import' statement;
    # the patch replaces the name in the source module but mockpatch_user.process()
    # calls its own reference and never sees the mock
    with patch("mockpatch_source.fetch_data", return_value=["mock", "data"]):
        result = mockpatch_user.process()

    print(f"Result:   {result}")
    print(f"Expected: ['MOCK', 'DATA']")
    assert result == ["MOCK", "DATA"], (
        f"Mock had no effect — got {result!r}\n"
        "Fix: patch 'mockpatch_user.fetch_data' (where it is used), "
        "not 'mockpatch_source.fetch_data' (where it is defined)"
    )


if __name__ == "__main__":
    try:
        test_process()
        print("PASS")
    except AssertionError as e:
        print(f"FAIL: {e}")
