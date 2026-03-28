# Intermediate Python

## Aliasing and In-Place Reversal {: #interpy-alias}

A function is supposed to reverse a list and return the reversed copy, but the
original list is also reversed after the call; the bug is using `list.reverse()`
(mutates in place) instead of `reversed()` or slicing. Teaches aliasing and the
difference between in-place and copy operations.

## Shared Mutable Class Attribute {: #interpy-sharemut}

A class that records the transaction history of a bank account shows every account's
transactions in every other account; the bug is that `history = []` is defined at
class level, so all instances share the same list object instead of each having
their own. Teaches the difference between shared mutable class attributes and
per-instance attributes initialized in `__init__`.

## Floating-Point Equality {: #interpy-fpeq}

A program compares two floating-point results that should be equal but the
comparison returns `False`; the bug is using `==` on floats computed by different
routes. Teaches floating-point representation errors and how to use `math.isclose`.

## Overly Broad Exception Handler {: #interpy-broad}

A web scraper wraps its fetch-and-parse loop in `try/except Exception: pass` to
tolerate network timeouts, but silently stops processing after the first malformed
URL because the `ValueError` raised by the URL parser is also caught and discarded.
Teaches how overly broad exception handlers swallow unrelated bugs, and how to use
`logging.exception` to record errors instead of ignoring them.

## Commas Inside CSV Fields {: #interpy-commas}

A script reads a two-column CSV file of names and scores and reports the top scorer,
but crashes with an `IndexError` on some rows; the bug is that names containing a
comma (e.g., "Smith, John") cause `line.split(',')` to produce three fields instead
of two, so the index used for the score points at the wrong element. Teaches why
hand-rolled CSV parsing fails on real data and when to use the `csv` module.

## Lexicographic vs. Numeric Sort {: #interpy-lexisort}

A function sorts filenames that contain embedded numbers (e.g., `file2.txt`,
`file10.txt`, `file1.txt`) expecting numeric order, but the default `sort()` gives
lexicographic order, placing `file10` before `file2`. Teaches the difference between
lexicographic and numeric sort order and how to write a `key` function that extracts
the embedded integer so the files sort as `file1`, `file2`, `file10`.

## Exhausted Generator {: #interpy-exhaust}

A generator function is used twice in the same expression, but the second use
produces no results; the bug is that generators are exhausted after one pass.
Teaches that generators are single-use iterators and when to use lists instead.

## Incomplete Cache Key {: #interpy-cachekey}

A caching decorator returns the same result for different inputs; the bug is that
the cache key does not include all function arguments (e.g., ignores keyword
arguments). Teaches how to construct correct cache keys and test with varied inputs.

## Forgetting `super().__init__()` {: #interpy-super}

A subclass calls a method that exists in the parent, but the parent's `__init__`
is never called, leaving required attributes missing; the bug is forgetting
`super().__init__()`. Teaches Python's method resolution order and how to
use `super()` correctly.

## File Not Closed on Exception {: #interpy-unclosed}

A function writes a processed summary to a file using `open()` without a `with`
statement; when an unhandled exception occurs midway through, the output file is
left partially written because the write buffer is never flushed and `close()` is
never called. Teaches why context managers guarantee file cleanup even when
exceptions occur, and how to use `with open(...) as f` to prevent data loss.
