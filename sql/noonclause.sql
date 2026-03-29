-- Match each job entry to the work records for that job.
select *
from job join work
-- BUG: the ON clause is missing; without it, SQL produces a Cartesian product
-- BUG: combining every row of job with every row of work (2 x 7 = 14 rows);
-- BUG: add ON job.name = work.job to keep only the matching pairs
limit 10;
