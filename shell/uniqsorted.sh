#!/usr/bin/env bash
# Count the number of distinct species recorded in species.csv.

# BUG: uniq only removes *adjacent* duplicate lines; the species column is not
# BUG: sorted, so non-adjacent duplicates are counted separately; pipe through sort
# BUG: before uniq to collapse all duplicates
cut -d, -f2 species.csv | uniq | wc -l
