-- to see how many 0,1,2,etc bedroom units are posted each week.

create table tmp2 as select *, strftime('%Y', time) year, strftime('%W', time) week, strftime('%m', time) month from ad where loc1 in ( 'Vancouver','Coal Harbour','West End','East Vancouver','Yaletown','Kitsilano','Vancouver West Side', 'Cambie','South Vancouver','Downtown','Gastown','False Creek','Point Grey','Shaughnessy', 'Chinatown', 'UBC');

create table tmp3 as select *, strftime('%Y', time) year, strftime('%m', time) month from ad where loc1 in ( 'Vancouver','Coal Harbour','West End','East Vancouver','Yaletown','Kitsilano','Vancouver West Side', 'Cambie','South Vancouver','Downtown','Gastown','False Creek','Point Grey','Shaughnessy', 'Chinatown', 'UBC');


create table bedroomsummary as select bedrooms,year,week,furnished,count(*) from tmp2 group by year,week,bedrooms,furnished order by year,week,bedrooms,furnished;

create table bedroommonth as select bedrooms,year,month,furnished,count(*) from tmp3 group by year,month,bedrooms,furnished order by year,month,bedrooms,furnished;

create table bedroommonth2 as select year,month,furnished,count(*) from tmp3 where bedrooms <= 2 group by year,month,furnished order by year,month,furnished;
create table bedroommonth3 as select year,month,furnished,count(*) from tmp3 where bedrooms >= 3 group by year,month,furnished order by year,month,furnished;

-- then in shell:
-- sqlite3 -separator $'\t' ~/Downloads/cl.db "select * from bedroomsummary" > bedrooms.csv
-- sqlite3 -separator $'\t' ~/Downloads/cl.db "select * from bedroommonth" > bedroommonth.csv
-- sqlite3 -separator $'\t' ~/Downloads/cl.db "select * from bedroommonth2" > bedroommonth2.csv
-- sqlite3 -separator $'\t' ~/Downloads/cl.db "select * from bedroommonth3" > bedroommonth3.csv
