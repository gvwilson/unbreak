-- List each person's full name and the number of surveys they have done.
select
    person.personal || ' ' || person.family as full_name,
    count(*) as num_surveys
from person join survey
-- BUG: the ON condition compares survey.person_id to itself, which is always
-- BUG: true and creates a Cartesian product; change the left side to person.person_id
-- BUG: so that only matching person and survey rows are combined
on survey.person_id = survey.person_id
group by person.person_id
order by person.family, person.personal;
