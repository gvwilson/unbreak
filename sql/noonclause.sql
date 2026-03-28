-- Match each job entry to the work records for that job.
select *
from job join work
-- BUG: the 'on' clause is missing; without it, SQL combines every row of
-- BUG: job with every row of work (2 x 7 = 14 rows); add 'on job.name = work.job'
-- BUG:  to keep only the matching pairs
limit 10;
