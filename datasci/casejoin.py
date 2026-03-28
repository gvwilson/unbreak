import polars as pl

sales = pl.DataFrame({
    "Region": ["North", "South", "East", "West", "North", "South"],
    "amount": [100, 200, 150, 175, 120, 210],
})

# Compute per-region mean sales.
means = sales.group_by("Region").agg(
    pl.col("amount").mean().alias("mean_amount")
)

# BUG: means has "Region" with values ["north","south",...] because the groupby
# BUG: key was lowercased in a prior step; join values do not match the original casing
means = means.with_columns(pl.col("Region").str.to_lowercase())

result = sales.join(means, on="Region", how="left")
print(result)
