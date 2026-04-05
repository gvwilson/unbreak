import polars as pl

df = pl.DataFrame({
    "id": [1, 2, 3, 4],
    "value": ["10", "20", "N/A", "40"],
})

# BUG: strict=False silently converts unparseable strings to null rather than
# BUG: raising an error, so the bad value "N/A" disappears into the data without
# BUG: any warning; remove strict=False (or use strict=True) to surface it immediately
result = df.with_columns(pl.col("value").cast(pl.Int64, strict=False))
print(result)
print(f"null count in value: {result['value'].null_count()}")
