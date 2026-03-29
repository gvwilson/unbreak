-- Show the average body mass for each species along with the sex of each penguin.
select species, sex, avg(body_mass_g) as avg_mass
from penguins
-- BUG: sex appears in SELECT but not in GROUP BY; the database picks an
-- BUG: arbitrary sex value for each species group, making the sex column meaningless;
-- BUG: either add sex to GROUP BY or remove it from SELECT
group by species;
