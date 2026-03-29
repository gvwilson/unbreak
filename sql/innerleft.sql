-- List every person and the total credits they have earned.
-- People who only did jobs not listed in the job table should appear with 0 credits.
select work.person, sum(job.credits) as total
-- BUG: inner join silently drops people whose jobs have no match in the job table
-- BUG: (e.g. anyone who only 'complain'-ed); use LEFT JOIN so every person appears,
-- BUG: then wrap the sum in COALESCE(..., 0) to replace null totals with 0
from work inner join job
on work.job = job.name
group by work.person;
