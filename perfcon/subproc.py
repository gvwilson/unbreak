import subprocess
import sys


def count_words(text):
    """Count words in text by passing it to a child Python process."""
    proc = subprocess.Popen(
        [sys.executable, "-c", "import sys; print(len(sys.stdin.read().split()))"],
        stdout=subprocess.PIPE,
        # BUG: stdin not set to subprocess.PIPE, so the child inherits the
        # parent's terminal stdin and waits for keyboard input instead of
        # reading 'text'; communicate() never sends the text to the child
    )
    try:
        stdout, _ = proc.communicate(timeout=3)
        return int(stdout.strip())
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        return None


if __name__ == "__main__":
    sample = "the quick brown fox jumps over the lazy dog"
    print(f"Text: {sample!r}")
    print(f"Expected word count: {len(sample.split())}")
    print("Calling count_words()… (will time out in 3 s if stdin is not piped)")
    result = count_words(sample)
    if result is None:
        print("Timed out — child was waiting for stdin that was never provided")
    else:
        print(f"Word count: {result}")
