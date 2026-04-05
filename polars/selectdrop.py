import polars as pl

df = pl.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Carol"],
    "score": [88, 72, 95],
})

# BUG: .select() returns only the listed columns and drops all others;
# BUG: id and name are lost; use .with_columns() to add a new column
# BUG: while keeping the existing ones
result = df.select([
    (pl.col("score") * 1.1).alias("adjusted"),
])
print(result)
