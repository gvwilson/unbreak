import polars as pl

CUTOFF = "2024-06-01"

df = pl.read_csv("datestring.csv")

# BUG: "date" is read as Utf8 (string); comparison is lexicographic, not
# BUG: chronological, so the filter may include or exclude wrong rows
result = df.filter(pl.col("date") > CUTOFF)
print(result)
