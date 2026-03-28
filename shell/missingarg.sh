#!/usr/bin/env bash
# Usage: missingarg.sh filename
# Print the filename and its line count.

# BUG: if the user runs the script with no argument, $1 is empty;
# BUG: echo prints "File: " and wc -l with no filename reads from standard
# BUG: input, causing the script to hang waiting for keyboard input
echo "File: $1"
wc -l $1
