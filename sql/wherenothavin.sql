-- Find species whose average body mass exceeds 4000 g.
select species, avg(body_mass_g) as avg_mass
from penguins
-- BUG: aggregate functions cannot appear in a WHERE clause (WHERE filters rows
-- BUG: before grouping); this raises a syntax error; move the condition to a HAVING
-- BUG: clause after GROUP BY
where avg(body_mass_g) > 4000.0
group by species;
