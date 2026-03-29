import polars as pl

# 999 is a sentinel value meaning "no response recorded"; treat as missing.
SENTINEL = 999

df = pl.read_csv("sentinel.csv")

# BUG: fill_null only replaces actual null values; 999 is a real integer in the
# BUG: column, not a null, so this call has no effect on the sentinel rows
clean = df.with_columns(
    pl.col("response_time").fill_null(None)
)
print(clean["response_time"].mean())
