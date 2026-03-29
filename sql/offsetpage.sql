-- Retrieve rows 11 through 15 from the penguins table (the third page of 5).
select *
from penguins
-- BUG: OFFSET 11 skips 11 rows and returns rows 12-16, not rows 11-15;
-- BUG: the correct offset for the third page of 5 is OFFSET 10
limit 5 offset 11;
