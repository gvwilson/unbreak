# Data Science

## Select rows within a date range {: #datasci-filterboundary}

Run the script and count the rows returned. Then count by hand how many rows in the
CSV should satisfy the condition. Do the two counts agree?

[% inc filterboundary.py scrub="\s*# BUG.*" %]
[% inc filterboundary.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `>=` instead of `>` (or vice versa) in the filter expression, so
the script keeps rows it should drop.

Shows: how to verify filter logic by checking boundary values and
using `.filter()` with explicit comparison operators.

To find it: count the matching rows by hand from the CSV, then compare to
`print(len(df.filter(...)))`. If the counts differ by one, check whether the boundary
date itself should be included or excluded, and verify whether `>=` or `>` is correct.

</details>

## Read a spreadsheet with a two-row header {: #datasci-multilinecsv}

Run the script and look at the row count and the first few rows of the DataFrame.
Do they match the data you expected to load?

[% inc multilinecsv.py scrub="\s*# BUG.*" %]
[% inc multilinecsv.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is not passing `skip_rows` to skip the extra header lines, so Polars reads
the multi-line header as data and reports the wrong number of rows.

Shows: how to inspect the first few rows of a DataFrame with `.head()`
and how to use `skip_rows` and `has_header` to handle non-standard
file layouts.

To find it: print `df.head()` and compare the first few rows to the raw CSV. If the
first "data" row contains what looks like a column header, the loader read one or
more header lines as data. Check `df.shape[0]` against the expected row count.

</details>

## Combine two datasets on a shared identifier {: #datasci-casejoin}

Run the script and examine the `mean_amount` column in the result. Are there any
null values where you did not expect them?

[% inc casejoin.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is joining on a column whose name differs by case (`"Region"` vs.
`"region"`), which Polars treats as different columns, so every row in the joined
output has a null for the group mean.

Shows: that Polars column names are case-sensitive and how to diagnose
null-filled join results.

To find it: print `df1.columns` and `df2.columns` side by side. Look for a column
that appears in both but differs by capitalization. A join on mismatched names
produces a null-filled column for the unmatched side.

</details>

## Sort records by date of collection {: #datasci-datestring}

Run the script and check the schema of the DataFrame. What type does Polars assign
to the `date` column? How many rows does the filter return?

[% inc datestring.py scrub="\s*# BUG.*" %]
[% inc datestring.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that Polars read the date column as strings, so the comparison is
lexicographic rather than chronological and the filter returns no rows even though
matching rows exist.

Shows: how to inspect inferred column types with `.schema`, and how to
cast a column to `pl.Date` before filtering.

To find it: print `df.schema` and check the type of the date column. If it shows
`String` instead of `Date`, comparisons against a `datetime` value will return no
rows because string comparison is lexicographic, not chronological.

</details>

## Compute per-group statistics before filtering {: #datasci-aggorder}

Run the script and compare the output totals to the values in the CSV file. Do the
per-region totals make sense?

[% inc aggorder.py scrub="\s*# BUG.*" %]
[% inc aggorder.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `.sum()` before `.group_by()`, which sums the entire column first
and then groups a single-row DataFrame, producing unexpectedly large totals.

Shows: the importance of operation order in lazy and eager pipelines
and how to verify intermediate results.

To find it: break the pipeline into two steps and print the DataFrame after each one.
After `.sum()` alone, you will see a single-row DataFrame — the sum already happened
before grouping.

</details>

## Debug a pipeline that fails at the wrong step {: #datasci-lazyerror}

Run the script and read the error message and traceback. Which step in the pipeline
does the error appear to come from? Is that where the mistake actually is?

[% inc lazyerror.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is referencing a column that was renamed in an earlier step, so a
`ColumnNotFoundError` is raised at `.collect()` time rather than when the
transformation is written.

Shows: how Polars lazy evaluation defers errors and how to use
`.collect()` on intermediate steps to locate the failing
transformation.

To find it: insert `.collect()` after each transformation step and run the script
again. The first step where `.collect()` raises a `ColumnNotFoundError` is where
the broken reference is — even though the original error appeared only at the final
`.collect()`.

</details>

## Read a tab-separated export from a database {: #datasci-wrongdelim}

Run the script and examine the column names and values in the combined DataFrame.
Are the columns what you expected?

[% inc wrongdelim.py scrub="\s*# BUG.*" %]
[% inc wrongdelim_a.csv %]
[% inc wrongdelim_b.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the second file uses semicolons as delimiters, so Polars reads the
entire row as a single column. When `concat` is called with `how="diagonal"`, missing
columns are filled with nulls and the result has twice as many columns as expected.

Shows: how to check column names and counts before concatenating
DataFrames.

To find it: print `df1.columns` and `df2.columns` before the concat. If `df2` has
one column whose name looks like an entire row — e.g., `"id;name;value"` — the file
uses a different delimiter than the one specified.

</details>

## Average measurements that include missing values {: #datasci-sentinel}

Run the script and look at the mean. Then inspect the raw data. Are there any
values in the column that seem unusually large?

[% inc sentinel.py scrub="\s*# BUG.*" %]
[% inc sentinel.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the dataset uses `999` as a sentinel for missing data rather than a
true null, so `.fill_null()` has no effect on them and the mean is skewed by what
appear to be valid large numbers.

Shows: how to identify domain-specific sentinel values and replace
them with `pl.Null` before analysis.

To find it: print `df["measurement"].max()`. A suspiciously round large value like
`999` in a column of biological measurements is a sentinel for "not recorded," not
a real reading. Replace it with `pl.Null` before computing the mean.

</details>

## Group survey responses by category {: #datasci-whitespace}

Run the script and count the number of groups produced. Is it more than you
expected? Call `.unique()` on the grouping column and examine what you see.

[% inc whitespace.py scrub="\s*# BUG.*" %]
[% inc whitespace.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that a string column has inconsistent whitespace (e.g., `"North "` and
`"North"` are treated as different groups), so `group_by` followed by `agg` produces
more groups than expected.

Shows: how to inspect unique values with `.unique()`, use
`.str.strip_chars()` to normalize strings before grouping, and verify
group counts.

To find it: print `df["category"].unique()` and count the items. If you see
`"North"` and `"North "` as separate entries, trailing whitespace is causing the
split.

</details>

## Smooth a noisy sensor signal {: #datasci-rolling}

Run the script and count the null values in the `rolling_mean` column. Is the
number of null rows what you expected for a 7-day window?

[% inc rolling.py scrub="\s*# BUG.*" %]
[% inc rolling.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is passing `window_size=7` without setting `min_periods=1`, so any window
that cannot be fully filled returns null and the result has far more nulls than
expected.

Shows: how rolling aggregations handle incomplete windows and how to
choose between strict and lenient behavior with `min_periods`.

To find it: print `df["rolling_mean"].is_null().sum()` to count null values. If the
count is much larger than `window_size - 1`, the window requires more data points
than are available for most positions. Setting `min_periods=1` allows partial windows
to produce a result.

</details>

## Plot measurement values on a scatter chart {: #datasci-quanttype}

Run the script and open the saved chart in a browser. Do all the bars have heights
that reflect the `value` column?

[% inc quanttype.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is encoding the y-axis with `alt.Y("value")` without specifying
`type="quantitative"`, so Altair treats the column as nominal and counts categories
instead of summing values, giving all bars the same height.

Shows: how Altair infers encoding types and why specifying `type`
explicitly avoids silent misinterpretation.

To find it: open the chart and count the unique bar heights. If every bar is the same
height, Altair is counting rows rather than summing values. Call
`alt.Chart(data).mark_bar().encode(y="value").to_dict()` and search for `"type"` in
the output to see what Altair inferred.

</details>

## Color a chart by a numeric category {: #datasci-colorscale}

Run the script and open the saved chart. Does the color scale appear as a
continuous gradient, or as a discrete set of colors?

[% inc colorscale.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the color column was read as a string (e.g., `"3.5"`) rather than a
float, so Altair applies a nominal color scale and the scatter plot shows a discrete
legend with arbitrary colors instead of a continuous gradient.

Shows: how data types in the source DataFrame determine Altair's
default encoding choices.

To find it: print `df.schema` and check the type of the color column. If it shows
`String` instead of `Float64`, cast it with `.cast(pl.Float64)` before charting.

</details>

## Plot measurements collected over time {: #datasci-temporal}

Open the saved chart in a browser. Are the months arranged in chronological order
along the x-axis, or in a different order?

[% inc temporal.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is encoding the x-axis date column as `type="nominal"` instead of
`type="temporal"`, so Altair does not order the points chronologically and the line
chart draws disconnected segments instead of a continuous line.

Shows: the difference between nominal and temporal encoding in Altair
and how to verify axis ordering.

To find it: open the chart and check whether the x-axis dates are in chronological
order. If months appear alphabetically — e.g., April before August before December —
rather than in calendar order, check the `alt.X(...)` call for `type=`.

</details>

## Add an interactive filter to a chart {: #datasci-filterfield}

Open the saved chart in a browser. Does it show only the categories whose count
is 100 or more, or does it show all of them?

[% inc filterfield.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a field name in `alt.Filter` that does not match any column. Altair
silently ignores the filter rather than raising an error, so all categories are
shown instead of just the top 10.

Shows: how to debug Altair transforms by inspecting the chart's JSON
specification and checking field names match the data source.

To find it: call `.to_dict()` on the chart and search for the field name inside the
`transform` section. Compare it character by character to the actual column name in
the DataFrame — a one-character difference silently disables the filter.

</details>

## Show column values in a chart tooltip {: #datasci-tooltip}

Open the saved chart in a browser and hover over a point. Does the `Sales Region`
field in the tooltip show a value?

[% inc tooltip.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the tooltip field name has a space in it (e.g., `"Sales Region"`)
but is referenced without quoting in the Altair shorthand string, so the tooltip
shows `null` for that field even though the data contains values.

Shows: how Altair shorthand handles special characters and when to use
`alt.Tooltip(field=…, title=…)` instead.

To find it: hover over a point in the chart and note which tooltip field shows
`null`. Then print `df.columns` to find the exact column name. If the name contains
a space, the Altair shorthand parser stops at the space and the field is never
matched.

</details>

## Pass a Polars dataframe to a chart library {: #datasci-polarsinaltair}

Run the script and open the saved chart in a browser. Does the chart show any data
points?

[% inc polarsinaltair.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is passing the Polars DataFrame directly to `alt.Chart()` instead of
converting it to a pandas DataFrame or using `alt.Data`, so the chart is blank.

Shows: which data formats Altair accepts natively and how to convert
between Polars and the formats Altair supports.

To find it: print `type(df)` to confirm it is a Polars `DataFrame`, then open the
chart — if it is blank, Altair did not receive a supported data format. Convert with
`df.to_pandas()` and open the chart again.

</details>

## Check whether two measurements are related {: #datasci-spurcorr}

Run the script and note the correlation value. Then examine how `metric_a` and
`metric_b` are constructed. Should they really be perfectly correlated?

[% inc spurcorr.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that both columns were derived from the same source column in the same
pipeline step (a copy rather than an independent transformation), so the correlation
is exactly 1.0 for columns that should not be perfectly correlated.

Shows: how to audit column provenance in a pipeline and use scatter
plots to sanity-check correlation claims.

To find it: print the expression used to create each column side by side. If both
are derived from `df["x"]` in the same step, they are the same data. A scatter plot
of `metric_a` vs. `metric_b` that falls on a perfect diagonal confirms it.

</details>

## Process a large file in pieces {: #datasci-chunkaccum}

Run the script on a large file and watch how memory usage changes as the script
runs. Does memory stay roughly constant, or does it grow?

[% inc chunkaccum.py scrub="\s*# BUG.*" %]
[% inc chunkaccum.csv %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is accumulating all chunks in memory before concatenating rather than
processing each chunk and writing results incrementally, so the pipeline runs out of
memory on large files.

Shows: streaming versus batch processing patterns and how to use
Polars' `scan_csv` with lazy evaluation to avoid loading the full
file.

To find it: add `import tracemalloc; tracemalloc.start()` at the top and print
`tracemalloc.get_traced_memory()` after processing each chunk. If the peak figure
grows linearly with the number of chunks, the chunks are being accumulated in memory
rather than discarded after each step.

</details>

## Facet a chart by year of collection {: #datasci-floatyear}

Open the saved chart in a browser. How many facet panels does it show? Inspect the
type of the `year` column in the DataFrame.

[% inc floatyear.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the year column contains floats (e.g., `2021.0`) because Polars
inferred it as `Float64`. Altair's facet treats each unique float as a separate
nominal value but the layout collapses to one panel due to the unexpected type.

Shows: how to cast integer-like columns to `pl.Int32` before charting
and how to verify facet behavior with a small sample.

To find it: print `df["year"].dtype` and `df["year"].unique()`. If the type is
`Float64` and the values show `.0` suffixes, cast the column with `.cast(pl.Int32)`
before passing to Altair.

</details>

## Run a notebook after restarting the kernel {: #datasci-outoforder}

Run this script from top to bottom. Does it raise an error? Which line causes the
error?

[% inc outoforder.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the notebook had cells executed out of order, leaving a modified
DataFrame in memory that masked an error in the cleaning step. The script produces
correct results when run step by step in a notebook but wrong results when run as a
script.

Shows: why notebooks must be tested by restarting the kernel and
running all cells in order, and how to structure pipelines so each
step depends only on its explicit inputs.

To find it: run the script as a plain Python file from a fresh process (not inside a
notebook). If it raises an error that never appeared during interactive execution,
a cell was run out of order. Add `print(df.columns)` at the start of each step to
confirm each step's input matches what the previous step produced.

</details>
