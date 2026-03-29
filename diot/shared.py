# Module-level registry — shared state that persists between tests
REGISTRY = {}


def register(name, value):
    REGISTRY[name] = value


def lookup(name):
    return REGISTRY.get(name)


# --- tests ---

def test_register():
    register("alpha", 1)
    assert lookup("alpha") == 1


def test_lookup_absent():
    # BUG: assumes REGISTRY is empty, but test_register() already added "alpha"
    assert lookup("absent") is None
    assert len(REGISTRY) == 0  # BUG: fails when run after test_register()


def test_overwrite():
    register("alpha", 99)
    # BUG: assumes starting value; actually clobbers the value left by test_register()
    assert lookup("alpha") == 99


if __name__ == "__main__":
    for test in [test_register, test_lookup_absent, test_overwrite]:
        try:
            test()
            print(f"PASS {test.__name__}")
        except AssertionError as e:
            print(f"FAIL {test.__name__}: {e}")
