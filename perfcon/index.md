# Performance, Concurrency, and System Interaction

## Search a large log file for matching entries {: #perfcon-repscans}

Run the word-frequency function on the provided text file and time how long it
takes. Then run `cProfile` on it to see which lines consume the most time.

[% inc repscans.py scrub="\s*# BUG.*" %]
[% inc repscans.txt %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `text.count(word)` for every unique word, re-scanning the entire
text each time. On a file of 50,000 words it takes several seconds, while a single
pass with `collections.Counter` is nearly instant.

Shows: how to identify repeated-scan inefficiency with `cProfile` and
how choosing the right data structure eliminates the need for multiple
passes.

To find it: run `python -m cProfile -s cumulative script.py | head -20` and look for
`str.count` near the top of the cumulative-time column. Each call re-scans the
entire string; multiplying the call count by the string length shows why this is
slow.

</details>

## Run an external tool and capture its output {: #perfcon-subproc}

Run this script. Does it return promptly, or does it hang?

[% inc subproc.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the subprocess is waiting for input on stdin that the parent never
provides, so the script hangs and never returns.

Shows: how subprocess I/O streams work and how to use `communicate()`
safely.

To find it: run the script and wait ten seconds. If it does not return, kill it with
Ctrl-C. Then check the `Popen` call: if `stdin` is not set to `subprocess.DEVNULL`
or `subprocess.PIPE` paired with `communicate()`, the child inherits the terminal
and blocks waiting for input that never arrives.

</details>

## Count requests handled by concurrent workers {: #perfcon-race}

Run this script several times and record the final counter value each time. Is the
value always the same? Is it always the value you expect?

[% inc race.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a race condition caused by unsynchronized read-modify-write, so multiple
threads updating a shared counter produce wrong totals.

Shows: what a race condition is, why it is hard to reproduce, and how
to use `threading.Lock` to fix it.

To find it: run the script five times in a row and record each final counter value.
If the values differ across runs, the counter is not being updated atomically. Print
the expected value (number of threads multiplied by increments per thread) alongside
each observed value to make the discrepancy concrete.

</details>

## Share a lookup table across worker processes {: #perfcon-multiproc}

Run this script and compare the contents of the shared list before and after the
worker processes run. Did the workers modify the list you passed in?

[% inc multiproc.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that each process has its own copy of memory, so changes made inside
child processes are not visible in the parent's shared list.

Shows: the difference between threading and multiprocessing memory
models.

To find it: print `id(shared_list)` inside the worker function and inside the parent
process. If the two addresses differ, each process has its own copy of the list and
modifications inside workers are invisible to the parent.

</details>

## Test a function that sends email notifications {: #perfcon-mockpatch}

Run the test. Does it pass? Add a print statement inside the mock to check whether
the mock is actually being called. Then look at the return value of the function
under test.

[% inc mockpatch_source.py scrub="\s*# BUG.*" %]
[% inc mockpatch_user.py scrub="\s*# BUG.*" %]
[% inc mockpatch.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is patching where the function is defined instead of where it is imported,
so `unittest.mock.patch` has no effect on the code under test.

Shows: how Python's import system works and where mocks must be
applied.

To find it: add `print("mock was called")` as the first line of the mock function.
Run the test. If the print never appears, the mock is not intercepting the real call.
Then check where `send_email` was imported in the module under test — the patch must
name that module, not the one where `send_email` is defined.

</details>
