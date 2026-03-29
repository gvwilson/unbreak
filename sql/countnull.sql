-- Report the total number of penguins in the dataset.
-- BUG: count(sex) only counts rows where sex is not null (333 penguins);
-- BUG: 11 penguins whose sex was not recorded are excluded from the count;
-- BUG: use count(*) to count every row regardless of null values (344 total)
select count(sex) as total_penguins
from penguins;
