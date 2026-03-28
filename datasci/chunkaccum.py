import polars as pl

CHUNK_SIZE = 2  # rows per chunk

# BUG: all chunks are appended to a list and then concatenated at the end;
# BUG: for a large file this holds the entire dataset in memory twice (once in
# BUG: the list, once in the concatenated result); use pl.scan_csv() with lazy
# BUG: evaluation to process the file without loading it all at once
chunks = []
for chunk in pl.read_csv_batched("chunkaccum.csv", batch_size=CHUNK_SIZE):
    chunks.append(chunk)

result = pl.concat(chunks)
print(result["value"].sum())
