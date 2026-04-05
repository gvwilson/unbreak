import pytest


# BUG: session scope means this fixture is created once and shared across all tests;
# BUG: because the fixture returns a mutable list, modifications in one test are
# BUG: visible in later tests; use function scope (the default) so each test gets
# BUG: a fresh copy
@pytest.fixture(scope="session")
def user_list():
    return []


def test_add_user(user_list):
    user_list.append("Alice")
    assert len(user_list) == 1


def test_list_starts_empty(user_list):
    assert len(user_list) == 0
