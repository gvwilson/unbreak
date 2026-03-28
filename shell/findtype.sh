#!/usr/bin/env bash
# Count all log files (and only log files) under the current directory.

# BUG: without -type f, find also counts directories whose names end in .log;
# BUG: add -type f to restrict results to regular files
find . -name "*.log" | wc -l
