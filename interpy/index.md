# Intermediate Python

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

## Scrape titles from a list of URLs {: #interpy-broad}

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

## Find the top scorer in a CSV file {: #interpy-commas}

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

## Build a list of functions in a loop {: #interpy-latebind}

Call each function in the list produced by `make_multipliers()`. Do they multiply by
different numbers?

[% inc latebind.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is late binding. Each lambda captures the *variable* `i`, not the value it
had when the lambda was created. By the time any lambda is called, the loop has
finished and `i` is 4, so every lambda multiplies by 4.

Shows: that closures capture variables, not values, and why a loop that creates
functions needs a way to freeze the current value (e.g. a default argument
`lambda x, i=i: x * i`).

To find it: print what each function returns — they all return the same value.
Capture the value with `lambda x, i=i: x * i`.

</details>

## Update a variable in an enclosing function {: #interpy-nonlocal}

Call the counter returned by `make_counter()`. Does it return 1?

[% inc nonlocal.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is assigning to `count` without declaring it `nonlocal`. Any assignment to a
name inside a function makes that name local, so `count = count + 1` tries to read a
local `count` before it exists and raises `UnboundLocalError`.

Shows: Python's scoping rules (LEGB) and that `nonlocal` (or `global`) is required to
assign to a variable from an enclosing scope.

To find it: the traceback says `UnboundLocalError: local variable 'count' referenced
before assignment`. Add `nonlocal count` as the first line of `increment`.

</details>

## Preserve a function's name and docstring {: #interpy-wraps}

Inspect `add.__name__` and `add.__doc__` after decorating it. Do they match the
original function?

[% inc wraps.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the missing `@functools.wraps(func)` on the wrapper. Without it, the
decorator returns a function named `wrapper` with no docstring, so `help()`,
`repr()`, and introspection tools report the wrong metadata.

Shows: how decorators replace the original function object, and why `functools.wraps`
is needed to copy `__name__`, `__doc__`, and other attributes to the wrapper.

To find it: print `add.__name__` — it shows `wrapper`, not `add`. Add
`@functools.wraps(func)` above the wrapper function.

</details>

## Pair up two lists of different lengths {: #interpy-ziplen}

Pair a list of three names with a list of two scores. Does every name get a score?

[% inc ziplen.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `zip` stops at the shorter iterable. When the two lists have different
lengths, `zip` silently drops the extra items from the longer one, so the last name is
missing from the result.

Shows: that `zip` truncates to the shortest input, and when mismatched lengths matter
use `itertools.zip_longest` (with a fill value) instead.

To find it: compare `len(names)` and `len(scores)` to the number of pairs returned.
The count is 2, not 3. Use `itertools.zip_longest(names, scores)` to keep all names.

</details>
