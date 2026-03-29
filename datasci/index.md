# Data Science

## Filter Boundary Condition {: #datasci-filterboundary}

Run the script and count the rows returned. Then count by hand how many rows in the
CSV should satisfy the condition. Do the two counts agree?

[% inc filterboundary.py scrub="\s*# BUG.*" %]
[% inc filterboundary.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A data cleaning script reads a CSV file into a Polars DataFrame and filters rows
where a numeric column exceeds a threshold, but keeps rows it should drop; the bug
is using `>=` instead of `>` (or vice versa) in the filter expression. Teaches how
to verify filter logic by checking boundary values and using `.filter()` with
explicit comparison operators.

</details>

## Multi-Line CSV Header {: #datasci-multilinecsv}

Run the script and look at the row count and the first few rows of the DataFrame.
Do they match the data you expected to load?

[% inc multilinecsv.py scrub="\s*# BUG.*" %]
[% inc multilinecsv.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script loads a dataset with a Polars `read_csv` call and reports the wrong number
of rows because the CSV has a multi-line header that Polars reads as data; the bug
is not passing `skip_rows` to skip the extra header lines. Teaches how to inspect
the first few rows of a DataFrame with `.head()` and how to use `skip_rows` and
`has_header` to handle non-standard file layouts.

</details>

## Case-Sensitive Column Name in Join {: #datasci-casejoin}

Run the script and examine the `mean_amount` column in the result. Are there any
null values where you did not expect them?

[% inc casejoin.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A Polars pipeline computes a per-group mean and then joins the result back to the
original DataFrame, but every row in the joined output has a null for the group
mean; the bug is joining on a column whose name differs by case (`"Region"` vs.
`"region"`), which Polars treats as different columns. Teaches that Polars column
names are case-sensitive and how to diagnose null-filled join results.

</details>

## Dates Read as Strings {: #datasci-datestring}

Run the script and check the schema of the DataFrame. What type does Polars assign
to the `date` column? How many rows does the filter return?

[% inc datestring.py scrub="\s*# BUG.*" %]
[% inc datestring.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that reads dates from a CSV file and filters for rows after a cutoff date
returns no rows even though matching rows exist; the bug is that Polars read the
date column as strings, so the comparison is lexicographic rather than chronological.
Teaches how to inspect inferred column types with `.schema`, and how to cast a
column to `pl.Date` before filtering.

</details>

## Aggregation Order Error {: #datasci-aggorder}

Run the script and compare the output totals to the values in the CSV file. Do the
per-region totals make sense?

[% inc aggorder.py scrub="\s*# BUG.*" %]
[% inc aggorder.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A Polars aggregation computes the total sales per region but the totals are
unexpectedly large; the bug is calling `.sum()` before `.group_by()`, summing the
entire column first and then grouping a single-row DataFrame. Teaches the importance
of operation order in lazy and eager pipelines and how to verify intermediate results.

</details>

## Lazy Evaluation Defers Errors {: #datasci-lazyerror}

Run the script and read the error message and traceback. Which step in the pipeline
does the error appear to come from? Is that where the mistake actually is?

[% inc lazyerror.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script builds a Polars LazyFrame pipeline with several transformations and calls
`.collect()` at the end, but raises a `ColumnNotFoundError` at collection time
rather than when the transformation is written; the bug is referencing a column that
was renamed in an earlier step. Teaches how Polars lazy evaluation defers errors and
how to use `.collect()` on intermediate steps to locate the failing transformation.

</details>

## Wrong CSV Delimiter {: #datasci-wrongdelim}

Run the script and examine the column names and values in the combined DataFrame.
Are the columns what you expected?

[% inc wrongdelim.py scrub="\s*# BUG.*" %]
[% inc wrongdelim_a.csv %]
[% inc wrongdelim_b.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script uses `pl.concat` to stack two DataFrames loaded from different CSV files,
but the result has twice as many columns as expected; the bug is that the second
file uses semicolons as delimiters, so Polars reads the entire row as a single
column, and `concat` with `how="diagonal"` fills missing columns with nulls.
Teaches how to check column names and counts before concatenating DataFrames.

</details>

## Sentinel Values Mistaken for Data {: #datasci-sentinel}

Run the script and look at the mean. Then inspect the raw data. Are there any
values in the column that seem unusually large?

[% inc sentinel.py scrub="\s*# BUG.*" %]
[% inc sentinel.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A data pipeline replaces missing values in a column using `.fill_null()` and then
computes statistics, but the mean is still skewed by what appear to be valid large
numbers; the bug is that the dataset uses `999` as a sentinel for missing data
rather than a true null, so `.fill_null()` has no effect on them. Teaches how to
identify domain-specific sentinel values and replace them with `pl.Null` before
analysis.

</details>

## Whitespace in Group Keys {: #datasci-whitespace}

Run the script and count the number of groups produced. Is it more than you
expected? Call `.unique()` on the grouping column and examine what you see.

[% inc whitespace.py scrub="\s*# BUG.*" %]
[% inc whitespace.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A Polars `group_by` followed by `agg` produces a different number of groups than
expected; the bug is that a string column has inconsistent whitespace (e.g.,
`"North "` and `"North"` are treated as different groups). Teaches how to inspect
unique values with `.unique()`, use `.str.strip_chars()` to normalize strings before
grouping, and verify group counts.

</details>

## Rolling Window min_periods {: #datasci-rolling}

Run the script and count the null values in the `rolling_mean` column. Is the
number of null rows what you expected for a 7-day window?

[% inc rolling.py scrub="\s*# BUG.*" %]
[% inc rolling.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script uses a Polars window function to compute a 7-day rolling mean, but the
result has nulls for far more rows than expected; the bug is passing `window_size=7`
without setting `min_periods=1`, so any window that cannot be fully filled returns
null. Teaches how rolling aggregations handle incomplete windows and how to choose
between strict and lenient behavior with `min_periods`.

</details>

## Missing Quantitative Encoding Type {: #datasci-quanttype}

Run the script and open the saved chart in a browser. Do all the bars have heights
that reflect the `value` column?

[% inc quanttype.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A Vega-Altair chart displays all bars at the same height even though the data
values differ; the bug is encoding the y-axis with `alt.Y("value")` without
specifying `type="quantitative"`, so Altair treats the column as nominal and counts
categories instead of summing values. Teaches how Altair infers encoding types and
why specifying `type` explicitly avoids silent misinterpretation.

</details>

## Color Scale from String Column {: #datasci-colorscale}

Run the script and open the saved chart. Does the color scale appear as a
continuous gradient, or as a discrete set of colors?

[% inc colorscale.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A Vega-Altair scatter plot intended to show a color gradient for a continuous
variable instead shows a discrete legend with arbitrary colors; the bug is that the
color column was read as a string (e.g., `"3.5"`) rather than a float, and Altair
applies a nominal color scale to string columns. Teaches how data types in the
source DataFrame determine Altair's default encoding choices.

</details>

## Nominal vs. Temporal Encoding {: #datasci-temporal}

Open the saved chart in a browser. Are the months arranged in chronological order
along the x-axis, or in a different order?

[% inc temporal.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A Vega-Altair line chart connecting monthly data points draws disconnected segments
instead of a continuous line; the bug is that the x-axis date column is encoded as
`type="nominal"` instead of `type="temporal"`, so Altair does not order the points
chronologically. Teaches the difference between nominal and temporal encoding in
Altair and how to verify axis ordering.

</details>

## Altair Filter on Wrong Field {: #datasci-filterfield}

Open the saved chart in a browser. Does it show only the categories whose count
is 100 or more, or does it show all of them?

[% inc filterfield.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A Vega-Altair bar chart meant to show the top 10 categories by count shows all
categories because the filtering was done with `alt.Filter` on the wrong field name;
the bug is a field name that does not match any column, which Altair silently ignores
rather than raising an error. Teaches how to debug Altair transforms by inspecting
the chart's JSON specification and checking field names match the data source.

</details>

## Tooltip Field with Spaces {: #datasci-tooltip}

Open the saved chart in a browser and hover over a point. Does the `Sales Region`
field in the tooltip show a value?

[% inc tooltip.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A Vega-Altair chart with an interactive tooltip shows `null` for one field in the
tooltip even though the data contains values; the bug is that the tooltip field name
has a space in it (e.g., `"Sales Region"`) but is referenced without quoting in the
Altair shorthand string. Teaches how Altair shorthand handles special characters
and when to use `alt.Tooltip(field=..., title=...)` instead.

</details>

## Polars DataFrame in Altair {: #datasci-polarsinaltair}

Run the script and open the saved chart in a browser. Does the chart show any data
points?

[% inc polarsinaltair.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script builds a Polars DataFrame from a Python list of dictionaries and then
creates an Altair chart from it, but the chart is blank; the bug is passing the
Polars DataFrame directly to `alt.Chart()` instead of converting it to a pandas
DataFrame or using `alt.Data`. Teaches which data formats Altair accepts natively
and how to convert between Polars and the formats Altair supports.

</details>

## Spurious Perfect Correlation {: #datasci-spurcorr}

Run the script and note the correlation value. Then examine how `metric_a` and
`metric_b` are constructed. Should they really be perfectly correlated?

[% inc spurcorr.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A data analysis script computes a correlation between two columns and gets a value
of exactly 1.0 for columns that should not be perfectly correlated; the bug is that
both columns were derived from the same source column in the same pipeline step
(a copy rather than an independent transformation). Teaches how to audit column
provenance in a pipeline and use scatter plots to sanity-check correlation claims.

</details>

## Memory from Chunk Accumulation {: #datasci-chunkaccum}

Run the script on a large file and watch how memory usage changes as the script
runs. Does memory stay roughly constant, or does it grow?

[% inc chunkaccum.py scrub="\s*# BUG.*" %]
[% inc chunkaccum.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A Polars pipeline reads a large CSV file in chunks and appends each chunk to a list
before calling `pl.concat`, but runs out of memory; the bug is accumulating all
chunks in memory before concatenating, rather than processing each chunk and writing
results incrementally. Teaches streaming versus batch processing patterns and how
to use Polars' `scan_csv` with lazy evaluation to avoid loading the full file.

</details>

## Float Year in Faceted Chart {: #datasci-floatyear}

Open the saved chart in a browser. How many facet panels does it show? Inspect the
type of the `year` column in the DataFrame.

[% inc floatyear.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A Vega-Altair faceted chart intended to show one subplot per year shows only a
single chart; the bug is that the year column contains floats (e.g., `2021.0`)
because Polars inferred it as `Float64`, and Altair's facet treats each unique float
as a separate nominal value but the layout collapses to one panel due to the
unexpected type. Teaches how to cast integer-like columns to `pl.Int32` before
charting and how to verify facet behavior with a small sample.

</details>

## Out-of-Order Notebook Cells {: #datasci-outoforder}

Run this script from top to bottom. Does it raise an error? Which line causes the
error?

[% inc outoforder.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that automates a full data pipeline (loading, cleaning, aggregating, and
charting) produces correct results when run step by step in a notebook but wrong
results when run as a script. The bug is that the notebook had cells executed out
of order, leaving a modified DataFrame in memory that masked an error in the
cleaning step. Teaches why notebooks must be tested by restarting the kernel and
running all cells in order, and how to structure pipelines so each step depends only
on its explicit inputs.

</details>
