#!/usr/bin/env bash
# Print the numbers in numericsort.txt in ascending order.

# BUG: sort without -n uses alphabetical order; "10" sorts before "2"
sort numericsort.txt
