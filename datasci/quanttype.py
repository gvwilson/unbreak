import altair as alt
import polars as pl

data = pl.DataFrame({
    "category": ["A", "B", "C", "D"],
    "value": [10, 40, 25, 60],
}).to_pandas()

# BUG: y encoding has no type= specified; Altair defaults to treating "value"
# BUG: as nominal and counts categories rather than using the numeric values
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X("category"),
    y=alt.Y("value"),
)
chart.save("quanttype.html")
