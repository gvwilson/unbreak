import polars as pl

df = pl.DataFrame({
    "name": ["Alice", "Bob", "Carol", "Dave"],
    "score": [88, 72, 95, 61],
})

result = (
    df.lazy()
    .filter(pl.col("score") >= 80)
    .select(["name", "score"])
    # BUG: .collect() is never called, so result is a LazyFrame (a query plan)
    # BUG: rather than a DataFrame; the filter and select have not yet run
)
print(type(result))
print(result)
