import os
import sys


def summarize(input_file, output_file):
    """Write uppercased non-blank lines from input_file to output_file."""
    out = open(output_file, "w")       # BUG: not using 'with'; if an exception occurs,
                                       # BUG: out.close() is never called and the write
                                       # BUG: buffer may not be flushed to disk
    with open(input_file) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                raise ValueError(f"Unexpected blank line in {input_file!r}")
            out.write(line.upper() + "\n")
    out.close() # BUG: never reached when exception is raised above


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "unclosed.txt"
    output_file = "unclosed_out.txt"

    try:
        summarize(input_file, output_file)
    except ValueError as e:
        print(f"Error: {e}")

    if os.path.exists(output_file):
        with open(output_file) as f:
            lines = f.readlines()
        print(f"Output has {len(lines)} line(s) — may be incomplete (buffer not flushed)")
        for line in lines:
            print(f"  {line!r}")
