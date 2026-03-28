import os
import tempfile

import pytest


@pytest.fixture
def temp_file():
    path = tempfile.mktemp()
    # BUG: return gives no way to run cleanup code after the test finishes;
    # BUG: if the test fails, the temp file is never deleted;
    # BUG: use yield path and put os.remove(path) after the yield instead
    return path


def test_write_and_read(temp_file):
    with open(temp_file, "w") as f:
        f.write("hello")
    assert os.path.exists(temp_file)
    raise RuntimeError("test failed partway through")
