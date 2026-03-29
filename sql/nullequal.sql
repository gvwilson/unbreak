-- Find all penguins whose sex was not recorded.
select *
from penguins
-- BUG: comparing to null with = always produces null (never true) in SQL's
-- BUG: ternary logic, so no rows are returned; use IS NULL instead
where sex = null;
