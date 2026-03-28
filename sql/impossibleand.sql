-- Find all penguins from either Biscoe island or Dream island.
select species, island, sex
from penguins
-- BUG: 'and' requires both conditions to be true simultaneously, but a row can
-- BUG: only have one island value; no row can be on both Biscoe and Dream, so the
-- BUG: result is always empty; use 'or' to accept either island
where island = 'Biscoe' and island = 'Dream';
