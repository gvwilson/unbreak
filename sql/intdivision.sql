-- Show body mass in kilograms for the first 10 penguins.
select species, body_mass_g,
    -- BUG: body_mass_g and 1000 are both integers, so SQLite performs integer
    -- BUG: division and truncates the result (e.g. 3750 / 1000 = 3, not 3.75);
    -- BUG: divide by 1000.0 to force floating-point arithmetic
    body_mass_g / 1000 as mass_kg
from penguins
limit 10;
