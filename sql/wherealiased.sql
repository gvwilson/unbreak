-- Find all penguins heavier than 4 kg, displaying mass in kilograms.
select species, body_mass_g / 1000.0 as mass_kg
from penguins
-- BUG: SQLite evaluates 'where' before 'select', so the alias mass_kg does not yet
-- BUG: exist when the 'where' clause runs; replace mass_kg with the full expression
-- BUG: body_mass_g / 1000.0 in the 'where' clause
where mass_kg > 4.0;
