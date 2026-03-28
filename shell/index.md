# The Unix Shell

## Sort a list of numbers from smallest to largest {: #shell-numericsort}

Run this script and look at the order of the numbers it prints. Is the smallest
number first? What order would you expect?

[% inc numericsort.sh scrub="\s*# BUG.*" %]
[% inc numericsort.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `sort` without the `-n` flag, which causes lexicographic
(alphabetical) ordering so `10` appears before `2`.

Shows: the difference between alphabetical and numeric sort and when
to use `sort -n`.

To find it: look at where `10` appears in the output — if it comes before `2`, the
sort is alphabetical because `"1" < "2"` at the first character. Run `sort -n` on
the same input and compare.

</details>

## Collect a summary line from each file in a directory {: #shell-overwrite}

Run this script and then look at `summary.txt`. How many lines does it contain?
How many did you expect?

[% inc overwrite.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `>` inside the loop, which overwrites the file on every iteration
instead of appending to it, so the summary contains only one entry.

Shows: the difference between `>` (overwrite) and `>>` (append).

To find it: run the script and then count the lines in `summary.txt` with
`wc -l summary.txt`. If only one line appears instead of one per file, look inside
the loop for `>` and check whether it should be `>>`.

</details>

## Copy monthly notes files to an archive directory {: #shell-wideglob}

Look at the list of `.txt` files in the directory. Which files does `*.txt` match?
Are all of them files you want to copy?

[% inc wideglob.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `*.txt` matches every `.txt` file in the directory, including the
running archive file itself, so the script copies more than the monthly notes files.

Shows: how to check what a wildcard matches before using it in a
destructive command, and how to narrow a pattern (e.g.,
`notes_???.txt`) to match only the intended files.

To find it: before running the script, run `echo *.txt` in the directory and read
the expansion. If the list includes files you do not want to copy, narrow the
pattern before using it.

</details>

## Count distinct species in a CSV file {: #shell-uniqsorted}

Run this script and check the count it reports. Then look at the species column in
`species.csv`. How many distinct species are there, and does the count match?

[% inc uniqsorted.sh scrub="\s*# BUG.*" %]
[% inc species.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is piping directly to `uniq` without sorting first. Only adjacent identical
lines are collapsed, so non-adjacent occurrences of the same species are counted
separately and the reported count is too high.

Shows: that `uniq` only removes adjacent duplicates and that
`sort | uniq` is the correct pattern for counting distinct values.

To find it: run `sort species.csv | uniq | wc -l` and compare the count to
`cat species.csv | uniq | wc -l`. If the two counts differ, non-adjacent duplicates
are being missed by `uniq` alone.

</details>

## Count words in files whose names contain spaces {: #shell-quotedvar}

Run this script with a filename that contains a space (e.g., `"field notes.txt"`).
Does it process the file correctly?

[% inc quotedvar.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `$f` without quotes, so the shell splits the filename on the space
and passes the two halves as separate arguments to `wc`, causing the loop to fail
for any filename that contains a space.

Shows: why loop variables should always be quoted as `"$f"` and how
spaces in filenames require consistent quoting throughout a script.

To find it: replace the command inside the loop with two consecutive lines
(i.e., `echo "$f"` and `echo $f`) then run with a filename containing a space. The
unquoted version prints the name split into two words; the quoted version prints it
as one.

</details>

## Filter lines from an input file into an output file {: #shell-wrongarg}

Run the script with a small input file and the name of an output file. Look at
which file was created and which file was modified.

[% inc wrongarg.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the arguments `$1` and `$2` are swapped, so the script reads from
the output path and writes to the input path instead.

Shows: how to verify which argument is which by reading the usage
comment, and how to use `echo` to print argument values before acting
on them.

To find it: replace the `grep` command temporarily with
`echo "reading from $1, writing to $2"` and run the script. If the output shows the
input and output filenames in the wrong positions, swap `$1` and `$2`.

</details>

## Print the most recent entries from a log file {: #shell-headtail}

Run this script and note which rows are printed. Are they from the beginning or
end of the file?

[% inc headtail.sh scrub="\s*# BUG.*" %]
[% inc headtail.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `head` (which prints the first N lines) instead of `tail` (which
prints the last N lines), so the script shows the oldest entries instead of the most
recent ones.

Shows: the difference between `head` and `tail` and how to combine
them, for example `tail -n 5` for the last 5 or `head -n 10 | tail -n 5`
for lines 6-10.

To find it: run `head -n 5 logfile.txt` and compare the timestamps to the script's
output. If both show the earliest timestamps, the wrong command is being used. Run
`tail -n 5 logfile.txt` to confirm those are the most recent entries.

</details>

## Save output to a shared directory one level up {: #shell-dotdot}

Read the comment at the top of the script. Map out the expected directory structure
on paper. How many levels up does `../..` go? Is that where `shared/` lives?

[% inc dotdot.sh scrub="\s*# BUG.*" %]
[% inc measurements.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is writing `../..` when the target is only one level up (`..`), so the
script saves output two levels up instead of one.

Shows: how to trace relative paths by counting directory levels, and
how to use `pwd` and `ls ..` to verify the directory structure before
running a script.

To find it: add `echo "saving to: $(pwd)/../../shared/"` before the output
command and run the script. Count how many directory levels `../../` climbs in
the printed path and compare that to a sketch of the directory tree you drew on
paper.

</details>

## Count the records in a data file {: #shell-wcflag}

Run this script and look at the numbers it prints. Do they match the number of
lines (records) in the file?

[% inc wcflag.sh scrub="\s*# BUG.*" %]
[% inc wcflag.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `wc -w` (count words) instead of `wc -l` (count lines), so the
script prints a much larger number than the number of records.

Shows: the difference between `wc` flags and how to use `wc --help` to
check which flag produces which count.

To find it: run both `wc -l file.txt` and `wc -w file.txt` on the same file and
compare the two numbers. If the script is printing the larger number, it is
counting words rather than lines.

</details>

## Find all CSV files in a directory tree {: #shell-findglob}

Run this script from a directory that contains at least one `.csv` file. What
arguments does `find` actually receive? Use `echo` in place of `find` to check.

[% inc findglob.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is passing `*.csv` without quotes, so the shell expands the glob before
`find` runs and the command searches for files whose names match already-expanded
filenames from the current directory.

Shows: that the shell expands unquoted wildcards before passing them
to any command, and that patterns given to `find -name` must be
quoted.

To find it: replace `find` with `echo find` and run the command. The shell will
print the arguments `find` would receive. If `*.csv` was expanded, the argument
list shows specific filenames rather than the literal pattern `*.csv`.

</details>

## Extract family names from a tab-separated file {: #shell-cutdelim}

Run this script and examine the output. Does each output line contain just the
family name, or does it contain the whole row?

[% inc cutdelim.sh scrub="\s*# BUG.*" %]
[% inc cutdelim.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is specifying `-d,` (comma delimiter) when the file uses tabs. Since there
are no commas, `cut` treats each line as a single field and returns it whole.

Shows: how to identify the actual delimiter in a file (using `cat -A`
to show invisible characters) and how to specify a tab with `-d$'\t'`.

To find it: run `cat -A file.txt | head -n 3` to make invisible characters visible.
Tab characters appear as `^I`. If `^I` separates the fields but `-d,` specifies a
comma, `cut` will see no delimiter and return each entire line as a single field.

</details>

## Filter error lines from a log file {: #shell-grepinvert}

Run this script and read the output. Do the lines shown contain the word you
were searching for?

[% inc grepinvert.sh scrub="\s*# BUG.*" %]
[% inc grepinvert.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the `-v` flag, which inverts the match so `grep` shows lines that do not
contain the pattern. The script prints everything except the error lines instead of
just the error lines.

Shows: what `-v` does and how to check the result of a `grep` command
against a small known file to confirm it is filtering in the right
direction.

To find it: run the script on the sample file and check whether any output line
contains the search term. If every output line lacks the search term, `-v` is
inverting the match. Remove `-v` to keep only matching lines.

</details>

## Count the lines in a file given on the command line {: #shell-missingarg}

Run this script with no arguments. Does it print useful output, produce an error,
or do something else? Use `Ctrl-C` to stop it if it appears to hang.

[% inc missingarg.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `$1` expands to nothing when no argument is given and `wc -l` with
no filename reads from standard input, so the script hangs waiting indefinitely for
keystrokes.

Shows: how positional parameters expand to empty strings when omitted,
and how to check for missing arguments with `echo "Usage: …"` before
using them.

To find it: run the script with no arguments and watch whether it hangs. Press
Ctrl-C to stop it. Then add `echo "Got: '$1'"` as the first line — running again
shows `Got: ''`, proving `$1` is empty and that `wc -l` is reading from stdin
instead of a file.

</details>

## Concatenate report sections in the correct order {: #shell-catorder}

Run this script and read the resulting `report.txt`. Does the report begin with
the introduction, or with a different section?

[% inc catorder.sh scrub="\s*# BUG.*" %]
[% inc section1.txt %]
[% inc section2.txt %]
[% inc section3.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the filenames are listed in the wrong sequence on the `cat` command
line, so the sections appear in the wrong order.

Shows: that `cat` concatenates files in the order they are given, and
how to verify the result with `head` before treating the output as
correct.

To find it: run `head -n 3 report.txt` after the script finishes. The first few
lines should come from the introduction file. If they do not, compare the order of
filenames on the `cat` command line to the intended section order.

</details>

## Append a summary line from each file to a report {: #shell-loopclobber}

Run this script once, then run it again. How many lines does `summary.txt` contain
after the first run? After the second run?

[% inc loopclobber.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `>>` inside the loop without clearing the file first, so each run
appends to whatever the previous run left and the file contains double the expected
entries after a second run.

Shows: how to decide between `>` and `>>`, and the pattern of
redirecting the first write with `>` or removing the output file
before the loop begins.

To find it: run the script twice and count the lines in `summary.txt` with
`wc -l` after each run. If the count doubles on the second run, the file is not
being cleared before the loop. Remove the file or use `>` on the first write before
switching to `>>` for subsequent writes.

</details>

## List the three largest files in a directory {: #shell-sortn}

Run this script in a directory that has files of different sizes. Compare the
output to `ls -s | sort -rn | head -n 3`. Are the results the same?

[% inc sortn.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `sort -r`, which reverses alphabetical order rather than numeric
order. A file of size 100 blocks sorts as smaller than 8 because `"8"` comes after
`"1"` in alphabetical order, so the three largest files are listed in the wrong
order.

Shows: that `-r` alone reverses the current sort order and that `-rn`
is needed to sort numbers in descending order.

To find it: run `ls -s` in the directory and note the block counts for a few files.
If the script output shows a file with size 100 below a file with size 8, the sort
is alphabetical rather than numeric. Compare with `ls -s | sort -rn | head -n 3`.

</details>

## Extract ten data rows from a CSV file {: #shell-headcount}

Run this script and count the data rows in the output. Then count the data rows
in the original file. Are they the same?

[% inc headcount.sh scrub="\s*# BUG.*" %]
[% inc headcount.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `head -n 10` when the header itself is one of the ten lines, so only nine
data rows remain instead of ten.

Shows: how to account for header lines when counting with `head` and
how to use `wc -l` to verify the actual line count of the output.

To find it: run `wc -l` on both the script's output and the original file. If the
output has 10 lines total but you expected 10 data rows plus a header, the header
was counted as one of the 10 lines. Use `head -n 11` to include the header and 10
data rows.

</details>

## Process a list of filenames passed as script arguments {: #shell-quotedall}

Run this script with a filename that contains a space. Does it process the file,
or does it report an error about a non-existent file?

[% inc quotedall.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `$@` without quotes, which causes word-splitting so each
space-separated token is treated as a separate argument and the script fails for any
argument that contains a space.

Shows: the difference between `$@` and `"$@"`: the quoted form
preserves each argument as a single token, even if it contains spaces.

To find it: add `echo "Processing: '$1'"` inside the loop and run with a filename
containing a space. The unquoted `$@` version prints two separate single-word
arguments for one filename; the quoted `"$@"` version prints one argument with the
space preserved.

</details>

## Count log files in a directory tree {: #shell-findtype}

Create a directory whose name ends in `.log` (e.g., `mkdir debug.log`). Now run
this script. Does the count include the directory?

[% inc findtype.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `-name "*.log"` matches any filesystem entry, not just regular
files, so directories whose names end in `.log` are included in the count.

Shows: the use of `-type f` to restrict `find` results to regular
files and `-type d` to restrict to directories.

To find it: create a directory whose name ends in `.log` — e.g., `mkdir debug.log`
— then run `find . -name "*.log"` and see whether that directory appears in the
output. Add `-type f` and rerun to confirm it is excluded.

</details>

## Copy a directory to a backup location {: #shell-cprecurse}

Run this script. Does it copy the directory, or does it produce an error message?
What does the error message say?

[% inc cprecurse.sh scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `cp` without the `-r` flag, which is required to copy a directory
and its contents recursively, so the script fails with the message "omitting
directory".

Shows: the difference between copying a file and copying a directory,
and how to read `cp --help` to find the right flag.

To find it: run the script and read the error message. It says
`cp: -r not specified; omitting directory`, i.e., the message names
the missing flag directly.

</details>
