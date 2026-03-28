import polars as pl

data = pl.DataFrame({
    "id": [1, 2, 3, 4],
    "score": [88, 72, 95, 61],
    "label": ["A", "B", "A", "C"],
})

# Build a lazy pipeline: rename "score" to "points", filter, then select.
result = (
    data.lazy()
    .rename({"score": "points"})
    .filter(pl.col("points") > 70)
    # BUG: "score" was renamed to "points" above; referencing "score" here
    # BUG: causes a ColumnNotFoundError that only surfaces at .collect() time
    .select(["id", "score", "label"])
    .collect()
)
print(result)
