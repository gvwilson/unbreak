import polars as pl

df = pl.read_csv("aggorder.csv")

# Compute total sales per region.

# BUG: .sum() is called on the full column before .group_by(), collapsing all
# BUG: rows to one; the subsequent group_by operates on a single-row DataFrame
result = (
    df.select(pl.col("sales").sum())
    .group_by(pl.lit("all"))
    .agg(pl.col("sales").sum())
)
print(result)
