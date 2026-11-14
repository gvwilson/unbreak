# Testing

## Write a test that is actually discovered {: #testing-discovery}

Run `pytest test_discovery.py -v`. How many tests ran? Why does pytest
report that no tests were collected?

[% inc test_discovery.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the test function name `check_total`. pytest only collects
functions whose names start with `test_`, so `check_total` is silently
ignored and the run reports "no tests ran".

Shows: pytest's test-discovery rule and why a misspelled test name
means the function is never exercised.

To find it: run `pytest test_discovery.py --collect-only`. It lists no
tests. Rename `check_total` to `test_total` and rerun to confirm the
function is now collected.

</details>

## Test that a doubling function returns the right value {: #testing-tupleassert}

Run `pytest test_tupleassert.py -v`. Does the test pass? What value
does `double(4)` actually return? Check the pytest warning in the
output.

[% inc test_tupleassert.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `assert (result, expected)`, which creates a two-element
tuple. A non-empty tuple is always truthy, so the assertion never
fails regardless of whether `result == expected`. The correct form is
`assert result == expected` without the enclosing parentheses.

Shows: how easy it is to write an assertion that looks plausible but
is logically vacuous, and why pytest's warning about this pattern
should not be ignored.

To find it: read the pytest output carefully. It includes a warning
that a non-empty tuple is always truthy. Remove the outer parentheses
so the assertion becomes `assert result == expected`, then rerun to
confirm the test can now fail.

</details>

## Test that a result contains no NaN {: #testing-nan}

Run `pytest test_nan.py -v`. Does the test pass? The result list
contains a `NaN` — should it have failed?

[% inc test_nan.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `float("nan") not in result`. `NaN` is not equal to
anything, including itself, so the `in` test (which uses `==`) is
always `False`, and the assertion passes even though the list contains
a `NaN`.

Shows: that `NaN` comparisons are always `False`, and how to detect
`NaN` with `math.isnan`.

To find it: print `float("nan") == float("nan")` — it prints `False`.
Replace the assertion with `assert not any(math.isnan(x) for x in result)`.

</details>

## Test that a function rejects invalid input {: #testing-broadexc}

Run `pytest test_broadexc.py -v`. Does the test pass? What exception
does `parse_count(None)` actually raise? Is that the exception the
test intended to check?

[% inc test_broadexc.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `pytest.raises(Exception)`, which accepts any
exception, including `TypeError`. The test passes even though
`parse_count` raises a `TypeError` rather than the expected
`ValueError`, masking a bug in the function.

Shows: how to use a specific exception type in `pytest.raises` and why
catching the base `Exception` class in tests hides incorrect
behaviour.

To find it: add `assert isinstance(exc.value, ValueError)` after the
`with pytest.raises(Exception) as exc:` block. If that assertion
fails, the function is raising a different exception type than
intended.

</details>

## Test a function that reads from a temporary file {: #testing-noyield}

Run `pytest test_noyield.py -v`. The test fails. After it fails, check
whether the temp file still exists. Then change `return path` to
`yield path` and add `os.remove(path)` after the yield. Run again and
check the filesystem.

[% inc test_noyield.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `return` in a fixture that needs to perform
cleanup. With `return`, there is no way to run code after the test
finishes, so the temp file is left on disk whenever the test
fails. With `yield`, pytest runs the code after the `yield` as
teardown even if the test raises an exception.

Shows: the difference between `return` and `yield` in pytest fixtures
and why `yield` is necessary for reliable cleanup.

To find it: after the test fails, list the files in the working
directory. If the temp file is still present, cleanup did not
run. Change `return path` to `yield path` in the fixture and add
`os.remove(path)` after the `yield`, then rerun to confirm the file is
removed.

</details>

## Test a registry that stores and retrieves entries {: #testing-orderdep}

Run `pytest test_orderdep.py -v`. Both tests pass. Now run
`pytest test_orderdep.py::test_lookup -v` to run only the second
test. What happens?

[% inc test_orderdep.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `test_lookup` relies on `test_register` having
populated `_registry` first. When `test_lookup` runs alone or in a
different order, `_registry` is empty and the test raises a
`KeyError`.

Shows: why each test must set up its own state independently rather
than relying on side effects from other tests, and how to use fixtures
to provide shared setup.

To find it: run `pytest test_orderdep.py::test_lookup -v` alone
without running `test_register` first. If it fails with a `KeyError`,
the test depends on state left by another test.

</details>

## Share a list fixture across multiple tests {: #testing-scopemut}

Run `pytest test_scopemut.py -v`. Which test fails? Reverse the order
of the two tests and run again. Does the other test now fail?

[% inc test_scopemut.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `scope="session"` on a fixture that returns a mutable
list. A session-scoped fixture is created once and reused across every
test in the run, so mutations made by one test are visible to all
later tests.

Shows: the difference between fixture scopes, why mutable objects
should use function scope (the default) rather than session scope, and
how fixture scope bugs often appear only when tests are run in a
particular order.

To find it: reverse the order of the tests in the file and run
again. If a different test now fails, the tests are sharing state
through the fixture. Check the fixture for a `scope=` argument:
`"session"` means one instance is shared across the entire run.

</details>

## Test that a function raises an error on bad input {: #testing-deadassert}

Run `pytest test_deadassert.py -v`. The test passes. Add a
`print("reached")` on the line after `result = parse_positive(0)`. Run
again. Is the print executed?

[% inc test_deadassert.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is placing an assertion inside a `with pytest.raises()` block
after the line that raises. Once `parse_positive(0)` raises
`ValueError`, execution jumps to the end of the `with` block and the
assertion is never reached. The test passes because the exception was
raised as expected, but the assertion that was supposed to check a
return value is silently skipped.

Shows: that assertions on return values must be placed after the
`with pytest.raises()` block, not inside it.

To find it: add `print("reached")` on the line immediately after the
raising call, inside the `with` block. Run the test: if the print
never appears, execution never reached that line. Move the assertion
to after the `with` block.

</details>

## Test a function with an unreachable assertion {: #testing-unreachable}

Run `pytest test_unreachable.py -v`. Does the test pass? Does it
actually exercise all three branches of `classify`?

[% inc test_unreachable.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a bare `return` in the middle of `test_classify`. It exits
the test before the assertions for the `"zero"` and `"positive"` cases
run, so only the first branch is ever checked and the test always
passes.

Shows: how an early `return` silently truncates a test and why
coverage tools flag branches that no assertion ever reaches.

To find it: add `print("after return")` on the line after the `return`.
It never prints. Remove the `return` so every assertion runs.

</details>

## Test that the right error message is raised {: #testing-raisematch}

Run `pytest test_raisematch.py -v`. Does the test pass? Which
`ValueError` message did `parse_count("abc")` actually raise — the one
the test intended?

[% inc test_raisematch.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `pytest.raises(ValueError)` without a `match=` argument. It
checks only the exception type, not the message, so a `ValueError`
raised for a different reason ("count must be an integer") passes a
test that intended to check "count cannot be None".

Shows: that `match=` pins a test to the specific message, and why
checking the type alone can let the wrong failure through.

To find it: print the caught exception with
`with pytest.raises(ValueError) as exc: ...; print(exc.value)`. Add
`match="cannot be None"` and rerun to confirm the test now fails for
the wrong input.

</details>

## Test a function that writes JSON to a file {: #testing-tmpfile}

Run `pytest test_tmpfile.py -v`. The test passes. After it finishes,
list the files in your working directory. What file was left behind?

[% inc test_tmpfile.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is opening `"output.json"` as a plain filename, which creates
the file in the current working directory. The file is not deleted
when the test finishes, so subsequent runs may read stale data, and
different tests that use the same filename can interfere with each
other.

Shows: how to use the `tmp_path` fixture, which provides a per-test
temporary directory that pytest removes automatically after each run.

To find it: list the files in the working directory after the test
suite finishes.  If `output.json` is present, the test wrote to the
current directory rather than a temporary one. Use the `tmp_path`
fixture to get a per-test directory that pytest cleans up
automatically.

</details>
