#!/usr/bin/env bash
# Print the last 5 data rows of headtail.txt (excluding the header line).

# BUG: head -n 5 prints the FIRST 5 lines, not the last 5; use tail -n 5
head -n 5 headtail.txt
