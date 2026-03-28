#!/usr/bin/env bash
# Report the number of observation records in wcflag.txt.
# Each line is one record.

# BUG: -w counts words, not lines; use -l to count lines (records)
wc -w wcflag.txt
