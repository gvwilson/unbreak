#!/usr/bin/env bash
# Run this script from inside results/2024/.
# Save a sorted copy of measurements.txt to the shared/ directory,
# which is one level above the current directory (i.e., results/shared/).

# BUG: ../.. goes up two levels (to the project root), not one;
# BUG: the destination should be ../shared/sorted.txt
sort -n measurements.txt > ../../shared/sorted.txt
