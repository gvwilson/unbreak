#!/usr/bin/env bash
# Find all CSV files anywhere under the data/ directory.

# BUG: without quotes, the shell expands *.csv in the current directory
# BUG: before passing it to find; if there are CSV files here, find receives
# BUG: their names as paths rather than the pattern; quote the pattern so
# BUG: find receives "*.csv" literally
find data -name *.csv
