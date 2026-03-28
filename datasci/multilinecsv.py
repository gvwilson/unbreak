import polars as pl

# Load survey results and report the number of respondents.

# BUG: missing skip_rows=2 to skip the two preamble lines before the header
df = pl.read_csv("multilinecsv.csv")
print(f"Rows: {len(df)}")
print(df.head())
