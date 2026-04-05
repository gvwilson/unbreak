# Testing

## Test with No Assertion {: #testing-vacuous}

Run `pytest test_vacuous.py -v`. Does the test pass? Add a print statement inside
`test_total` to confirm that `result` is being computed. Does a passing test mean
the function is correct?

[% inc test_vacuous.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the test contains no assertion, so pytest has nothing to check and
always reports it as passing. A vacuous test gives false confidence: the function
could return any value and the test would still pass. Shows that every test must
contain at least one assertion that can actually fail.

</details>

## Tuple Is Always Truthy {: #testing-tupleassert}

Run `pytest test_tupleassert.py -v`. Does the test pass? What value does `double(4)`
actually return? Check the pytest warning in the output.

[% inc test_tupleassert.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `assert (result, expected)`, which creates a two-element tuple. A
non-empty tuple is always truthy, so the assertion never fails regardless of whether
`result == expected`. The correct form is `assert result == expected` without the
enclosing parentheses. Shows how easy it is to write an assertion that looks
plausible but is logically vacuous, and why pytest's warning about this pattern
should not be ignored.

</details>

## Floating-Point Equality {: #testing-floatequal}

Run `pytest test_floatequal.py -v`. Read the assertion error carefully. What value
did `running_total` actually return?

[% inc test_floatequal.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is comparing floating-point results with `==`. Repeated addition accumulates
rounding error in IEEE 754 arithmetic, so `0.1 + 0.2 + 0.3` produces
`0.6000000000000001`, not `0.6`. Shows how to use `pytest.approx` to compare
floats within a tolerance, and why exact equality between computed floats is
unreliable.

</details>

## pytest.raises Catches the Wrong Exception {: #testing-broadexc}

Run `pytest test_broadexc.py -v`. Does the test pass? What exception does
`parse_count(None)` actually raise? Is that the exception the test intended to check?

[% inc test_broadexc.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `pytest.raises(Exception)`, which accepts any exception, including
`TypeError`. The test passes even though `parse_count` raises a `TypeError` rather
than the expected `ValueError`, masking a bug in the function. Shows how to use a
specific exception type in `pytest.raises` and why catching the base `Exception`
class in tests hides incorrect behaviour.

</details>

## Fixture with No Cleanup {: #testing-noyield}

Run `pytest test_noyield.py -v`. The test fails. After it fails, check whether the
temp file still exists. Then change `return path` to `yield path` and add
`os.remove(path)` after the yield. Run again and check the filesystem.

[% inc test_noyield.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `return` in a fixture that needs to perform cleanup. With `return`,
there is no way to run code after the test finishes, so the temp file is left on disk
whenever the test fails. With `yield`, pytest runs the code after the `yield` as
teardown even if the test raises an exception. Shows the difference between
`return` and `yield` in pytest fixtures and why `yield` is necessary for reliable
cleanup.

</details>

## Test Depends on Execution Order {: #testing-orderdep}

Run `pytest test_orderdep.py -v`. Both tests pass. Now run
`pytest test_orderdep.py::test_lookup -v` to run only the second test. What happens?

[% inc test_orderdep.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `test_lookup` relies on `test_register` having populated `_registry`
first. When `test_lookup` runs alone or in a different order, `_registry` is empty
and the test raises a `KeyError`. Shows why each test must set up its own state
independently rather than relying on side effects from other tests, and how to use
fixtures to provide shared setup.

</details>

## Mutable Session-Scoped Fixture {: #testing-scopemut}

Run `pytest test_scopemut.py -v`. Which test fails? Reverse the order of the two
tests and run again. Does the other test now fail?

[% inc test_scopemut.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `scope="session"` on a fixture that returns a mutable list. A session-scoped
fixture is created once and reused across every test in the run, so mutations made by
one test are visible to all later tests. Shows the difference between fixture
scopes, why mutable objects should use function scope (the default) rather than
session scope, and how fixture scope bugs often appear only when tests are run in a
particular order.

</details>

## Assertion After the Raising Call Is Dead Code {: #testing-deadassert}

Run `pytest test_deadassert.py -v`. The test passes. Add a `print("reached")` on
the line after `result = parse_positive(0)`. Run again. Is the print executed?

[% inc test_deadassert.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is placing an assertion inside a `with pytest.raises()` block after the line
that raises. Once `parse_positive(0)` raises `ValueError`, execution jumps to the
end of the `with` block and the assertion is never reached. The test passes because
the exception was raised as expected, but the assertion that was supposed to check a
return value is silently skipped. Shows that assertions on return values must be
placed after the `with pytest.raises()` block, not inside it.

</details>

## Missing Return in Tested Function {: #testing-missingreturn}

Run `pytest test_missingreturn.py -v`. Read the assertion error. What value did
`strip_prefix` return? Is that what you expected from the code?

[% inc test_missingreturn.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a missing `return` in `strip_prefix`. The slicing expression computes
the correct substring but discards it, so the function returns `None`. The test then
compares `None == "disk full"` and fails. Shows how to recognise a missing
`return` from a `None` assertion error and how to check function return values as a
first step when a test fails unexpectedly.

</details>

## sort Returns None {: #testing-paramtype}

Run `pytest test_paramtype.py -v`. All three cases fail. Read the assertion error
for the first case. What value did `result` have?

[% inc test_paramtype.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `values.sort()` and assigning its return value. `list.sort()`
sorts the list in place and returns `None`; the sorted result is in `values`, not
in `result`. The assertion then compares `None` against the expected list and fails.
Shows the difference between `list.sort()` (in-place, returns `None`) and
`sorted()` (returns a new sorted list), and how parametrize makes the pattern of
failure visible across multiple inputs at once.

</details>

## Test Writes to the Working Directory {: #testing-tmpfile}

Run `pytest test_tmpfile.py -v`. The test passes. After it finishes, list the files
in your working directory. What file was left behind?

[% inc test_tmpfile.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is opening `"output.json"` as a plain filename, which creates the file in
the current working directory. The file is not deleted when the test finishes, so
subsequent runs may read stale data, and different tests that use the same filename
can interfere with each other. Shows how to use the `tmp_path` fixture, which
provides a per-test temporary directory that pytest removes automatically after
each run.

</details>
