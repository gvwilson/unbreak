# Intermediate Python

## Aliasing and In-Place Reversal {: #interpy-alias}

Call the function and then print both the original list and the returned value.
Has the original list changed?

[% inc alias.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A function is supposed to reverse a list and return the reversed copy, but the
original list is also reversed after the call; the bug is using `list.reverse()`
(mutates in place) instead of `reversed()` or slicing. Teaches aliasing and the
difference between in-place and copy operations.

</details>

## Shared Mutable Class Attribute {: #interpy-sharemut}

Create two account objects, add different transactions to each, and then print the
transaction history of each. Does each account show only its own transactions?

[% inc sharemut.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A class that records the transaction history of a bank account shows every account's
transactions in every other account; the bug is that `history = []` is defined at
class level, so all instances share the same list object instead of each having
their own. Teaches the difference between shared mutable class attributes and
per-instance attributes initialized in `__init__`.

</details>

## Floating-Point Equality {: #interpy-fpeq}

Run this script and examine the two computed values. Are they exactly equal? Try
printing each value with many decimal places.

[% inc fpeq.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A program compares two floating-point results that should be equal but the
comparison returns `False`; the bug is using `==` on floats computed by different
routes. Teaches floating-point representation errors and how to use `math.isclose`.

</details>

## Overly Broad Exception Handler {: #interpy-broad}

Run the scraper with the provided URL list, which includes one malformed URL. Does
it process all the valid URLs? Check whether anything is silently discarded.

[% inc broad.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A web scraper wraps its fetch-and-parse loop in `try/except Exception: pass` to
tolerate network timeouts, but silently stops processing after the first malformed
URL because the `ValueError` raised by the URL parser is also caught and discarded.
Teaches how overly broad exception handlers swallow unrelated bugs, and how to use
`logging.exception` to record errors instead of ignoring them.

</details>

## Commas Inside CSV Fields {: #interpy-commas}

Run the script with the provided CSV file and read the traceback. Which line in the
file triggers the error? Examine that line carefully.

[% inc commas.py scrub="\s*# BUG.*" %]
[% inc commas.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script reads a two-column CSV file of names and scores and reports the top scorer,
but crashes with an `IndexError` on some rows; the bug is that names containing a
comma (e.g., "Smith, John") cause `line.split(',')` to produce three fields instead
of two, so the index used for the score points at the wrong element. Teaches why
hand-rolled CSV parsing fails on real data and when to use the `csv` module.

</details>

## Lexicographic vs. Numeric Sort {: #interpy-lexisort}

Run the sort function and examine the output order. Where does `file10` appear
relative to `file2`?

[% inc lexisort.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A function sorts filenames that contain embedded numbers (e.g., `file2.txt`,
`file10.txt`, `file1.txt`) expecting numeric order, but the default `sort()` gives
lexicographic order, placing `file10` before `file2`. Teaches the difference between
lexicographic and numeric sort order and how to write a `key` function that extracts
the embedded integer so the files sort as `file1`, `file2`, `file10`.

</details>

## Exhausted Generator {: #interpy-exhaust}

Run the script and look at both outputs. Does each one produce the values you
expected?

[% inc exhaust.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A generator function is used twice in the same expression, but the second use
produces no results; the bug is that generators are exhausted after one pass.
Teaches that generators are single-use iterators and when to use lists instead.

</details>

## Incomplete Cache Key {: #interpy-cachekey}

Call the cached function twice with the same positional argument but a different
keyword argument each time. Do both calls return the correct result?

[% inc cachekey.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A caching decorator returns the same result for different inputs; the bug is that
the cache key does not include all function arguments (e.g., ignores keyword
arguments). Teaches how to construct correct cache keys and test with varied inputs.

</details>

## Forgetting `super().__init__()` {: #interpy-super}

Create an instance of the subclass and try to access an attribute that is set in
the parent's `__init__`. Does it exist?

[% inc super.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A subclass calls a method that exists in the parent, but the parent's `__init__`
is never called, leaving required attributes missing; the bug is forgetting
`super().__init__()`. Teaches Python's method resolution order and how to
use `super()` correctly.

</details>

## File Not Closed on Exception {: #interpy-unclosed}

Run the script so that it raises an exception part-way through writing. Then open
the output file. Does it contain complete data?

[% inc unclosed.py scrub="\s*# BUG.*" %]
[% inc unclosed.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A function writes a processed summary to a file using `open()` without a `with`
statement; when an unhandled exception occurs midway through, the output file is
left partially written because the write buffer is never flushed and `close()` is
never called. Teaches why context managers guarantee file cleanup even when
exceptions occur, and how to use `with open(...) as f` to prevent data loss.

</details>
