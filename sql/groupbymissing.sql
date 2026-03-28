-- Count the number of penguins observed on each island, broken down by species.
select species, island, count(*) as num_penguins
from penguins
-- BUG: island appears in 'select' but is absent from 'group by'; the database picks
-- BUG: an arbitrary island value for each species group; add island to 'group by'
group by species;
