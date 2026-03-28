# Data, I/O, and Testing

## Read a contact list from a CSV export {: #diot-quotecsv}

Run the parser with the provided CSV file. Do all rows produce the correct number
of fields? Pay particular attention to rows that contain commas.

[% inc quotecsv.py scrub="\s*# BUG.*" %]
[% inc quotecsv.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `line.split(',')` instead of the `csv` module, so rows that contain
commas inside quoted fields are split incorrectly.

Shows: why hand-rolled parsers fail on real-world data and when to use
standard library tools.

To find it: print `len(fields)` for each row as you parse. When it prints `3` instead
of `2`, find that row in the CSV and count the commas — the extra one is inside a
quoted field that `line.split(',')` does not recognize as quoted.

</details>

## Benchmark an image processing function {: #diot-walltime}

Run the benchmarking function several times and examine the elapsed time values.
Do any of them look unusual?

[% inc walltime.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `time.time()` without accounting for system clock adjustments, so
the function reports negative durations when the clock is set back.

Shows: the difference between wall time and monotonic time and when to
use `time.monotonic`.

To find it: print each start and end timestamp as a float alongside the computed
elapsed time. A negative elapsed value proves the end timestamp was smaller than the
start, which happens when the system clock is stepped backward by NTP or a VM
snapshot restore.

</details>

## Schedule a recurring task across time zones {: #diot-daylight}

Call the date arithmetic function with a date near a daylight saving transition.
Compare the result from the naive datetime path with the result from the
timezone-aware path.

[% inc daylight.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is adding a `timedelta` to a naive datetime, so the function produces results
that are off by one day around daylight saving time transitions.

Shows: the difference between naive and timezone-aware datetimes.

To find it: call the function with `datetime(2024, 3, 10)` — the Sunday US clocks
spring forward — and add one day. Print the naive result and the timezone-aware
result side by side. The naive version may report the wrong date because it adds
exactly 86,400 seconds without accounting for the 23-hour day.

</details>

## Scrape prices from a product page {: #diot-missparse}

Run the script with the provided HTML file and check whether it finds all the
expected elements. What happens when an element is not found?

[% inc missparse.py scrub="\s*# BUG.*" %]
[% inc missparse.html %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the HTML structure varies and the selector matches zero elements
without raising an error, so the script fails silently on some pages.

Shows: how to handle missing data in HTML parsing and use assertions
to catch unexpected input.

To find it: print `len(soup.select(selector))` before accessing the first element.
Seeing `0` tells you the selector matched nothing. Then print the first hundred
characters of `str(soup)` to confirm whether the expected element is actually present
in the HTML.

</details>

## Extract phone numbers from a text file {: #diot-overexp}

Test the regular expression against a few valid email addresses and a few strings
that look like email addresses but are not. Does it reject the invalid ones?

[% inc overexp.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a pattern that is too permissive (e.g., missing anchors or character
class constraints), so the regular expression also matches invalid strings.

Shows: how to test regular expressions with both valid and invalid
inputs.

To find it: test the regular expression against known-invalid strings such as
`"not_an_email"` or `"two@@signs.com"`. If `re.fullmatch` returns a match object
instead of `None` for either, the pattern is too permissive.

</details>

## Write a test for a data validation function {: #diot-noassert}

Run the test suite. Does it pass? Now deliberately break the function the test is
testing. Does the test still pass?

[% inc noassert.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the test calls the function but never asserts anything about the
result, so it always passes even when the function is broken.

Shows: that a test with no assertions is not a test and how to write
assertions correctly.

To find it: modify the function under test to return an obviously wrong value, such
as `return None`. Run the test suite again. If the test still passes, it contains
no assertion that can detect the wrong return value.

</details>

## Test a function that modifies a global registry {: #diot-shared}

Run each test on its own. Then run both together. Do you get the same results both
ways?

[% inc shared.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that one test modifies a module-level variable that another test depends
on, so the suite passes in isolation but fails when run together.

Shows: test isolation, teardown, and the risks of shared global state.

To find it: run `pytest test.py::test_first -v` alone, then run
`pytest test.py::test_second -v` alone. If each passes in isolation but one fails
when both run together, the failing test depends on state left by the other.

</details>

## Load a reference data file in a test {: #diot-abspath}

Run the script from a different working directory than the one where the script
file is saved. Does it find its configuration file?

[% inc abspath.py scrub="\s*# BUG.*" %]
[% inc abspath.json %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using a hardcoded absolute path instead of a path relative to the
script's location, so the function behaves differently on different machines.

Shows: the difference between `__file__`-relative and
working-directory-relative paths.

To find it: run the script from a different directory — e.g., `cd /tmp && python
/full/path/to/script.py`. It will fail to open the config file. Print `os.getcwd()`
inside the script to confirm that `open("config.json")` resolves relative to `/tmp`,
not to the script's own directory.

</details>

## Save a record with a timestamp to a file {: #diot-jsondate}

Run the script and read the error message. Which value in the data structure cannot
be serialized?

[% inc jsondate.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the data contains `datetime` objects, which are not
JSON-serializable, so the program raises an error when writing output.

Shows: how to identify serialization errors and write custom JSON
encoders.

To find it: read the `TypeError` message — `Object of type datetime is not JSON
serializable`. Then search the data structure being serialized for any `datetime`
object: `print(type(record['timestamp']))` will show `<class 'datetime.datetime'>`.

</details>

## Add diagnostic output to a data pipeline {: #diot-loglevel}

Run the script and then look at the log file. Are the messages you expected to see
present?

[% inc loglevel.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the log level is set to `WARNING` but the calls use
`logger.debug()`, so the messages never appear in the log file.

Shows: how Python's logging hierarchy works and how to verify the
effective log level.

To find it: add `print(logger.getEffectiveLevel())` near the top of the script. The
output `30` means the effective level is `WARNING` (30), and `DEBUG` messages require
level `10`. Either lower the level to `DEBUG` or upgrade the calls to `logger.warning()`.

</details>
