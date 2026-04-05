# Basic Python

## Off-by-One in Sliding Window {: #basicpy-sliding}

Run this code with a small list (for example, five elements and a window size of
three) and count the windows by hand. Does the number of windows the code returns
match the number you counted?

[% inc sliding.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `range(len(data) - k)` instead of `range(len(data) - k + 1)`, so the
last window is never produced. Shows how to identify off-by-one errors in index
arithmetic and how to verify boundary conditions with small, hand-checkable examples.

</details>

## String Concatenation Instead of Addition {: #basicpy-catadd}

Run this script with the provided input file and examine the total it prints. Does
the value look like a reasonable sum of exam scores?

[% inc catadd.py scrub="\s*# BUG.*" %]
[% inc catadd.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is accumulating scores with `total = total + line.strip()` (string
concatenation) instead of converting each line to a number first, so the script
always reports a nonsensical total. Shows the difference between string `+` and
numeric `+`, and how to check the type of a value at runtime using `type()` or
`isinstance()`.

</details>

## Boolean Logic in Validation {: #basicpy-andor}

Call the validation function with several passwords, including one you expect to be
accepted. Does it accept any of them?

[% inc andor.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is joining the two conditions with `and` instead of `or`, which requires
both to fail simultaneously and almost never happens, so valid passwords are always
rejected. Shows how boolean logic errors cause silent misbehavior, and how a small
truth table reveals which operator is correct.

</details>

## Misremembered Conversion Formula {: #basicpy-formula}

Call the conversion function with a coordinate you can verify by hand—for example,
1 degree, 30 minutes, 0 seconds should equal 1.5 decimal degrees. Does the function
return the correct value?

[% inc formula.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is dividing seconds by 60 instead of 3600 (a misremembered formula), so the
function gives wrong results. Shows how to verify formulas against known values
(e.g., 1°30′0″ = 1.5°) and how to add assertion checks for values that must fall
within a known range.

</details>

## In-Place Sort Returns None {: #basicpy-sortnone}

Run this script and examine what it prints. Is the list what you expected?

[% inc sortnone.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `list.sort()` (which returns `None`) and assigning the result, so
the list is always empty. Shows that many list methods mutate in place and return
`None`.

</details>

## Misindented Loop State Update {: #basicpy-indent}

Run this script with the provided input file and examine the run-length counts.
Then trace through the loop by hand with a short example—track what the "previous
line" variable holds at each step.

[% inc indent.py scrub="\s*# BUG.*" %]
[% inc indent.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the variable storing the previous line is updated outside (after) the
while loop body due to a missing level of indentation, so every line is counted as
starting a new run. Shows how indentation governs control flow in Python and how to
step through a loop mentally to find where state is updated at the wrong time.

</details>

## Missing Return Statement {: #basicpy-noreturn}

Call the function and print its return value. Is it what you expected?

[% inc noreturn.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a missing `return` statement: the function builds the result but does not
return it, so it returns `None`. Shows that Python functions return `None` by
default and how to spot missing `return` in control flow.

</details>

## KeyError in Word Counter {: #basicpy-nokey}

Run this script with the provided input file. Read the full traceback carefully.
Which line raises the error, and what does the error message tell you about what
is missing?

[% inc nokey.py scrub="\s*# BUG.*" %]
[% inc nokey.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is incrementing `counts[word]` without first checking whether the key exists,
so the function crashes with a `KeyError` on the first new word it encounters.
Shows defensive dictionary access using `dict.get(key, 0)` or
`collections.defaultdict`, and how to read a `KeyError` traceback to identify the
missing key.

</details>

## JSON Integers vs. String Input {: #basicpy-streq}

Run this script with a user ID taken directly from the JSON file. Does it grant
access? Use `type()` to examine the types of the two values being compared.

[% inc streq.py scrub="\s*# BUG.*" %]
[% inc streq.json %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the JSON file stores IDs as integers but the login ID arrives as a
string from user input, and `"42" != 42` in Python, so the script always reports
"access denied" even for valid users. Shows how JSON types map to Python types and
why type conversion must happen explicitly at system boundaries.

</details>

## Wrong Recursive Base Case {: #basicpy-recurse}

Call the function with the argument `0`. Does it return the correct result?

[% inc recurse.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a base-case condition that uses `>` instead of `>=`, so calling the
function with zero triggers infinite recursion and raises a `RecursionError`. Shows
how to identify missing or incorrect base cases in recursion.

</details>

## Mutable Default Argument {: #basicpy-mutable}

Call the function twice in a row with no arguments and compare the two return
values. Are they the same?

[% inc mutable.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a mutable default argument (`def f(result=[])`), so every call starts
with leftover items from previous calls. Shows Python's mutable default argument
trap and why `None` is the correct default.

</details>

## Invisible Trailing Whitespace {: #basicpy-trailing}

Run this script with the provided input file. Use `repr()` on a field value that
fails to match its expected string. Does the `repr()` output reveal anything that
was not visible before?

[% inc trailing.py scrub="\s*# BUG.*" %]
[% inc trailing.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that certain applications pad fields with trailing spaces, so string
comparisons always fail for those rows even though the values look correct to the
naked eye. Shows that real-world data often contains invisible characters, and how
`.strip()` and `repr()` help diagnose string comparison failures.

</details>

## String Methods Return Copies {: #basicpy-strmeth}

Call the function and print the message before and after the call. Has the message
changed?

[% inc strmeth.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `str.replace` returns a new string and the return value is never
assigned back, so the original message is unchanged at the end. Shows that string
methods never mutate their argument, and that every string transformation must be
captured in a variable.

</details>

## Mutating a List During Iteration {: #basicpy-mutiter}

Run this script and count how many items were removed. Is it the number you
expected? Try with a list where every element should be removed.

[% inc mutiter.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is modifying a list while iterating over it, which causes the loop to skip
every other matching item. Shows why mutating a collection during iteration causes
unpredictable behavior.

</details>
