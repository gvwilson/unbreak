#!/usr/bin/env bash
# Extract the family name (first column) from the tab-delimited roster.

# BUG: -d, sets comma as the delimiter, but cutdelim.txt uses tabs;
# BUG: omit -d to use the default tab delimiter, or use -d$'\t'
cut -d, -f1 cutdelim.txt
