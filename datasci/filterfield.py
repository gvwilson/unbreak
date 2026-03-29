import altair as alt
import polars as pl

data = pl.DataFrame({
    "category": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "count": [50, 120, 30, 200, 80, 15, 175, 60, 90, 140, 25],
}).to_pandas()

# Show only categories with count >= 100.

# BUG: the filter references "Count" (capital C) but the field is "count"
# BUG: (lowercase); Altair silently ignores transforms on unknown fields, so all
# BUG: categories are shown
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X("category:N"),
    y=alt.Y("count:Q"),
).transform_filter(
    alt.datum.Count >= 100
)
chart.save("filterfield.html")
