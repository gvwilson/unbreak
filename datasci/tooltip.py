import altair as alt
import polars as pl

data = pl.DataFrame({
    "Product Name": ["Widget", "Gadget", "Doohickey"],
    "Sales Region": ["North", "South", "East"],
    "revenue": [1200, 800, 950],
}).to_pandas()

# BUG: Altair shorthand "Sales Region" treats the space as a field-type
# BUG: separator; the tooltip shows null for this field instead of the region name
chart = alt.Chart(data).mark_point().encode(
    x=alt.X("revenue:Q"),
    tooltip=["Product Name:N", "Sales Region", "revenue:Q"],
)
chart.save("tooltip.html")
