#!/usr/bin/env bash
# Count the lines in each text file passed to this script.

for f in "$@"
do
    # BUG: $f without quotes splits on spaces in filenames; a file called
    # BUG: "field notes.txt" becomes two arguments: "field" and "notes.txt"
    wc -l $f
done
