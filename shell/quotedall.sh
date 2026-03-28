#!/usr/bin/env bash
# Usage: quotedall.sh file1 file2 ...
# Count the lines in each file passed as an argument.

for f in $@
do
    # BUG: unquoted $@ undergoes word-splitting; a filename like
    # BUG: "field notes.txt" becomes two tokens ("field" and "notes.txt"),
    # BUG: causing wc to look for non-existent files; use "$@" instead
    wc -l "$f"
done
