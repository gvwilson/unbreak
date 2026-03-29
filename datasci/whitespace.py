import polars as pl

df = pl.read_csv("whitespace.csv")

# BUG: the "region" column has inconsistent surrounding whitespace
# BUG: ("North " and "North" are treated as different groups); should call
# BUG: .str.strip_chars() before grouping
result = df.group_by("region").agg(pl.col("sales").sum())
print(result)
