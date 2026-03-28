def sorted_logs(filenames):
    """Return filenames sorted by their embedded sequence number."""
    return sorted(filenames)  # BUG: lexicographic order; "file10.txt" sorts before "file2.txt"


if __name__ == "__main__":
    files = ["file10.txt", "file2.txt", "file1.txt", "file20.txt", "file3.txt"]
    result = sorted_logs(files)
    print("Sorted order:")
    for f in result:
        print(f"  {f}")
    print()
    print("Expected numeric order: file1, file2, file3, file10, file20")
