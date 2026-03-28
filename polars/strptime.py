import polars as pl

df = pl.DataFrame({
    "event": ["conference", "deadline", "review"],
    "date_str": ["03/04/2024", "07/08/2024", "11/12/2024"],
})

# BUG: the dates use day/month/year order but the format string specifies
# BUG: month/day/year (%m/%d/%Y), so "03/04/2024" parses as March 4 instead
# BUG: of April 3; no error is raised because all values are valid under either
# BUG: interpretation; use "%d/%m/%Y" to match the actual day/month/year format
result = df.with_columns(
    pl.col("date_str").str.to_date(format="%m/%d/%Y").alias("date")
)
print(result)
