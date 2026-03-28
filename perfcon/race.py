import threading

THREADS = 5
INCREMENTS = 100_000

counter = 0


def increment():
    global counter
    for _ in range(INCREMENTS):
        counter = counter + 1  # BUG: read-modify-write is not atomic;
                                #      another thread may read the same value
                                #      between the read and the write


if __name__ == "__main__":
    threads = [threading.Thread(target=increment) for _ in range(THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    expected = THREADS * INCREMENTS
    print(f"Expected: {expected}")
    print(f"Got:      {counter}")
    if counter != expected:
        print(f"Lost {expected - counter} increments to the race condition")
    else:
        print("(got lucky this run — try again or increase INCREMENTS)")
