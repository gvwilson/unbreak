# The Unix Shell

## Numeric Sort {: #shell-numericsort}

Run this script and look at the order of the numbers it prints. Is the smallest
number first? What order would you expect?

[% inc numericsort.sh scrub="\s*# BUG.*" %]
[% inc numericsort.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that sorts a list of numbers produces them in the wrong order; the bug is
calling `sort` without the `-n` flag, which causes lexicographic (alphabetical)
ordering so `10` appears before `2`. Teaches the difference between alphabetical
and numeric sort and when to use `sort -n`.

</details>

## Redirect Overwrites {: #shell-overwrite}

Run this script and then look at `summary.txt`. How many lines does it contain?
How many did you expect?

[% inc overwrite.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A loop that is supposed to collect the first line of each data file into a single
summary produces a file with only one entry; the bug is using `>` inside the loop,
which overwrites the file on every iteration instead of appending to it. Teaches
the difference between `>` (overwrite) and `>>` (append).

</details>

## Wildcard Too Broad {: #shell-wideglob}

Look at the list of `.txt` files in the directory. Which files does `*.txt` match?
Are all of them files you want to copy?

[% inc wideglob.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script copies the monthly notes files to an archive directory but also copies the
running archive file itself because `*.txt` matches every `.txt` file in the
directory. Teaches how to check what a wildcard matches before using it in a
destructive command, and how to narrow a pattern (e.g., `notes_???.txt`) to match
only the intended files.

</details>

## Unsorted Input to `uniq` {: #shell-uniqsorted}

Run this script and check the count it reports. Then look at the species column in
`species.csv`. How many distinct species are there, and does the count match?

[% inc uniqsorted.sh scrub="\s*# BUG.*" %]
[% inc species.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A pipeline that counts the number of distinct species in a CSV file gives a number
that is too high; the bug is piping directly to `uniq` without sorting first, so
only adjacent identical lines are collapsed and non-adjacent occurrences of the
same species are counted separately. Teaches that `uniq` only removes adjacent
duplicates and that `sort | uniq` is the correct pattern for counting distinct values.

</details>

## Unquoted Loop Variable {: #shell-quotedvar}

Run this script with a filename that contains a space (e.g., `"field notes.txt"`).
Does it process the file correctly?

[% inc quotedvar.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A loop that counts lines in files fails when any filename contains a space; the
bug is using `$f` without quotes, so the shell splits the filename on the space
and passes the two halves as separate arguments to `wc`. Teaches why loop
variables should always be quoted as `"$f"` and how spaces in filenames require
consistent quoting throughout a script.

</details>

## Wrong Positional Parameter {: #shell-wrongarg}

Run the script with a small input file and the name of an output file. Look at
which file was created and which file was modified.

[% inc wrongarg.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that copies the first 20 lines of an input file to an output file reads
from the output path and writes to the input path instead; the bug is that the
arguments `$1` and `$2` are swapped. Teaches how to verify which argument is
which by reading the usage comment, and how to use `echo` to print argument values
before acting on them.

</details>

## `head` Instead of `tail` {: #shell-headtail}

Run this script and note which rows are printed. Are they from the beginning or
end of the file?

[% inc headtail.sh scrub="\s*# BUG.*" %]
[% inc headtail.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script intended to show the most recent entries in a data file shows the oldest
entries instead; the bug is using `head` (which prints the first N lines) instead
of `tail` (which prints the last N lines). Teaches the difference between `head`
and `tail` and how to combine them — for example `tail -n 5` for the last 5, or
`head -n 10 | tail -n 5` for lines 6–10.

</details>

## Too Many `..` {: #shell-dotdot}

Read the comment at the top of the script. Map out the expected directory structure
on paper. How many levels up does `../..` go? Is that where `shared/` lives?

[% inc dotdot.sh scrub="\s*# BUG.*" %]
[% inc measurements.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that saves output to a sibling directory goes two levels up instead of
one; the bug is writing `../..` when the target is only one level up (`..`).
Teaches how to trace relative paths by counting directory levels, and how to
use `pwd` and `ls ..` to verify the directory structure before running a script.

</details>

## Wrong `wc` Flag {: #shell-wcflag}

Run this script and look at the numbers it prints. Do they match the number of
lines (records) in the file?

[% inc wcflag.sh scrub="\s*# BUG.*" %]
[% inc wcflag.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that should count the number of records in a file prints a much larger
number; the bug is using `wc -w` (count words) instead of `wc -l` (count lines).
Teaches the difference between `wc` flags and how to use `wc --help` to check
which flag produces which count.

</details>

## Unquoted Glob in `find` {: #shell-findglob}

Run this script from a directory that contains at least one `.csv` file. What
arguments does `find` actually receive? Use `echo` in place of `find` to check.

[% inc findglob.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A `find` command that should search a subdirectory for CSV files instead searches
for files whose names match already-expanded filenames from the current directory;
the bug is passing `*.csv` without quotes, so the shell expands the glob before
`find` runs. Teaches that the shell expands unquoted wildcards before passing
them to any command, and that patterns given to `find -name` must be quoted.

</details>

## Wrong `cut` Delimiter {: #shell-cutdelim}

Run this script and examine the output. Does each output line contain just the
family name, or does it contain the whole row?

[% inc cutdelim.sh scrub="\s*# BUG.*" %]
[% inc cutdelim.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that extracts one column from a tab-delimited file prints the entire line
unchanged; the bug is specifying `-d,` (comma delimiter) when the file uses tabs.
Since there are no commas, `cut` treats each line as a single field and returns it
whole. Teaches how to identify the actual delimiter in a file (using `cat -A` to
show invisible characters) and how to specify a tab with `-d$'\t'`.

</details>

## Inverted `grep` {: #shell-grepinvert}

Run this script and read the output. Do the lines shown contain the word you
were searching for?

[% inc grepinvert.sh scrub="\s*# BUG.*" %]
[% inc grepinvert.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that should print error lines from a log file prints everything except the
error lines; the bug is the `-v` flag, which inverts the match so `grep` shows
lines that do not contain the pattern. Teaches what `-v` does and how to check
the result of a `grep` command against a small known file to confirm it is
filtering in the right direction.

</details>

## Missing Script Argument {: #shell-missingarg}

Run this script with no arguments. Does it print useful output, produce an error,
or do something else? Use `Ctrl-C` to stop it if it appears to hang.

[% inc missingarg.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that expects a filename as its first argument hangs when run with no
arguments because `$1` expands to nothing and `wc -l` with no filename reads from
standard input, waiting indefinitely for keystrokes. Teaches how positional
parameters expand to empty strings when omitted, and how to check for missing
arguments with `echo "Usage: ..."` before using them.

</details>

## Wrong `cat` Order {: #shell-catorder}

Run this script and read the resulting `report.txt`. Does the report begin with
the introduction, or with a different section?

[% inc catorder.sh scrub="\s*# BUG.*" %]
[% inc section1.txt %]
[% inc section2.txt %]
[% inc section3.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that assembles a report from three section files produces them in the
wrong order because the filenames are listed in the wrong sequence on the `cat`
command line. Teaches that `cat` concatenates files in the order they are given,
and how to verify the result with `head` before treating the output as correct.

</details>

## Loop Clobbers on Re-run {: #shell-loopclobber}

Run this script once, then run it again. How many lines does `summary.txt` contain
after the first run? After the second run?

[% inc loopclobber.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that collects statistics into a summary file produces a file with double
the expected entries when run a second time; the bug is using `>>` inside the loop
without clearing the file first, so each run appends to whatever the previous run
left. Teaches how to decide between `>` and `>>`, and the pattern of redirecting
the first write with `>` or removing the output file before the loop begins.

</details>

## Numeric Reverse Sort {: #shell-sortn}

Run this script in a directory that has files of different sizes. Compare the
output to `ls -s | sort -rn | head -n 3`. Are the results the same?

[% inc sortn.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A pipeline intended to show the three largest files lists them in the wrong order
because `sort -r` reverses alphabetical order rather than numeric order; a file of
size 100 blocks sorts as a smaller number than 8 because `"8"` comes after `"1"` in
alphabetical order. Teaches that `-r` alone reverses the current sort order and
that `-rn` is needed to sort numbers in descending order.

</details>

## `head` Off by One {: #shell-headcount}

Run this script and count the data rows in the output. Then count the data rows
in the original file. Are they the same?

[% inc headcount.sh scrub="\s*# BUG.*" %]
[% inc headcount.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that should extract a header and ten data rows produces only nine data
rows; the bug is `head -n 10` when the header itself is one of the ten lines, so
only nine data rows remain. Teaches how to account for header lines when counting
with `head` and how to use `wc -l` to verify the actual line count of the output.

</details>

## Unquoted `$@` {: #shell-quotedall}

Run this script with a filename that contains a space. Does it process the file,
or does it report an error about a non-existent file?

[% inc quotedall.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that loops over all its arguments fails when any argument contains a
space; the bug is using `$@` without quotes, which causes word-splitting so each
space-separated token is treated as a separate argument. Teaches the difference
between `$@` and `"$@"`: the quoted form preserves each argument as a single
token, even if it contains spaces.

</details>

## `find` Missing `-type f` {: #shell-findtype}

Create a directory whose name ends in `.log` (e.g., `mkdir debug.log`). Now run
this script. Does the count include the directory?

[% inc findtype.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that counts log files includes directories whose names end in `.log` in
the count; the bug is that `-name "*.log"` matches any filesystem entry, not just
regular files. Teaches the use of `-type f` to restrict `find` results to regular
files and `-type d` to restrict to directories.

</details>

## `cp` Without `-r` {: #shell-cprecurse}

Run this script. Does it copy the directory, or does it produce an error message?
What does the error message say?

[% inc cprecurse.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that backs up a directory fails with the message "omitting directory";
the bug is calling `cp` without the `-r` flag, which is required to copy a
directory and its contents recursively. Teaches the difference between copying a
file and copying a directory, and how to read `cp --help` to find the right flag.

</details>
