-- select distinct genre
-- from movie, 
-- json_table(genres, '$[*]'
-- columns(
--     genre path '$'
-- )
-- )
-- order by 1 asc;

select * from movie
where runtime < 90;