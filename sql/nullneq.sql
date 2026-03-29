-- Find all penguins whose sex has been recorded.
select *
from penguins
-- BUG: comparing to null with != produces null (not true) in SQL's ternary logic,
-- BUG: so the 333 rows where sex is known are also excluded; use IS NOT NULL instead
where sex != null;
