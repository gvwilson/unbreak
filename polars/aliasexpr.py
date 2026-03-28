import polars as pl

df = pl.DataFrame({
    "price": [10.0, 20.0, 30.0],
    "qty": [3, 1, 2],
})

# BUG: no .alias() on the expression, so Polars names the result column "price"
# BUG: (the left operand's name), silently replacing the original price column
# BUG: instead of adding a new "total" column; add .alias("total") to name it correctly
result = df.with_columns(pl.col("price") * pl.col("qty"))
print(result)
