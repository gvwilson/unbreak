#!/usr/bin/env bash
# Copy the monthly notes files to the archive directory.
# Monthly notes are notes_jan.txt and notes_feb.txt.
# notes_archive.txt is the running archive and should NOT be copied.

# BUG: *.txt matches notes_archive.txt as well as the monthly files;
# BUG: the pattern should be notes_???.txt or list the files explicitly
cp *.txt archive/
