-- Count the number of penguins observed on each island, broken down by species.
select species, island, count(*) as num_penguins
from penguins
-- BUG: island appears in SELECT but is absent from GROUP BY; the database picks
-- BUG: an arbitrary island value for each species group; add island to GROUP BY
group by species;
