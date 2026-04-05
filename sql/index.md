# SQL

[download databases](./databases.zip)

## Wrong Sort Column Order {: #sql-sortcol}

Run this query and look at the first several rows. Is the output ordered by island
first, or by species first?

[% inc sortcol.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query meant to sort penguins by island and then by species within each island
produces species-first ordering instead; the bug is listing the columns in the
wrong order in the `order by` clause. Shows how `order by` applies columns from
left to right and why column order in that clause matters.

</details>

## Off-by-One in OFFSET Paging {: #sql-offsetpage}

Run this query and note which rows are returned. Count from the beginning of the
full table to check whether rows 11–15 are actually what you got.

[% inc offsetpage.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query meant to retrieve the third page of five rows returns rows 12–16 instead
of rows 11–15; the bug is using `offset 11` (which skips 11 rows) instead of
`offset 10`. Shows how `limit` and `offset` interact and how to calculate the
correct offset for a given page number.

</details>

## Integer Division Truncation {: #sql-intdivision}

Run this query and compare the `mass_kg` column to the `body_mass_g` column.
Do the kilogram values look right for a penguin that weighs, say, 3750 g?

[% inc intdivision.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that converts body mass from grams to kilograms silently truncates the
result because SQLite performs integer division when both operands are integers;
the bug is dividing by `1000` instead of `1000.0`. Shows how to force
floating-point arithmetic in SQL and why checking computed columns against known
values catches this class of error.

</details>

## DISTINCT Over Too Many Columns {: #sql-distinctcols}

Run this query and count the rows returned. How many distinct species are in the
dataset? Does the row count match that number?

[% inc distinctcols.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query intended to list the distinct species in the dataset returns seven rows
instead of three because `distinct` is applied to both `species` and `sex`,
producing one row per unique (species, sex) combination; the bug is including `sex`
in the `select` clause. Shows that `distinct` operates on the entire set of
selected columns, not on individual ones.

</details>

## NULL Equality Test {: #sql-nullequal}

Run this query. How many rows does it return? Are there penguins in the table whose
sex was not recorded?

[% inc nullequal.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that tries to find penguins with no recorded sex returns zero rows because
comparing any value to `null` with `=` produces `null` (not `true`) in SQL's
ternary logic, so the `where` clause never passes; the bug is using `= null` instead
of `is null`. Shows SQL's three-valued logic and the two special tests `is null`
and `is not null`.

</details>

## Impossible AND Condition {: #sql-impossibleand}

Run this query. How many rows does it return? Choose a penguin you know is on
Biscoe island from a previous query and check whether it appears here.

[% inc impossibleand.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should return penguins from either Biscoe or Dream island returns
zero rows because `and` requires both conditions to be true at the same time, but
a penguin can only be on one island; the bug is using `and` where `or` is needed.
Shows the difference between `and` and `or` and how to spot conditions that can
never simultaneously be true.

</details>

## Case-Sensitive String Value {: #sql-casevalue}

Run this query and count the rows returned. Then run a query to find the distinct
values stored in the `sex` column. Do any of them match the literal used in the
`where` clause?

[% inc casevalue.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should return all female penguins returns zero rows because the `sex`
column stores the value `'FEMALE'` in uppercase but the query filters on
`'female'` in lowercase; SQLite string comparisons are case-sensitive for non-ASCII
characters. Shows how to inspect the actual stored values before writing a filter
and how to use functions like `upper()` or `lower()` to normalise comparisons.

</details>

## WHERE References a SELECT Alias {: #sql-wherealiased}

Run this query. Does it raise an error or return wrong results? Add a second
`select` that uses the full expression `body_mass_g / 1000.0` in the `where`
clause and compare the two queries' output.

[% inc wherealiased.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that tries to filter using a column alias defined in the `select` clause
fails with a "no such column" error because SQL evaluates `where` before `select`,
so the alias does not yet exist at that point; the bug is referencing `mass_kg` in
`where` instead of repeating the full expression `body_mass_g / 1000.0`. Shows
the order of SQL clause evaluation.

</details>

## AND/OR Operator Precedence {: #sql-andorprecedence}

Run this query. Which species and islands appear in the result? Is the output what
you expected based on the comment describing the intent?

[% inc andorprecedence.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query intended to find Adelie or Chinstrap penguins that are on Biscoe island
instead returns all Adelie penguins from any island plus Chinstraps on Biscoe,
because `and` binds more tightly than `or`; the bug is missing parentheses around
the `or` sub-expression. Shows SQL operator precedence and why parentheses are
needed to make complex `where` conditions unambiguous.

</details>

## Non-Aggregated Column in GROUP BY {: #sql-nonaggcol}

Run this query and examine the `sex` column. Pick one species and check a few rows
against the original data. Are the sex values consistent with what you expected
for that species group?

[% inc nonaggcol.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that groups by species but also selects `sex` without aggregating it
produces an arbitrary, unpredictable sex value for each species group because `sex`
is not in the `group by` clause; the bug is selecting a column that is neither
aggregated nor part of the grouping. Shows why every column in `select` must
either appear in `group by` or be wrapped in an aggregation function.

</details>

## Aggregate Function in WHERE Clause {: #sql-wherenothavin}

Run this query. Does it return a result or raise an error? Check whether moving
the condition to a `having` clause after `group by` fixes the problem.

[% inc wherenothavin.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that tries to filter groups by their average value using `where` raises an
error because aggregate functions like `avg()` cannot appear in `where`; `where`
filters individual rows before grouping, while `having` filters groups after
aggregation; the bug is placing the condition in `where` instead of `having`.
Shows the difference in timing between `where` and `having` in SQL's execution
order.

</details>

## GROUP BY Missing a Column {: #sql-groupbymissing}

Run this query and examine the `island` column. Do all the rows for a given species
show the same island? Check a few values against the original table.

[% inc groupbymissing.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that counts penguins per species per island produces unreliable island
values because `island` appears in `select` but not in `group by`, so the database
picks an arbitrary island for each species group; the bug is omitting `island` from
the `group by` clause. Shows that every non-aggregated column in `select` must
also appear in `group by`.

</details>

## count(column) Skips NULL Rows {: #sql-countnull}

Run this query. Then run a second query using `count(*)` and compare the two
results. If the numbers differ, find the rows that account for the difference.

[% inc countnull.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query meant to count all penguins in the dataset underreports the total because
`count(sex)` only counts rows where `sex` is not null, omitting the 11 penguins
whose sex was not recorded; the bug is using `count(sex)` instead of `count(*)`.
Shows the difference between `count(column)` (excludes nulls) and `count(*)`
(counts every row).

</details>

## Manual Average With Wrong Denominator {: #sql-avgmanual}

Run this query and note the result. Then run `select avg(body_mass_g) from penguins`
and compare. Are the two values the same?

[% inc avgmanual.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A manual average calculation divides the sum of body masses by the total row count,
but `sum()` skips the two rows where `body_mass_g` is null while `count(*)` still
counts them, making the denominator too large and the result too small; the bug is
dividing by `count(*)` instead of `count(body_mass_g)` or using `avg()` directly.
Shows how aggregation functions treat null values and why the built-in `avg()`
should be preferred over hand-rolled sum/count averages.

</details>

## NULL Inequality Test {: #sql-nullneq}

Run this query. How many rows does it return? Then run a query using `is not null`
and compare the row counts.

[% inc nullneq.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should return only penguins with a recorded sex returns zero rows
because comparing any value to null with `!=` produces null (not true) in SQL's
ternary logic, so the `where` clause never passes any row; the bug is using
`!= null` instead of `is not null`. Shows that null comparisons with `=` or `!=`
always yield null, and that `is null` / `is not null` are the only reliable null
tests.

</details>

## INNER JOIN Drops Unmatched Rows {: #sql-innerleft}

Run this query and list the people in the result. Then run `select distinct person
from work` and compare. Does every person from the `work` table appear in the
query output?

[% inc innerleft.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should list total credits for every person silently omits people whose
jobs do not appear in the `job` table (because their work has no matching credit
value to join to); the bug is using `inner join` instead of `left join`. Shows
the difference between inner and left joins and when each is appropriate.

</details>

## Missing ON Clause (Cartesian Product) {: #sql-noonclause}

Run this query. Count the rows returned. How many rows are in the `job` table?
How many are in the `work` table? How do those numbers relate to the row count
you observed?

[% inc noonclause.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should pair each job with its matching work records instead returns
every possible combination of rows from both tables because the `on` clause is
missing; a join without an `on` condition (or equivalent `where` condition) is
a Cartesian product, producing rows equal to the product of the two table sizes.
Shows that a join without a matching condition is almost never correct and how to
recognise a Cartesian product by its unexpectedly large row count.

</details>

## NULL Sum Needs COALESCE {: #sql-coalescemiss}

Run this query and check the `total` column for each person. Which person has a
null total? What jobs did that person do, according to the `work` table?

[% inc coalescemiss.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that uses a left join to include all people shows null instead of 0 for
a person whose jobs produce no credit values, because `sum()` of an all-null group
returns null; the bug is not wrapping the sum in `coalesce(…, 0)`. Shows how
`coalesce` provides a fallback value for null results and why left joins often
require it.

</details>

## JOIN ON Condition References Same Table Twice {: #sql-joinswapped}

Run this query. Does every person appear? Compare the `num_surveys` counts to what
you get from `select count(*) from survey group by person_id`. Do the numbers match?

[% inc joinswapped.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A query that should join people to their surveys instead produces a Cartesian
product because the `on` clause compares `survey.person_id` to itself (which is
always true) rather than to `person.person_id`; the bug is a copy-paste error
that left the table name on the left side of `on` as `survey` instead of `person`.
Shows how to carefully check `on` conditions when the same column name appears in
both tables.

</details>

## Self-Join Aliases Confused {: #sql-selfjoin}

Run this query and look at a few rows. Use the `person` table to verify which
people are supervisors and which are subordinates. Are the labels in the output
correct?

[% inc selfjoin.sql scrub="\s*--.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A self-join query that should display each person's name alongside their
supervisor's name has the labels reversed: the `on` condition `pa.person_id =
pb.supervisor_id` makes `pa` the supervisor and `pb` the subordinate, but the
aliases label `pa` as `person_name` and `pb` as `supervisor_name`; the bug is
swapping the alias names. Shows how to reason about the direction of a self-join
and how to verify the result against the underlying data.

</details>
