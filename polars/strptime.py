import polars as pl

df = pl.DataFrame({
    "event": ["launch", "review", "close"],
    "date_str": ["2024-03-15", "2024-04-01", "2024-05-20"],
})

# BUG: the format string uses %d/%m/%Y (day/month/year with slashes) but the
# BUG: dates are formatted as YYYY-MM-DD; strict=False hides the mismatch by
# BUG: silently producing all nulls; use "%Y-%m-%d" to match the actual format
result = df.with_columns(
    pl.col("date_str").str.to_date(format="%d/%m/%Y", strict=False).alias("date")
)
print(result)
print(f"null dates: {result['date'].null_count()}")
