# Performance, Concurrency, and System Interaction

## Repeated Scans

A function finds the most common word in a text file by calling `text.count(word)`
for every unique word it encounters, re-scanning the entire text each time; on a
file of 50,000 words it takes several seconds, while a single pass with
`collections.Counter` is nearly instant. Teaches how to identify repeated-scan
inefficiency with `cProfile` and how choosing the right data structure eliminates
the need for multiple passes.

## Subprocess Waiting for Input

A command-line tool that calls a subprocess hangs and never returns; the bug is
that the subprocess is waiting for input on stdin that the parent never provides.
Teaches how subprocess I/O streams work and how to use `communicate()` safely.

## Race Condition in Shared Counter

A script that spawns several threads to update a shared counter produces wrong
totals; the bug is a race condition caused by unsynchronized read-modify-write.
Teaches what a race condition is, why it is hard to reproduce, and how to use
`threading.Lock` to fix it.

## Multiprocessing Memory Model

A program uses `multiprocessing` but child processes do not see changes made to a
shared list; the bug is that each process has its own copy of memory (no shared
state). Teaches the difference between threading and multiprocessing memory models.

## Mock Patched at Wrong Location

A script that patches a function with `unittest.mock.patch` has no effect because
the patch is applied to the wrong module; the bug is patching where the function
is defined instead of where it is imported. Teaches how Python's import system
works and where mocks must be applied.
