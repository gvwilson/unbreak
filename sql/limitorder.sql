-- Show the five heaviest penguins.
select species, island, body_mass_g
from penguins
-- BUG: 'limit' without 'order by' returns an arbitrary set of rows, not the
-- BUG: five heaviest; the database makes no ordering promise, so the result
-- BUG: can change between runs; add 'order by body_mass_g desc' before the limit
limit 5;
