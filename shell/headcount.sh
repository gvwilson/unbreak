#!/usr/bin/env bash
# Extract the header row plus the first 10 data rows from headcount.csv
# (11 lines total: 1 header + 10 data).

# BUG: head -n 10 extracts only 10 lines total (the header plus 9 data rows),
# BUG: missing the tenth data row; use head -n 11
head -n 10 headcount.csv
