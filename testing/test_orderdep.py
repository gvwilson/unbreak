import pytest

_registry = {}


def register(name, value):
    _registry[name] = value


def lookup(name):
    return _registry[name]


def test_register():
    register("threshold", 10)
    assert lookup("threshold") == 10


def test_lookup():
    # BUG: this test relies on test_register having populated _registry first;
    # BUG: pytest does not guarantee execution order, and running this test alone
    # BUG: with pytest -k test_lookup raises a KeyError;
    # BUG: each test should set up its own state rather than depending on another test
    assert lookup("threshold") == 10
