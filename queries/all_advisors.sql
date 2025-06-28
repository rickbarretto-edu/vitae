-- Queries all existing Advisors
--
-- Since Advisors can't be a FK, i can't do it at ORM level.

select Researcher.* from Researcher
join Advising on Researcher.lattes_id = Advising.advisor_id;