-- to see how many 0,1,2,etc bedroom units are posted each week.

create table tmp2 as select *, strftime('%Y', time) year, strftime('%W', time) week from ad where loc1 in ( 'Vancouver','Coal Harbour','West End','East Vancouver','Yaletown','Kitsilano','Vancouver West Side', 'Cambie','South Vancouver','Downtown','Gastown','False Creek','Point Grey','Shaughnessy', 'Chinatown', 'UBC');

create table bedroomsummary as select bedrooms,year,week,count(*) from tmp2 group by year,week,bedrooms order by year,week,bedrooms;

-- then in shell:
-- sqlite3 -separator ',' ~/Downloads/cl.db "select * from bedroomsummary" > bedrooms.csv
