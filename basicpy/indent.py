import sys


def count_runs(filename):
    """Return a list of (value, count) pairs for runs of identical lines."""
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f]

    runs = []
    prev = ""
    run_count = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if line != prev:
            if run_count > 0:
                runs.append((prev, run_count))
            run_count = 0
        run_count += 1
        i += 1
    prev = line  # BUG: should be indented one level to sit inside the while loop body

    if run_count > 0:
        runs.append((prev, run_count))
    return runs


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "indent.txt"
    for value, count in count_runs(filename):
        print(f"{count} x {value!r}")
