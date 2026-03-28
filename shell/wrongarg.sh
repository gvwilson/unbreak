#!/usr/bin/env bash
# Usage: wrongarg.sh input_file output_file
# Copy the first 20 lines of input_file into output_file.

# BUG: arguments are swapped; "$2" is the output file, "$1" is the input file;
# BUG: this reads from the output path and writes to the input path
head -n 20 "$2" > "$1"
