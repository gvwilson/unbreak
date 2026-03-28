# Basic Python

## Off-by-One in Sliding Window {: #basicpy-sliding}

[% inc sliding.py %]

A function that builds all sliding windows of size k over a list returns one fewer
window than expected; the bug is `range(len(data) - k)` instead of
`range(len(data) - k + 1)`, so the last window is never produced. Teaches how to
identify off-by-one errors in index arithmetic and how to verify boundary conditions
with small, hand-checkable examples.

## String Concatenation Instead of Addition {: #basicpy-catadd}

[% inc catadd.py %]

A script reads exam scores from a text file and computes the class average, but
always reports a nonsensical total because the scores are accumulated with
`total = total + line.strip()` (string concatenation) instead of converting each
line to a number first. Teaches the difference between string `+` and numeric `+`,
and how to check the type of a value at runtime using `type()` or `isinstance()`.

## Boolean Logic in Validation {: #basicpy-andor}

[% inc andor.py %]

A function that validates whether a password meets length and character requirements
always rejects valid passwords; the bug is joining the two conditions with `and`
instead of `or` (requiring both to fail simultaneously, which almost never happens).
Teaches how boolean logic errors cause silent misbehavior, and how a small truth
table reveals which operator is correct.

## Misremembered Conversion Formula {: #basicpy-formula}

[% inc formula.py %]

A function converts a geographic coordinate from degrees, minutes, and seconds to
decimal degrees but gives wrong results because it divides seconds by 60 instead of
3600 (a misremembered formula). Teaches how to verify formulas against known values
(e.g., 1°30′0″ = 1.5°) and how to add assertion checks for values that must fall
within a known range.

## In-Place Sort Returns None {: #basicpy-sortnone}

[% inc sortnone.py %]

A script builds a list of squared numbers but the list is always empty; the bug
is calling `list.sort()` (which returns `None`) and assigning the result. Teaches
that many list methods mutate in place and return `None`.

## Misindented Loop State Update {: #basicpy-indent}

[% inc indent.py %]

A function reads lines from a file and counts how many consecutive identical lines
appear in each run, but counts every line as starting a new run; the bug is that
the variable storing the previous line is updated outside (after) the while loop
body due to a missing level of indentation. Teaches how indentation governs control
flow in Python and how to step through a loop mentally to find where state is
updated at the wrong time.

## Missing Return Statement {: #basicpy-noreturn}

[% inc noreturn.py %]

A function filters negative numbers from a list but returns `None`; the bug is a
missing `return` statement (the function builds the result but does not return it).
Teaches that Python functions return `None` by default and how to spot missing
`return` in control flow.

## KeyError in Word Counter {: #basicpy-nokey}

[% inc nokey.py %]

A function tallies word frequencies in a document but crashes with a `KeyError` on
the first new word it encounters because it increments `counts[word]` without first
checking whether the key exists. Teaches defensive dictionary access using
`dict.get(key, 0)` or `collections.defaultdict`, and how to read a `KeyError`
traceback to identify the missing key.

## JSON Integers vs. String Input {: #basicpy-streq}

[% inc streq.py %]

A script reads a list of allowed user IDs from a JSON file and checks whether a
login ID is permitted, but always reports "access denied" even for valid users.
The bug is that the JSON file stores IDs as integers but the login ID arrives as
a string from user input, and `"42" != 42` in Python. Teaches how JSON types map
to Python types and why type conversion must happen explicitly at system boundaries.

## Wrong Recursive Base Case {: #basicpy-recurse}

[% inc recurse.py %]

A recursive function computes factorials correctly for positive numbers but raises
a `RecursionError` for zero; the bug is a base-case condition that uses `>` instead
of `>=`. Teaches how to identify missing or incorrect base cases in recursion.

## Mutable Default Argument {: #basicpy-mutable}

[% inc mutable.py %]

A function appends items to a result list but every call starts with leftover items
from previous calls; the bug is a mutable default argument (`def f(result=[])`).
Teaches Python's mutable default argument trap and why `None` is the correct default.

## Invisible Trailing Whitespace {: #basicpy-trailing}

[% inc trailing.py %]

A script reads a pipe-delimited export from a spreadsheet and compares field values
against expected strings, but matches always fail for rows exported from certain
applications that pad fields with trailing spaces. Teaches that real-world data
often contains invisible characters, and how `.strip()` and `repr()` help diagnose
string comparison failures that look correct to the naked eye.

## String Methods Return Copies {: #basicpy-strmeth}

[% inc strmeth.py %]

A function censors a list of words in a message by calling `message.replace(word,
'***')` for each word, but the original message is unchanged at the end; the bug
is that `str.replace` returns a new string and the return value is never assigned
back. Teaches that string methods never mutate their argument, and that every
string transformation must be captured in a variable.

## Mutating a List During Iteration {: #basicpy-mutiter}

[% inc mutiter.py %]

A loop processes items from a list while removing some of them, and skips every
other matching item; the bug is modifying a list while iterating over it. Teaches
why mutating a collection during iteration causes unpredictable behavior.
