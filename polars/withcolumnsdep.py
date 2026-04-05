import polars as pl

df = pl.DataFrame({
    "price": [100.0, 200.0, 300.0],
    "tax_rate": [0.1, 0.2, 0.1],
})

# BUG: all expressions in a single with_columns() call are evaluated against the
# BUG: original DataFrame; "discounted_price" does not yet exist when "total" is
# BUG: computed, so Polars raises a ColumnNotFoundError; use two separate
# BUG: with_columns() calls so the second can reference the first's output
result = df.with_columns([
    (pl.col("price") * 0.9).alias("discounted_price"),
    (pl.col("discounted_price") * (1 + pl.col("tax_rate"))).alias("total"),
])
print(result)
