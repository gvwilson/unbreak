import polars as pl

WINDOW = 7  # days

df = pl.read_csv("rolling.csv")

# BUG: without min_periods=1, any window that cannot be filled to size WINDOW
# BUG: returns null; the first six rows will all be null instead of partial means
result = df.with_columns(
    pl.col("value")
    .rolling_mean(window_size=WINDOW)
    .alias("rolling_mean")
)
print(result)
