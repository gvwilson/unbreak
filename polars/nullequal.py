import polars as pl

df = pl.DataFrame({
    "name": ["Alice", "Bob", "Carol", "Dave"],
    "score": [88, None, 95, None],
})

# BUG: == None produces a null series rather than a boolean series, because any
# BUG: comparison involving null yields null in Polars; use .is_null() instead
result = df.filter(pl.col("score") == None)  # noqa: E711
print(f"rows with missing score: {len(result)}")
print(result)
