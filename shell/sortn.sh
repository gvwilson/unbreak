#!/usr/bin/env bash
# List the three largest files in the current directory by block size,
# largest first.

# BUG: sort -r reverses alphabetical order; numbers like 8, 12, 100 sort
# BUG: as "100" < "12" < "8" alphabetically, giving the wrong largest-first order;
# BUG: use sort -rn for numeric reverse sort
ls -s | sort -r | head -n 3
