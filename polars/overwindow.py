import polars as pl

df = pl.DataFrame({
    "name": ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "dept": ["eng", "eng", "hr", "hr", "eng"],
    "salary": [90000, 85000, 70000, 75000, 92000],
})

# BUG: group_by().agg() collapses the DataFrame to one row per department;
# BUG: to add a per-employee column showing each person's department mean,
# BUG: use pl.col("salary").mean().over("dept") inside with_columns() instead
result = df.group_by("dept").agg(pl.col("salary").mean().alias("dept_mean"))
print(f"input rows: {len(df)}, output rows: {len(result)}")
print(result)
