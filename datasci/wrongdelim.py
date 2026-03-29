import polars as pl

df_a = pl.read_csv("wrongdelim_a.csv")

# BUG: wrongdelim_b.csv uses semicolons as delimiters; reading without
# BUG: separator=";" treats each row as a single column and produces a DataFrame
# BUG: with one wide column instead of three; pl.concat with how="diagonal"
# BUG: then fills the missing columns with nulls
df_b = pl.read_csv("wrongdelim_b.csv")

combined = pl.concat([df_a, df_b], how="diagonal")
print(f"Columns: {combined.columns}")
print(combined)
