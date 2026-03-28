import polars as pl

df = pl.DataFrame({
    "id": [1, 2],
    "tags": ["python,data,science", "web,api"],
})

# BUG: explode() requires a column of lists; calling it on a plain string column
# BUG: raises an InvalidOperationError; split the strings into lists first with
# BUG: pl.col("tags").str.split(",") before calling explode()
result = df.explode("tags")
print(result)
