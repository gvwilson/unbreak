-- Show the average body mass for each species along with the sex of each penguin.
select species, sex, avg(body_mass_g) as avg_mass
from penguins
-- BUG: sex appears in 'select' but not in 'group by'; the database picks an
-- BUG: arbitrary sex value for each species group, making the sex column meaningless;
-- BUG: either add sex to 'group by' or remove it from 'select'
group by species;
