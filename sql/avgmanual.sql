-- Calculate the average body mass of all penguins.
-- BUG: sum(body_mass_g) ignores the 2 rows where body_mass_g is null, but
-- BUG: count(*) counts all 344 rows including those two; dividing the sum by a
-- BUG: denominator that is too large produces a value lower than the true mean;
-- BUG: use avg(body_mass_g) or divide by count(body_mass_g) instead
select sum(body_mass_g) / count(*) as avg_mass
from penguins;
