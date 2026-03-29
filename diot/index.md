# Data, I/O, and Testing

## Quoted Fields in CSV Parsing {: #diot-quotecsv}

Run the parser with the provided CSV file. Do all rows produce the correct number
of fields? Pay particular attention to rows that contain commas.

[% inc quotecsv.py scrub="\s*# BUG.*" %]
[% inc quotecsv.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A CSV-parsing function misreads rows that contain commas inside quoted fields;
the bug is using `line.split(',')` instead of the `csv` module. Teaches why
hand-rolled parsers fail on real-world data and when to use standard library tools.

</details>

## Wall Time vs. Monotonic Time {: #diot-walltime}

Run the benchmarking function several times and examine the elapsed time values.
Do any of them look unusual?

[% inc walltime.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A function that measures elapsed time reports negative durations when the clock
wraps; the bug is using `time.time()` without accounting for system clock
adjustments. Teaches the difference between wall time and monotonic time and when
to use `time.monotonic`.

</details>

## Naive Datetime and Daylight Saving {: #diot-daylight}

Call the date arithmetic function with a date near a daylight saving transition.
Compare the result from the naive datetime path with the result from the
timezone-aware path.

[% inc daylight.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A date-arithmetic function produces results that are off by one day around daylight
saving time transitions; the bug is adding a `timedelta` to a naive datetime.
Teaches the difference between naive and timezone-aware datetimes.

</details>

## Missing Elements in HTML Parsing {: #diot-missparse}

Run the script with the provided HTML file and check whether it finds all the
expected elements. What happens when an element is not found?

[% inc missparse.py scrub="\s*# BUG.*" %]
[% inc missparse.html %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that downloads a web page and parses it for prices fails silently on some
pages; the bug is that the HTML structure varies and the selector matches zero
elements without raising an error. Teaches how to handle missing data in HTML
parsing and use assertions to catch unexpected input.

</details>

## Overly Permissive Regular Expression {: #diot-overexp}

Test the regular expression against a few valid email addresses and a few strings
that look like email addresses but are not. Does it reject the invalid ones?

[% inc overexp.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A regular expression meant to extract email addresses also matches invalid strings;
the bug is a pattern that is too permissive (e.g., missing anchors or character
class constraints). Teaches how to test regular expressions with both valid and
invalid inputs.

</details>

## Test with No Assertions {: #diot-noassert}

Run the test suite. Does it pass? Now deliberately break the function the test is
testing. Does the test still pass?

[% inc noassert.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A unit test always passes even when the function is broken; the bug is that the
test calls the function but never asserts anything about the result. Teaches that
a test with no assertions is not a test and how to write assertions correctly.

</details>

## Shared State Between Tests {: #diot-shared}

Run each test on its own. Then run both together. Do you get the same results both
ways?

[% inc shared.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A test suite that passes in isolation fails when run together; the bug is that one
test modifies a module-level variable that another test depends on. Teaches test
isolation, teardown, and the risks of shared global state.

</details>

## Hardcoded Absolute Path {: #diot-abspath}

Run the script from a different working directory than the one where the script
file is saved. Does it find its configuration file?

[% inc abspath.py scrub="\s*# BUG.*" %]
[% inc abspath.json %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A function that reads a configuration file behaves differently on different
machines; the bug is using a hardcoded absolute path instead of a path relative
to the script's location. Teaches the difference between `__file__`-relative and
working-directory-relative paths.

</details>

## Unserializable Datetime in JSON {: #diot-jsondate}

Run the script and read the error message. Which value in the data structure cannot
be serialized?

[% inc jsondate.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A program writes JSON output that cannot be parsed back in; the bug is that the
data contains `datetime` objects, which are not JSON-serializable. Teaches how
to identify serialization errors and write custom JSON encoders.

</details>

## Wrong Logging Level {: #diot-loglevel}

Run the script and then look at the log file. Are the messages you expected to see
present?

[% inc loglevel.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A logging call that should record errors never appears in the log file; the bug is
that the log level is set to `WARNING` but the calls use `logger.debug()`. Teaches
how Python's logging hierarchy works and how to verify the effective log level.

</details>
