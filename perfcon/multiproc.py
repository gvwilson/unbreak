import multiprocessing

results = []


def collect(value):
    results.append(value)  # BUG: modifies the child process's own copy of 'results';
                            #      the parent's 'results' list is never touched


if __name__ == "__main__":
    processes = [
        multiprocessing.Process(target=collect, args=(i,))
        for i in range(5)
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print(f"results: {results}")          # always [] — parent's list is unchanged
    print(f"expected: [0, 1, 2, 3, 4] in some order")
    print()
    print("Each child process gets its own copy of memory.")
    print("Fix: use multiprocessing.Manager().list() or return values via a Queue.")
