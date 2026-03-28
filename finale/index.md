# Conclusion

<p class="subtitle">looking back and next steps</p>

Every exercise in this book uses one or more of the following tactics
to locate a bug.

## General

1. Read a traceback from bottom to top: the last frame names the line that raised
   the error; the frames above it show what triggered that line. The error message
   on the final line is often enough — read it before scrolling up.
2. Run the code with the smallest input you can verify entirely by hand, then
   check every output value against your manual calculation. Five items and a
   window of three beats a thousand items every time.
3. Binary-search the bug: comment out half the suspect code and check whether the
   problem persists. If it does, the bug is in the half that remains; if it
   disappears, the bug is in the half you removed. Repeat until one line is left.
4. Add `print("entered function_name")` at the top of every function or method
   you suspect, so you can see which ones actually run and in what order.
5. Call a function twice with identical arguments and compare both return values.
   If they differ, the function has hidden state that changes between calls.

## Inspecting values

6. Print `type(value)` when a comparison unexpectedly fails. A mismatch between
   `str` and `int`, or between a plain number and a NumPy scalar, explains why
   `==` returns `False` or raises `TypeError`.
7. Print `repr(value)` to reveal invisible characters such as trailing spaces,
   embedded newlines, or a `\r` that looks identical to nothing in plain `print`
   output but breaks every string comparison.
8. Print `vars(obj)` to see exactly which attributes an object has stored. An
   empty dictionary after construction means `__init__` never assigned anything
   to `self`; a misspelled key means the attribute was stored under a different
   name than the one being read.
9. Print `id(a)` and `id(b)` when two names that should be independent seem
   linked. The same number means they point to the same object in memory, which
   explains why modifying one changes the other.

## Contracts and exceptions

10. Check that the return type matches what the caller expects. Python's special
    methods have exact contracts: `__str__` and `__repr__` must return `str`,
    `__len__` must return a non-negative `int`, `__bool__` must return `bool` or
    `int`, and `__init__` must return `None`. Returning the wrong type raises
    `TypeError` with a message that names the method.
11. Replace a broad `except Exception: pass` or bare `except: pass` with
    `logging.exception("caught")` to see the actual exception type and message
    being swallowed. Silent failure is almost never the right choice.
12. Introduce a deliberate bug in the code under test, then rerun the test suite.
    If the tests still pass, no assertion is checking the output that matters.
13. Run each test in isolation with `pytest path/test_file.py::test_name` to
    verify it does not depend on another test having run first.
14. Add `print("mock was called")` as the first line of a mock or patch to
    confirm it is actually intercepting the real call instead of leaving the
    original in place.

## Data and pipelines

15. Check the exact stored values in a column before writing a filter, e.g.,
    use `SELECT DISTINCT col` in SQL or `.unique()` in a dataframe to confirm the
    literal strings or numbers the data actually contains, including leading or
    trailing spaces.
16. Count rows before and after each transformation step to detect rows that were
    silently dropped, duplicated, or merged incorrectly.
17. Insert `.collect()` after each step in a lazy query pipeline to pin down
    which transformation is raising an error, rather than getting a single
    traceback from the final collect.

## Performance

18. Run `python -m cProfile -s cumulative script.py | head -20` to find the
    slow function instead of guessing. The cumulative column shows where time
    actually accumulates, which is rarely where intuition points.

## Browser and frontend

19. Open the browser's Network tab before reproducing the bug, then reload: the
    tab records every request, its status code, the request headers, and the
    response body. Check the Console tab for JavaScript errors at the same time.
20. When a CSS rule seems to have no effect, open DevTools, select the element,
    and look at the Styles panel. A strikethrough means the declaration was
    overridden by a more specific rule; a warning triangle means the value is
    invalid and was silently discarded.
21. Check the HTTP status code before parsing the response body: a `404` or
    `422` response usually returns HTML or a JSON error object, not the data
    you expected, so the parse error is a symptom and the status code is the cause.

## Shell

22. Echo or print the exact string a shell command receives before running it on
    real data; use `echo "$var"` to check variable contents, or replace a
    command with `echo` to preview what the shell will execute without side effects.
23. Sketch the directory tree on paper and count levels before running a command
    that uses a relative path such as `../..`, since one extra or missing `..` quietly
    reads or writes the wrong directory.

## Patterns

24. Test a regular expression against known-invalid inputs, not just valid ones,
    to verify the pattern rejects what it should. A pattern that matches
    everything is not the same as a pattern that matches the right things.
