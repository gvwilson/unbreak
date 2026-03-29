import altair as alt
import polars as pl

data = pl.DataFrame({
    "region": ["North", "South", "East", "North", "South", "East"],
    # BUG: year is stored as Float64 because Polars inferred it from a CSV
    # BUG: with a missing value; Altair treats each unique float as a distinct
    # BUG: nominal facet key, but the layout collapses to one panel
    "year": [2022.0, 2022.0, 2022.0, 2023.0, 2023.0, 2023.0],
    "sales": [100, 150, 120, 130, 160, 140],
}).to_pandas()

chart = alt.Chart(data).mark_bar().encode(
    x=alt.X("region:N"),
    y=alt.Y("sales:Q"),
).facet(
    facet="year:N",
    columns=2,
)
chart.save("floatyear.html")
