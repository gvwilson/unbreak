#!/usr/bin/env bash
# Collect the first (header) line of each .dat file into summary.txt.

for f in overwrite_a.dat overwrite_b.dat overwrite_c.dat
do
    # BUG: > overwrites summary.txt on every iteration; use >> to append
    head -n 1 "$f" > summary.txt
done
