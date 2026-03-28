import altair as alt
import polars as pl

# Simulated dataset where "temperature" was read from a CSV as strings.
data = pl.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 15, 30, 25],
    # BUG: temperature values are strings (e.g. "3.5") instead of floats;
    # BUG: Altair applies a nominal (discrete) color scale to string columns
    "temperature": ["1.2", "2.4", "3.5", "4.1", "5.0"],
}).to_pandas()

chart = alt.Chart(data).mark_point().encode(
    x="x:Q",
    y="y:Q",
    color="temperature",
)
chart.save("colorscale.html")
