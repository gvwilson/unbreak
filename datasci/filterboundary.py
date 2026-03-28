import polars as pl

# Keep only rows where value EXCEEDS (strictly greater than) the threshold.
THRESHOLD = 50.0

df = pl.read_csv("filterboundary.csv")

# BUG: >= keeps rows equal to the threshold; should be >
result = df.filter(pl.col("value") >= THRESHOLD)
print(result)
