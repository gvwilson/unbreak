-- Find all female penguins.
select *
from penguins
-- BUG: sex is stored as 'FEMALE' (all uppercase); the literal 'female' (lowercase)
-- BUG: does not match any rows in SQLite's case-sensitive string comparison
where sex = 'female';
