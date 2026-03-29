#!/usr/bin/env bash
# Collect word counts for all .dat files into summary.txt.
# Running this script a second time should produce the same summary,
# not a file with doubled entries.

for f in *.dat
do
    # BUG: >> appends every time the script runs; on a second run the file
    # BUG: contains each entry twice; redirect the first write with > and the
    # BUG: rest with >>, or delete summary.txt before the loop
    wc -w "$f" >> summary.txt
done
