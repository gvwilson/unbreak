-- Find penguins that are on Biscoe island and are either Adelie or Chinstrap.
select species, island
from penguins
-- BUG: AND binds more tightly than OR, so this is parsed as:
-- BUG:   species='Adelie' OR (species='Chinstrap' AND island='Biscoe')
-- BUG: which returns ALL Adelie penguins (from any island) plus Chinstraps on Biscoe;
-- BUG: add parentheses: (species='Adelie' OR species='Chinstrap') AND island='Biscoe'
where species = 'Adelie' or species = 'Chinstrap' and island = 'Biscoe';
