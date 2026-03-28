import altair as alt
import polars as pl

data = pl.DataFrame({
    "month": ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05"],
    "sales": [120, 95, 140, 110, 160],
}).to_pandas()

# BUG: encoding the month column as "nominal" instead of "temporal" causes
# BUG: Altair to sort alphabetically rather than chronologically, and the line
# BUG: segments are drawn in the wrong order
chart = alt.Chart(data).mark_line(point=True).encode(
    x=alt.X("month:N"),
    y=alt.Y("sales:Q"),
)
chart.save("temporal.html")
