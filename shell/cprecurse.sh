#!/usr/bin/env bash
# Back up the entire results/ directory to backup/results/.

# BUG: cp without -r cannot copy a directory and exits with an error;
# BUG: use cp -r to copy the directory and all its contents
cp results/ backup/results/
