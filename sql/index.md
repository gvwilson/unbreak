# SQL

[download databases](./databases.zip)

## Display records sorted by last name then first name {: #sql-sortcol}

Run this query and look at the first several rows. Is the output
ordered by island first, or by species first?

[% inc sortcol.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query meant to sort penguins by island and then by species within
each island produces species-first ordering instead; the bug is
listing the columns in the wrong order in the `order by` clause.

Shows: how `order by` applies columns from left to right and why
column order in that clause matters.

To find it: run the query and examine the first few rows. If all
`'Adelie'` rows appear before any `'Chinstrap'` rows regardless of
island, the sort is species-first. Compare the `order by` column
sequence to the intended priority.

</details>

## Retrieve the second page of search results {: #sql-offsetpage}

Run this query and note which rows are returned. Count from the
beginning of the full table to check whether rows 11-15 are actually
what you got.

[% inc offsetpage.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query meant to retrieve the third page of five rows returns rows 12-16 instead
of rows 11-15; the bug is using `offset 11` (which skips 11 rows) instead of
`offset 10`.

Shows: how `limit` and `offset` interact and how to calculate the
correct offset for a given page number.

To find it: add `rowid` to the `select` clause and run the query. If the first
returned row has `rowid = 12` but the page should start at row 11, the offset is
off by one. The formula is `(page_number - 1) * page_size`, so page 3 with
page size 5 gives `offset 10`.

</details>

## Calculate the average score per student {: #sql-intdivision}

Run this query and compare the `mass_kg` column to the `body_mass_g` column.
Do the kilogram values look right for a penguin that weighs, say, 3750 g?

[% inc intdivision.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that converts body mass from grams to kilograms silently truncates the
result because SQLite performs integer division when both operands are integers;
the bug is dividing by `1000` instead of `1000.0`.

Shows: how to force floating-point arithmetic in SQL and why checking
computed columns against known values catches this class of error.

To find it: run `select body_mass_g, body_mass_g / 1000 as mass_kg from penguins
limit 5`. A penguin weighing 3750 g should show `3.75` kg; if it shows `3`, integer
division is truncating the decimal. Change `1000` to `1000.0` and rerun.

</details>

## List unique participants in a study {: #sql-distinctcols}

Run this query and count the rows returned. How many distinct species are in the
dataset? Does the row count match that number?

[% inc distinctcols.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query intended to list the distinct species in the dataset returns seven rows
instead of three because `distinct` is applied to both `species` and `sex`,
producing one row per unique (species, sex) combination; the bug is including `sex`
in the `select` clause.

Shows: that `distinct` operates on the entire set of selected columns,
not on individual ones.

To find it: run `select count(*) from (select distinct species from penguins)`. If
that returns 3 but the original query returns 7, the extra column is what is
producing the extra rows.

</details>

## Find records with no assigned reviewer {: #sql-nullequal}

Run this query. How many rows does it return? Are there penguins in the table whose
sex was not recorded?

[% inc nullequal.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that tries to find penguins with no recorded sex returns zero rows because
comparing any value to `null` with `=` produces `null` (not `true`) in SQL's
ternary logic, so the `where` clause never passes; the bug is using `= null` instead
of `is null`.

Shows: SQL's three-valued logic and the two special tests `is null`
and `is not null`.

To find it: run `select count(*) from penguins where sex is null`. If that returns
a nonzero count but `where sex = null` returns zero, the `=` test is failing because
null comparisons always produce null, never `true`.

</details>

## Filter for records in two different categories {: #sql-impossibleand}

Run this query. How many rows does it return? Choose a penguin you know is on
Biscoe island from a previous query and check whether it appears here.

[% inc impossibleand.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should return penguins from either Biscoe or Dream island returns
zero rows because `and` requires both conditions to be true at the same time, but
a penguin can only be on one island; the bug is using `and` where `or` is needed.

Shows: the difference between `and` and `or` and how to spot
conditions that can never simultaneously be true.

To find it: ask whether a single penguin can be on Biscoe island and Dream island
at the same time. It cannot, so `AND` can never be true. Whenever a zero-row result
is unexpected, check whether the conditions are mutually exclusive.

</details>

## Query records by status label {: #sql-casevalue}

Run this query and count the rows returned. Then run a query to find the distinct
values stored in the `sex` column. Do any of them match the literal used in the
`where` clause?

[% inc casevalue.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should return all female penguins returns zero rows because the `sex`
column stores the value `'FEMALE'` in uppercase but the query filters on
`'female'` in lowercase; SQLite string comparisons are case-sensitive for non-ASCII
characters.

Shows: how to inspect the actual stored values before writing a filter
and how to use functions like `upper()` or `lower()` to normalise
comparisons.

To find it: run `select distinct sex from penguins` before writing the filter. If
the results show `'FEMALE'` in uppercase, a `where sex = 'female'` will return zero
rows because the literal does not match.

</details>

## Filter on a calculated column {: #sql-wherealiased}

Run this query. Does it raise an error or return wrong results? Add a second
`select` that uses the full expression `body_mass_g / 1000.0` in the `where`
clause and compare the two queries' output.

[% inc wherealiased.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that tries to filter using a column alias defined in the `select` clause
fails with a "no such column" error because SQL evaluates `where` before `select`,
so the alias does not yet exist at that point; the bug is referencing `mass_kg` in
`where` instead of repeating the full expression `body_mass_g / 1000.0`.

Shows: the order of SQL clause evaluation.

To find it: run the query and read the error: `no such column: mass_kg`. SQL
evaluates `where` before `select`, so the alias defined in `select` does not yet
exist when `where` runs. Replace the alias in `where` with the full expression
`body_mass_g / 1000.0`.

</details>

## Select records matching one of two conditions {: #sql-andorprecedence}

Run this query. Which species and islands appear in the result? Is the output what
you expected based on the comment describing the intent?

[% inc andorprecedence.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query intended to find Adelie or Chinstrap penguins that are on Biscoe island
instead returns all Adelie penguins from any island plus Chinstraps on Biscoe,
because `and` binds more tightly than `or`; the bug is missing parentheses around
the `or` sub-expression.

Shows: SQL operator precedence and why parentheses are needed to make
complex `where` conditions unambiguous.

To find it: run the query and check whether any Adelie penguins from non-Biscoe
islands appear in the result. If they do, `and` is binding more tightly than `or`
and the condition is being read as `species = 'Adelie' or (species = 'Chinstrap' and
island = 'Biscoe')`. Add parentheses around the `or` sub-expression.

</details>

## Summarize sales by region and product {: #sql-nonaggcol}

Run this query and examine the `sex` column. Pick one species and check a few rows
against the original data. Are the sex values consistent with what you expected
for that species group?

[% inc nonaggcol.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that groups by species but also selects `sex` without aggregating it
produces an arbitrary, unpredictable sex value for each species group because `sex`
is not in the `group by` clause; the bug is selecting a column that is neither
aggregated nor part of the grouping.

Shows: why every column in `select` must either appear in `group by`
or be wrapped in an aggregation function.

To find it: pick one species in the result and verify its `sex` value against the
original table. If the grouped query shows a single sex for the group but the raw
data contains both sexes for that species, the database is picking an arbitrary
value.

</details>

## Keep only groups above a minimum size {: #sql-wherenothavin}

Run this query. Does it return a result or raise an error? Check whether moving
the condition to a `having` clause after `group by` fixes the problem.

[% inc wherenothavin.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that tries to filter groups by their average value using `where` raises an
error because aggregate functions like `avg()` cannot appear in `where`; `where`
filters individual rows before grouping, while `having` filters groups after
aggregation; the bug is placing the condition in `where` instead of `having`.

Shows: the difference in timing between `where` and `having` in SQL's
execution order.

To find it: run the query and read the error message — something like `misuse of
aggregate function avg()`. Aggregate functions cannot appear in `where` because rows
haven't been grouped yet at that point. Move the condition to a `having` clause after
the `group by`.

</details>

## Count entries per category and subcategory {: #sql-groupbymissing}

Run this query and examine the `island` column. Do all the rows for a given species
show the same island? Check a few values against the original table.

[% inc groupbymissing.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that counts penguins per species per island produces unreliable island
values because `island` appears in `select` but not in `group by`, so the database
picks an arbitrary island for each species group; the bug is omitting `island` from
the `group by` clause.

Shows: that every non-aggregated column in `select` must also appear
in `group by`.

To find it: run the query and note the `island` value for one species. Then run
`select island from penguins where species = 'Adelie'` to see all islands that
species actually inhabits. If the grouped result shows only one island but the raw
data shows three, the database is picking arbitrarily.

</details>

## Count how many records have a phone number {: #sql-countnull}

Run this query. Then run a second query using `count(*)` and compare the two
results. If the numbers differ, find the rows that account for the difference.

[% inc countnull.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query meant to count all penguins in the dataset underreports the total because
`count(sex)` only counts rows where `sex` is not null, omitting the 11 penguins
whose sex was not recorded; the bug is using `count(sex)` instead of `count(*)`.

Shows: the difference between `count(column)` (excludes nulls) and
`count(*)` (counts every row).

To find it: run `select count(*), count(sex) from penguins`. If the two numbers
differ, the difference is the number of penguins `count(sex)` is missing because
their `sex` is null.

</details>

## Compute a class average including absent students {: #sql-avgmanual}

Run this query and note the result. Then run `select avg(body_mass_g) from penguins`
and compare. Are the two values the same?

[% inc avgmanual.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A manual average calculation divides the sum of body masses by the total row count,
but `sum()` skips the two rows where `body_mass_g` is null while `count(*)` still
counts them, making the denominator too large and the result too small; the bug is
dividing by `count(*)` instead of `count(body_mass_g)` or using `avg()` directly.

Shows: how aggregation functions treat null values and why the
built-in `avg()` should be preferred over hand-rolled sum/count
averages.

To find it: run `select avg(body_mass_g) from penguins` and compare it to the manual
calculation. If they differ, check whether `count(*)` and `count(body_mass_g)` return
the same number — if not, some rows have a null mass and the manual denominator is
too large.

</details>

## Find records that don't match a given value {: #sql-nullneq}

Run this query. How many rows does it return? Then run a query using `is not null`
and compare the row counts.

[% inc nullneq.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should return only penguins with a recorded sex returns zero rows
because comparing any value to null with `!=` produces null (not true) in SQL's
ternary logic, so the `where` clause never passes any row; the bug is using
`!= null` instead of `is not null`.

Shows: that null comparisons with `=` or `!=` always yield null, and
that `is null` / `is not null` are the only reliable null tests.

To find it: run `select count(*) from penguins where sex is not null`. If that
returns rows but the original query returns zero, the `!= null` test is failing
because null comparisons always produce null, not `true` or `false`.

</details>

## List all customers with or without orders {: #sql-innerleft}

Run this query and list the people in the result. Then run `select distinct person
from work` and compare. Does every person from the `work` table appear in the
query output?

[% inc innerleft.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should list total credits for every person silently omits people whose
jobs do not appear in the `job` table (because their work has no matching credit
value to join to); the bug is using `inner join` instead of `left join`.

Shows: the difference between inner and left joins and when each is
appropriate.

To find it: run `select distinct person from work` and compare the names to those in
the join result. Any name present in `work` but absent from the join result was
dropped because `inner join` excludes rows with no matching partner in the other
table.

</details>

## Join two tables to combine related records {: #sql-noonclause}

Run this query. Count the rows returned. How many rows are in the `job` table?
How many are in the `work` table? How do those numbers relate to the row count
you observed?

[% inc noonclause.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should pair each job with its matching work records instead returns
every possible combination of rows from both tables because the `on` clause is
missing; a join without an `on` condition (or equivalent `where` condition) is
a Cartesian product, producing rows equal to the product of the two table sizes.

Shows: that a join without a matching condition is almost never
correct and how to recognise a Cartesian product by its unexpectedly
large row count.

To find it: count the rows in `job` and the rows in `work`, then multiply. If the
query result has exactly that many rows, the join produced a Cartesian product,
which means the `on` clause is missing.

</details>

## Total donations where some records are empty {: #sql-coalescemiss}

Run this query and check the `total` column for each person. Which person has a
null total? What jobs did that person do, according to the `work` table?

[% inc coalescemiss.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that uses a left join to include all people shows null instead of 0 for
a person whose jobs produce no credit values, because `sum()` of an all-null group
returns null; the bug is not wrapping the sum in `coalesce(…, 0)`.

Shows: how `coalesce` provides a fallback value for null results and
why left joins often require it.

To find it: look for null values in the `total` column of the result. Then run
`select person, job from work where person = '<name with null total>'` to confirm
that person has work records. The null total comes from `sum()` over an all-null
group — wrap it in `coalesce(..., 0)` to return zero instead.

</details>

## Match employees to their department records {: #sql-joinswapped}

Run this query. Does every person appear? Compare the `num_surveys` counts to what
you get from `select count(*) from survey group by person_id`. Do the numbers match?

[% inc joinswapped.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should join people to their surveys instead produces a Cartesian
product because the `on` clause compares `survey.person_id` to itself (which is
always true) rather than to `person.person_id`; the bug is a copy-paste error
that left the table name on the left side of `on` as `survey` instead of `person`.

Shows: how to carefully check `on` conditions when the same column
name appears in both tables.

To find it: compare `num_surveys` in the join result to `select count(*) from
survey group by person_id`. If every person shows the same `num_surveys` equal to
the total number of survey rows, the `on` clause is always true and is joining every
row to every other row.

</details>

## Find pairs of employees in the same department {: #sql-selfjoin}

Run this query and look at a few rows. Use the `person` table to verify which
people are supervisors and which are subordinates. Are the labels in the output
correct?

[% inc selfjoin.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A self-join query that should display each person's name alongside their
supervisor's name has the labels reversed: the `on` condition `pa.person_id =
pb.supervisor_id` makes `pa` the supervisor and `pb` the subordinate, but the
aliases label `pa` as `person_name` and `pb` as `supervisor_name`; the bug is
swapping the alias names.

Shows: how to reason about the direction of a self-join and how to
verify the result against the underlying data.

To find it: pick one row from the result and look up both IDs in the `person` table.
If the person labeled `supervisor_name` is actually listed as a subordinate in the
raw data, the alias names in the query are reversed.

</details>
