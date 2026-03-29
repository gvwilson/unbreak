-- Show total credits earned per person.
-- People who only did jobs not in the job table should show 0, not null.
select work.person, sum(job.credits) as total
from work left join job
on work.job = job.name
group by work.person
-- BUG: when all of a person's jobs are unrecognised (e.g. Madhi only 'complain'-ed),
-- BUG: sum() returns null because it has no non-null values to add; wrap with
-- BUG: COALESCE(sum(job.credits), 0) to display 0 instead of null
order by work.person;
