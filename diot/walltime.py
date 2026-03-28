import time
from unittest.mock import patch


def measure(func):
    """Return (elapsed_seconds, return_value) for a call to func."""
    start = time.time()   # BUG: time.time() can go backward (NTP sync, manual adjustment)
    result = func()
    end = time.time()
    return end - start, result


def work():
    time.sleep(0.05)
    return "done"


if __name__ == "__main__":
    # Normal case: elapsed time is positive.
    elapsed, result = measure(work)
    print(f"Normal:           {elapsed:.4f}s  result={result!r}")

    # Simulated NTP step: the system clock is adjusted backward mid-measurement.
    call_count = [0]
    def stepped_back():
        call_count[0] += 1
        return 1000.0 if call_count[0] == 1 else 999.7   # end < start

    with patch("time.time", stepped_back):
        elapsed, result = measure(work)
    print(f"After clock step: {elapsed:.4f}s  result={result!r}")  # negative duration
    print("(time.monotonic() would never produce a negative duration)")
