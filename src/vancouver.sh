
sqlite3 -separator $'\t' ~/Downloads/cl.db "select * from ad where loc1 in ( 'Vancouver','Coal Harbour','West End','East Vancouver','Yaletown','Kitsilano','Vancouver West Side', 'Cambie','South Vancouver','Downtown','Gastown','False Creek','Point Grey','Shaughnessy', 'Chinatown', 'UBC') and time > '2017-12-31'" > vancouver.csv
