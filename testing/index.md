# Testing

## Write a test for a totaling function {: #testing-vacuous}

Run `pytest test_vacuous.py -v`. Does the test pass? Add a print
statement inside `test_total` to confirm that `result` is being
computed. Does a passing test mean the function is correct?

[% inc test_vacuous.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the test contains no assertion, so pytest has nothing
to check and always reports it as passing. A vacuous test gives false
confidence: the function could return any value and the test would
still pass.

Shows: that every test must contain at least one assertion that can
actually fail.

To find it: modify the function to return an obviously wrong value,
such as returning `0` regardless of input, then rerun the test. If it
still passes, the test has no assertion and is not checking anything.

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

## Test a running total function {: #testing-floatequal}

Run `pytest test_floatequal.py -v`. Read the assertion error
carefully. What value did `running_total` actually return?

[% inc test_floatequal.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is comparing floating-point results with `==`. Repeated
addition accumulates rounding error in IEEE 754 arithmetic, so
`0.1 + 0.2 + 0.3` produces `0.6000000000000001`, not `0.6`.

Shows: how to use `pytest.approx` to compare floats within a
tolerance, and why exact equality between computed floats is
unreliable.

To find it: print `f"{result:.20f}"` in the test before the
assertion. If the last few digits are not all zeros, rounding error
has accumulated. Replace `assert result == expected` with
`assert result == pytest.approx(expected)`.

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

## Test a string prefix-stripping function {: #testing-missingreturn}

Run `pytest test_missingreturn.py -v`. Read the assertion error. What
value did `strip_prefix` return? Is that what you expected from the
code?

[% inc test_missingreturn.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a missing `return` in `strip_prefix`. The slicing
expression computes the correct substring but discards it, so the
function returns `None`. The test then compares `None == "disk full"`
and fails.

Shows: how to recognise a missing `return` from a `None` assertion
error and how to check function return values as a first step when a
test fails unexpectedly.

To find it: print `result` in the test before the assertion. If it
prints `None`, the function did not return a value. Read the function
and find the branch that computes the answer but has no `return`
statement.

</details>

## Test a function that returns a sorted list {: #testing-paramtype}

Run `pytest test_paramtype.py -v`. All three cases fail. Read the
assertion error for the first case. What value did `result` have?

[% inc test_paramtype.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `values.sort()` and assigning its return
value. `list.sort()` sorts the list in place and returns `None`; the
sorted result is in `values`, not in `result`. The assertion then
compares `None` against the expected list and fails.

Shows: the difference between `list.sort()` (in-place, returns `None`)
and `sorted()` (returns a new sorted list), and how parametrize makes
the pattern of failure visible across multiple inputs at once.

To find it: print `result` inside the test for the first failing
case. If `result` is `None`, the function returned `None` instead of a
list. Check whether the function calls `list.sort()`, which returns
`None`, or `sorted()`, which returns a new sorted list.

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
