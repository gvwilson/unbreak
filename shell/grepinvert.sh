#!/usr/bin/env bash
# Print all lines in the log that contain the word "ERROR".

# BUG: -v inverts the match and prints lines that do NOT contain "ERROR";
# BUG: remove -v to print only the matching lines
grep -v "ERROR" grepinvert.txt
