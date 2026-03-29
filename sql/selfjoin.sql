-- For each person, show their full name and their supervisor's full name.
select
    pa.personal || ' ' || pa.family as person_name,
    pb.personal || ' ' || pb.family as supervisor_name
from person pa join person pb
-- BUG: pa.person_id = pb.supervisor_id finds rows where pa supervises pb,
-- BUG: so pa is the supervisor and pb is the subordinate; the column aliases
-- BUG: person_name and supervisor_name are backwards relative to this logic;
-- BUG: swap the aliases or swap the ON condition to pa.supervisor_id = pb.person_id
on pa.person_id = pb.supervisor_id
order by pa.family, pa.personal;
