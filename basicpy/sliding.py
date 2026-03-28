def sliding_windows(data, k):
    """Return all sliding windows of size k over data."""
    return [data[i : i + k] for i in range(len(data) - k)]  # BUG: should be len(data) - k + 1


if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    k = 3
    windows = sliding_windows(data, k)
    print(f"Windows: {windows}")
    print(f"Got {len(windows)}, expected {len(data) - k + 1}")
