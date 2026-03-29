-- List the distinct species found in the penguins dataset (one row per species).
-- BUG: including sex produces one row per (species, sex) combination, giving
-- BUG: seven rows instead of three; remove sex from SELECT to get species alone
select distinct species, sex
from penguins;
