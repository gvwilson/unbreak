import altair as alt
import polars as pl

df = pl.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 25, 15, 30, 20],
})

# BUG: alt.Chart() does not accept a Polars DataFrame directly; the chart
# BUG: renders blank because Altair cannot read Polars' internal format;
# BUG: convert with df.to_pandas() or wrap in alt.Data first
chart = alt.Chart(df).mark_line().encode(
    x="x:Q",
    y="y:Q",
)
chart.save("polarsinaltair.html")
