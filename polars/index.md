# Polars

## Add a computed column to a DataFrame {: #polars-selectdrop}

Run the script and look at the columns in the result. How many columns does it
have? How many columns did the original DataFrame have?

[% inc selectdrop.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `.select()` to add a new column. `.select()` returns only the
columns listed in the call and drops all others, so `id` and `name` are lost.

Shows: the difference between `.select()` (choose columns) and `.with_columns()`
(add or replace columns while keeping the rest).

To find it: print `result.columns` and compare to `df.columns`. If the result
has fewer columns than the original, `.select()` dropped them. Find the `.select()`
call in the pipeline and replace it with `.with_columns()`.

</details>

## Filter and select rows from a dataset {: #polars-nocollect}

Run the script and look at what is printed. Is the output a table of data, or
something else? What type does `type(result)` report?

[% inc nocollect.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `.lazy()` to start a lazy pipeline but never calling `.collect()`
at the end, so the result is a `LazyFrame` (a query plan) rather than a `DataFrame`.
The filter and select have not executed.

Shows: the difference between eager and lazy evaluation in Polars and
when `.collect()` is required.

To find it: add `print(type(result))` after the pipeline. Seeing
`<class 'polars.LazyFrame'>` instead of `<class 'polars.DataFrame'>` confirms the
pipeline never executed. Add `.collect()` at the end of the chain.

</details>

## Find rows with missing scores {: #polars-nullequal}

Run the script. How many rows does it print? How many rows contain a missing score?

[% inc nullequal.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `== None` to test for missing values. In Polars, any comparison
involving null yields null rather than a boolean, so every row in the filtered
result is null and the filter keeps nothing.

Shows: null semantics in Polars and how to use `.is_null()` to
correctly select rows where a value is missing.

To find it: print `df["score"].is_null().sum()` to count actual nulls, then
compare to `len(result)` after the filter. If the filter returns 0 rows but the
null count is positive, the comparison `== None` is the problem — replace it with
`.is_null()`.

</details>

## Convert float scores to integers {: #polars-castsilent}

Run the script and compare the values in the `score` column to the expected rounded
values printed below them. What happened to 88.7 and 95.6?

[% inc castsilent.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `cast(pl.Int64)` truncates toward zero rather than rounding, so
88.7 becomes 88 and 95.6 becomes 95 instead of 89 and 96. No error is raised.

Shows: that integer casting in Polars is a truncation operation, and
how to use `.round(0).cast(pl.Int64)` when rounding behavior is
intended.

To find it: print `df.select(pl.col("score")`,
`pl.col("score").round(0).cast(pl.Int64).alias("rounded")`,
and `pl.col("score").cast(pl.Int64).alias("truncated"))`.
For a value like 88.7, the `rounded` column shows 89 and the `truncated` column
shows 88. The mismatch reveals that `.cast()` alone is discarding the fractional
part rather than rounding.

</details>

## Add a department average salary to each employee row {: #polars-overwindow}

Run the script. How many rows does the output have? How many rows did you expect?

[% inc overwindow.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `group_by().agg()` when the goal is to add a per-row column showing
each employee's department mean. `group_by().agg()` collapses the DataFrame to one row
per group.

Shows: the difference between aggregation (which reduces rows) and
window functions (which compute a value per row), and how to use
`.over()` inside `.with_columns()` to attach group statistics to every
row.

To find it: print `len(result)` and compare to `len(df)`. If the result has one
row per department instead of one per employee, `group_by().agg()` collapsed the
rows. Replace the `group_by().agg()` pipeline with
`.with_columns(pl.col("salary").mean().over("department").alias("dept_avg"))`.

</details>

## Join orders to customer records {: #polars-innerjoin}

Run the script and compare the number of input orders to the number of rows in the
result. Which order is missing, and why?

[% inc innerjoin.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using the default join, which is inner. Order 4 has a `customer_id` of 99
that does not appear in the customers table, so it is silently dropped.

Shows: the difference between inner and left joins, how to specify
`how="left"` to retain all rows from the left table, and how to verify
row counts before and after a join.

To find it: print `len(orders)` before the join and `len(result)` after. If they
differ, rows were dropped. To identify which, print
`orders["customer_id"].is_in(customers["customer_id"]).value_counts()`. Any
`False` entries name the customer IDs that have no match and will be lost in an
inner join.

</details>

## Add a total price column to an order table {: #polars-aliasexpr}

Run the script and compare the column names and values to the original DataFrame.
Which column was overwritten, and which column was supposed to be added?

[% inc aliasexpr.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is omitting `.alias()` on the expression. Without an explicit name, Polars
assigns the column the name of the left operand (`"price"`), which silently replaces
the original `price` column with the product values instead of adding a new `total`
column.

Shows: how Polars names unnamed expressions and why `.alias()` is
needed whenever the result should have a different name from its
inputs.

To find it: print `result.columns` and `result.head()`. If the `price` column now
contains the product of `price * quantity` rather than unit prices, the expression
was assigned back to `price` rather than creating a new column. Add
`.alias("total")` to the expression inside `.with_columns()`.

</details>

## Parse dates from a CSV file {: #polars-strptime}

Run the script and look at the parsed `date` column. Is `"03/04/2024"` shown as
April 3rd or March 4th? What date was intended?

[% inc strptime.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a mismatch between the data order (day/month/year) and the format string
(`%m/%d/%Y`, month/day/year). Because all day and month values are 12 or below,
every date parses without error, but each one is wrong.

Shows: how ambiguous numeric date formats cause silent data
corruption, and why checking a few parsed values against known inputs
is necessary to confirm the format string is correct.

To find it: print the first few rows of the parsed `date` column alongside the
original string values. Find a row where the day value is greater than 12 (for
example, `"15/04/2024"`) and check whether the parsed month is 15 or the parsed
day is 15. Only one interpretation is possible, and it immediately reveals whether
`%d` and `%m` are swapped in the format string.

</details>

## Split a tags column into one row per tag {: #polars-explodestring}

Run the script and read the error message. What type does Polars report for the
`tags` column?

[% inc explodestring.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `.explode()` on a column that contains plain strings rather than
lists. Polars raises an `InvalidOperationError` because `.explode()` requires a
list-type column.

Shows: how to convert a delimited string column into a list column
with `.str.split()` before calling `.explode()`, and how to check
column types with `.schema` before applying list operations.

To find it: print `df.schema` and check the type of the `tags` column. Seeing
`String` instead of `List[String]` explains the `InvalidOperationError`:
`.explode()` requires a list-type column. Add
`.with_columns(pl.col("tags").str.split(", "))` before the `.explode()` call.

</details>

## Compute a discounted price and order total in one step {: #polars-withcolumnsdep}

Run the script and read the error message. Which column is reported as not found?
Is that column present in the original DataFrame?

[% inc withcolumnsdep.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is referencing `discounted_price` in the same `.with_columns()` call where
it is first computed. All expressions in a single `.with_columns()` call are
evaluated against the original DataFrame, so `discounted_price` does not yet exist
when `total` is computed, and Polars raises a `ColumnNotFoundError`.

Shows: how Polars evaluates expressions in parallel within one call
and how to chain two separate `.with_columns()` calls when one result
depends on another.

To find it: read the `ColumnNotFoundError`, which names `discounted_price` as
missing. Search the code for where `discounted_price` is created and where it is
referenced. If both appear in the same `.with_columns()` call, split them: put
the expression that creates `discounted_price` in one `.with_columns()` call and
the expression that uses it in a second chained call.

</details>
