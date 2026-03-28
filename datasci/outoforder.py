import polars as pl

# BUG: This script mimics a notebook that was run out of order.
# BUG: In the notebook, a cell that cleaned "raw" was executed before the cell
# BUG: that loaded it, so a stale "clean" DataFrame (from a previous run) was
# BUG: used instead of the freshly loaded one.

raw = pl.read_csv("filterboundary.csv")

# BUG: "clean" is defined here as if it came from a prior notebook cell;
# BUG: running this script top-to-bottom will fail with a NameError because
# BUG: "clean" has not been assigned yet at the point it is used below
# BUG: (in the notebook the stale in-memory value masked this dependency gap)
summary = clean.group_by("product").agg(pl.col("value").mean())  # noqa: F821

clean = raw.filter(pl.col("value") > 40)

print(summary)
