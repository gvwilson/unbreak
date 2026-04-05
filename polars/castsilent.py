import polars as pl

df = pl.DataFrame({
    "id": [1, 2, 3, 4],
    "score": [88.7, 72.3, 95.6, 61.9],
})

# BUG: cast(pl.Int64) truncates toward zero rather than rounding,
# BUG: so 88.7 becomes 88 and 95.6 becomes 95 instead of 89 and 96;
# BUG: use .round(0).cast(pl.Int64) to round before truncating
result = df.with_columns(pl.col("score").cast(pl.Int64))
print(result)
print("expected if rounded:", [round(x) for x in [88.7, 72.3, 95.6, 61.9]])
