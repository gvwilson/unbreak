# Data, I/O, and Testing

## Quoted Fields in CSV Parsing {: #diot-quotecsv}

[% inc quotecsv.py scrub="\s*# BUG.*" %]

A CSV-parsing function misreads rows that contain commas inside quoted fields;
the bug is using `line.split(',')` instead of the `csv` module. Teaches why
hand-rolled parsers fail on real-world data and when to use standard library tools.

## Wall Time vs. Monotonic Time {: #diot-walltime}

[% inc walltime.py scrub="\s*# BUG.*" %]

A function that measures elapsed time reports negative durations when the clock
wraps; the bug is using `time.time()` without accounting for system clock
adjustments. Teaches the difference between wall time and monotonic time and when
to use `time.monotonic`.

## Naive Datetime and Daylight Saving {: #diot-daylight}

[% inc daylight.py scrub="\s*# BUG.*" %]

A date-arithmetic function produces results that are off by one day around daylight
saving time transitions; the bug is adding a `timedelta` to a naive datetime.
Teaches the difference between naive and timezone-aware datetimes.

## Missing Elements in HTML Parsing {: #diot-missparse}

[% inc missparse.py scrub="\s*# BUG.*" %]

A script that downloads a web page and parses it for prices fails silently on some
pages; the bug is that the HTML structure varies and the selector matches zero
elements without raising an error. Teaches how to handle missing data in HTML
parsing and use assertions to catch unexpected input.

## Overly Permissive Regular Expression {: #diot-overexp}

[% inc overexp.py scrub="\s*# BUG.*" %]

A regular expression meant to extract email addresses also matches invalid strings;
the bug is a pattern that is too permissive (e.g., missing anchors or character
class constraints). Teaches how to test regular expressions with both valid and
invalid inputs.

## Test with No Assertions {: #diot-noassert}

[% inc noassert.py scrub="\s*# BUG.*" %]

A unit test always passes even when the function is broken; the bug is that the
test calls the function but never asserts anything about the result. Teaches that
a test with no assertions is not a test and how to write assertions correctly.

## Shared State Between Tests {: #diot-shared}

[% inc shared.py scrub="\s*# BUG.*" %]

A test suite that passes in isolation fails when run together; the bug is that one
test modifies a module-level variable that another test depends on. Teaches test
isolation, teardown, and the risks of shared global state.

## Hardcoded Absolute Path {: #diot-abspath}

[% inc abspath.py scrub="\s*# BUG.*" %]

A function that reads a configuration file behaves differently on different
machines; the bug is using a hardcoded absolute path instead of a path relative
to the script's location. Teaches the difference between `__file__`-relative and
working-directory-relative paths.

## Unserializable Datetime in JSON {: #diot-jsondate}

[% inc jsondate.py scrub="\s*# BUG.*" %]

A program writes JSON output that cannot be parsed back in; the bug is that the
data contains `datetime` objects, which are not JSON-serializable. Teaches how
to identify serialization errors and write custom JSON encoders.

## Wrong Logging Level {: #diot-loglevel}

[% inc loglevel.py scrub="\s*# BUG.*" %]

A logging call that should record errors never appears in the log file; the bug is
that the log level is set to `WARNING` but the calls use `logger.debug()`. Teaches
how Python's logging hierarchy works and how to verify the effective log level.
