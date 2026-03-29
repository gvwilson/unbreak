#!/usr/bin/env bash
# Assemble the three sections of the report in order: introduction, methods, results.

# BUG: sections are listed in the wrong order (results, introduction, methods);
# BUG: the correct order is section1.txt section2.txt section3.txt
cat section3.txt section1.txt section2.txt > report.txt
