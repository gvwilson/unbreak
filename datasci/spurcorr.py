import polars as pl

data = pl.DataFrame({
    "base": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
})

# BUG: both "metric_a" and "metric_b" are derived from "base" in the same
# BUG: step; they differ only by a constant offset, so their correlation is
# BUG: exactly 1.0 regardless of the underlying data
data = data.with_columns(
    (pl.col("base") * 2.5).alias("metric_a"),
    (pl.col("base") * 2.5 + 10.0).alias("metric_b"),
)

corr = data.select(pl.corr("metric_a", "metric_b")).item()
print(f"Correlation: {corr}")
