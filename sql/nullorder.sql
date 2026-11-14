-- List penguins ordered by body mass, lightest first.
select species, island, body_mass_g
from penguins
-- BUG: rows with a null body_mass_g sort first by default in SQLite; they appear
-- BUG: at the top as if lighter than everything else; use
-- BUG: 'order by body_mass_g is null, body_mass_g' to push nulls to the end
order by body_mass_g;
