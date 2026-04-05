# Polars

## select Drops Unlisted Columns {: #polars-selectdrop}

Run the script and look at the columns in the result. How many columns does it
have? How many columns did the original DataFrame have?

[% inc selectdrop.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `.select()` to add a new column. `.select()` returns only the
columns listed in the call and drops all others, so `id` and `name` are lost.
Teaches the difference between `.select()` (choose columns) and `.with_columns()`
(add or replace columns while keeping the rest).

</details>

## Lazy Frame Never Collected {: #polars-nocollect}

Run the script and look at what is printed. Is the output a table of data, or
something else? What type does `type(result)` report?

[% inc nocollect.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `.lazy()` to start a lazy pipeline but never calling `.collect()`
at the end, so the result is a `LazyFrame` (a query plan) rather than a `DataFrame`.
The filter and select have not executed. Teaches the difference between eager and
lazy evaluation in Polars and when `.collect()` is required.

</details>

## Null Comparison with == None {: #polars-nullequal}

Run the script. How many rows does it print? How many rows contain a missing score?

[% inc nullequal.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `== None` to test for missing values. In Polars, any comparison
involving null yields null rather than a boolean, so every row in the filtered
result is null and the filter keeps nothing. Teaches null semantics in Polars and
how to use `.is_null()` to correctly select rows where a value is missing.

</details>

## Silent Null on Cast Failure {: #polars-castsilent}

Run the script and check the null count it prints. Did the cast raise an error for
the row that contained `"N/A"`?

[% inc castsilent.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is passing `strict=False` to `cast()`. This tells Polars to convert any value
it cannot parse to null rather than raising an error, so the bad value `"N/A"`
disappears into the data without warning. Teaches how to inspect null counts after a
cast to detect silent data loss, and why removing `strict=False` (or setting
`strict=True` explicitly) is safer when the input is expected to be clean.

</details>

## group_by Collapses Rows {: #polars-overwindow}

Run the script. How many rows does the output have? How many rows did you expect?

[% inc overwindow.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `group_by().agg()` when the goal is to add a per-row column showing
each employee's department mean. `group_by().agg()` collapses the DataFrame to one row
per group. Teaches the difference between aggregation (which reduces rows) and window
functions (which compute a value per row), and how to use `.over()` inside
`.with_columns()` to attach group statistics to every row.

</details>

## Default Inner Join Drops Rows {: #polars-innerjoin}

Run the script and compare the number of input orders to the number of rows in the
result. Which order is missing, and why?

[% inc innerjoin.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using the default join, which is inner. Order 4 has a `customer_id` of 99
that does not appear in the customers table, so it is silently dropped. Teaches the
difference between inner and left joins, how to specify `how="left"` to retain all
rows from the left table, and how to verify row counts before and after a join.

</details>

## Missing alias on Computed Column {: #polars-aliasexpr}

Run the script and compare the column names and values to the original DataFrame.
Which column was overwritten, and which column was supposed to be added?

[% inc aliasexpr.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is omitting `.alias()` on the expression. Without an explicit name, Polars
assigns the column the name of the left operand (`"price"`), which silently replaces
the original `price` column with the product values instead of adding a new `total`
column. Teaches how Polars names unnamed expressions and why `.alias()` is needed
whenever the result should have a different name from its inputs.

</details>

## Wrong Date Format String {: #polars-strptime}

Run the script and check the null count it prints. How many dates were successfully
parsed? Examine the format string and compare it to the actual date values.

[% inc strptime.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a format string that does not match the data. The dates are formatted as
`YYYY-MM-DD` but the format string specifies `%d/%m/%Y` (day/month/year with
slashes). Because `strict=False` is set, every parse fails silently and the result
is a column of nulls with no error message. Teaches how to verify format strings
against sample values and how removing `strict=False` (letting Polars raise on
failure) catches this mistake immediately.

</details>

## explode on a String Column {: #polars-explodestring}

Run the script and read the error message. What type does Polars report for the
`tags` column?

[% inc explodestring.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `.explode()` on a column that contains plain strings rather than
lists. Polars raises an `InvalidOperationError` because `.explode()` requires a
list-type column. Teaches how to convert a delimited string column into a list
column with `.str.split()` before calling `.explode()`, and how to check column
types with `.schema` before applying list operations.

</details>

## Cross-Reference in One with_columns Call {: #polars-withcolumnsdep}

Run the script and read the error message. Which column is reported as not found?
Is that column present in the original DataFrame?

[% inc withcolumnsdep.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is referencing `discounted_price` in the same `.with_columns()` call where
it is first computed. All expressions in a single `.with_columns()` call are
evaluated against the original DataFrame, so `discounted_price` does not yet exist
when `total` is computed, and Polars raises a `ColumnNotFoundError`. Teaches how
Polars evaluates expressions in parallel within one call and how to chain two
separate `.with_columns()` calls when one result depends on another.

</details>
