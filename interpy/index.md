# Intermediate Python

## Reverse a sequence for display {: #interpy-alias}

Call the function and then print both the original list and the returned value.
Has the original list changed?

[% inc alias.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `list.reverse()` (which mutates in place) instead of `reversed()`
or slicing, so the original list is also reversed after the call.

Shows: aliasing and the difference between in-place and copy
operations.

To find it: print `id(original_list)` before the call and `id(returned_list)` after.
If both print the same number, the function returned the same object rather than a
copy, and reversing it also mutated the original.

</details>

## Track items added to each shopping cart {: #interpy-sharemut}

Create two account objects, add different transactions to each, and then print the
transaction history of each. Does each account show only its own transactions?

[% inc sharemut.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `history = []` is defined at class level, so all instances share the
same list object instead of each having their own, and every account's transactions
appear in every other account.

Shows: the difference between shared mutable class attributes and
per-instance attributes initialized in `__init__`.

To find it: create two accounts, add one transaction to the first and a different one
to the second, then print `account1.history` and `account2.history`. If both lists
contain both transactions, confirm the sharing with `print(Account.history is
account1.history)` — it will print `True`.

</details>

## Check whether a running total hits a target {: #interpy-fpeq}

Run this script and examine the two computed values. Are they exactly equal? Try
printing each value with many decimal places.

[% inc fpeq.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `==` on floats computed by different routes, so the comparison
returns `False` even when the values should be equal.

Shows: floating-point representation errors and how to use
`math.isclose`.

To find it: print both values with 20 decimal places using `f"{val:.20f}"`. You will
see that one ends in `...000001` rather than matching the other exactly, revealing
the rounding difference that makes `==` return `False`.

</details>

## Load settings from a configuration file {: #interpy-broad}

Run the scraper with the provided URL list, which includes one malformed URL. Does
it process all the valid URLs? Check whether anything is silently discarded.

[% inc broad.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is wrapping the fetch-and-parse loop in `try/except Exception: pass` to
tolerate network timeouts. The `ValueError` raised by the URL parser is also caught
and discarded, so the scraper silently stops processing after the first malformed
URL.

Shows: how overly broad exception handlers swallow unrelated bugs, and
how to use `logging.exception` to record errors instead of ignoring
them.

To find it: replace `pass` in the `except` block with `logging.exception("caught")`.
Run the script again and read the log output. You will see a `ValueError` from the
URL parser printed for the malformed URL, proving the `except` block was swallowing
the wrong exception type.

</details>

## Read addresses from a spreadsheet export {: #interpy-commas}

Run the script with the provided CSV file and read the traceback. Which line in the
file triggers the error? Examine that line carefully.

[% inc commas.py scrub="\s*# BUG.*" %]
[% inc commas.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that names containing a comma (e.g., "Smith, John") cause
`line.split(',')` to produce three fields instead of two, so the index used for the
score points at the wrong element and the script crashes with an `IndexError`.

Shows: why hand-rolled CSV parsing fails on real data and when to use
the `csv` module.

To find it: open the CSV in a text editor and find the row that triggers the
`IndexError`. Count the commas on that line — there are two, not one. The extra
comma sits inside a quoted name field that `line.split(',')` does not recognize as
quoted.

</details>

## Rank files by version number {: #interpy-lexisort}

Run the sort function and examine the output order. Where does `file10` appear
relative to `file2`?

[% inc lexisort.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using the default `sort()`, which gives lexicographic order and places
`file10` before `file2`.

Shows: the difference between lexicographic and numeric sort order and
how to write a `key` function that extracts the embedded integer so
the files sort as `file1`, `file2`, `file10`.

To find it: run the sort and search for `file10` in the output. It appears
immediately after `file1`, before `file2`. That placement is the signature of
alphabetical order, where `"10" < "2"` because `"1" < "2"` at the first character.

</details>

## Process a pipeline of records twice {: #interpy-exhaust}

Run the script and look at both outputs. Does each one produce the values you
expected?

[% inc exhaust.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that generators are exhausted after one pass, so the second use of the
generator in the same expression produces no results.

Shows: that generators are single-use iterators and when to use lists
instead.

To find it: print `type(pipeline)` to confirm it is a generator. Then assign
`results = list(pipeline)` and print `results` a second time — the second access
returns an empty list, proving the generator was exhausted on the first pass.

</details>

## Cache results of an expensive calculation {: #interpy-cachekey}

Call the cached function twice with the same positional argument but a different
keyword argument each time. Do both calls return the correct result?

[% inc cachekey.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the cache key does not include all function arguments (e.g., ignores
keyword arguments), so the decorator returns the same result for different inputs.

Shows: how to construct correct cache keys and test with varied
inputs.

To find it: call the cached function twice with the same positional argument but
different keyword arguments — e.g., `f(1, multiplier=2)` then `f(1, multiplier=3)`.
If both return the same value, add `print(key)` inside the decorator to show the
key is identical for both calls.

</details>

## Extend a base class with new attributes {: #interpy-super}

Create an instance of the subclass and try to access an attribute that is set in
the parent's `__init__`. Does it exist?

[% inc super.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is forgetting `super().__init__()`, so the parent's `__init__` is never
called and required attributes are missing when a subclass method tries to use them.

Shows: Python's method resolution order and how to use `super()`
correctly.

To find it: instantiate the subclass and immediately try to access a parent-defined
attribute. The `AttributeError` names the missing attribute. Search the subclass
`__init__` for a call to `super().__init__()` — its absence is the cause.

</details>

## Write results to disk when processing fails {: #interpy-unclosed}

Run the script so that it raises an exception part-way through writing. Then open
the output file. Does it contain complete data?

[% inc unclosed.py scrub="\s*# BUG.*" %]
[% inc unclosed.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `open()` without a `with` statement. When an unhandled exception
occurs midway through, the output file is left partially written because the write
buffer is never flushed and `close()` is never called.

Shows: why context managers guarantee file cleanup even when
exceptions occur, and how to use `with open(…) as f` to prevent data
loss.

To find it: run the script so that it raises an exception midway through writing,
then open the output file in a text editor. Count the records. If the count is less
than expected, the buffer was never flushed — `close()` was never called because the
exception skipped it.

</details>
