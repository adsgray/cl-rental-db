.load /usr/lib/sqlite3/pcre.so";
update ad set furnished=1 where lower(title) REGEXP "\bfurnished";
