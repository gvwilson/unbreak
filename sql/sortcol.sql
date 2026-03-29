-- Show the species, island, and sex of all penguins,
-- sorted alphabetically by island and then by species within each island.
select species, island, sex
from penguins
-- BUG: ORDER BY lists species before island, so rows are sorted by species
-- BUG: first and then by island; swap the column order to get island-first sorting
order by species, island;
