#!/bin/bash

vancouverloc="( 'Vancouver','Coal Harbour','West End','East Vancouver','Yaletown','Kitsilano','Vancouver West Side', 'Cambie','South Vancouver','Downtown','Gastown','False Creek','Point Grey','Shaughnessy', 'Chinatown', 'UBC')"
furnished=0
bedrooms="(0)"
#from=2017-11-01
#to=2017-12-01
from=2018-12-01
to=2019-01-01
#from=2019-01-01
#to=2019-02-01
#from=2019-02-01
#to=2019-03-01
#from=2019-03-01
#to=2019-04-01
date="time >= '$from' and time <= '$to'"
guardmin=100
guardmax=10000
file=/tmp/clrent.tsv

do_median() {
    bedrooms=$1
    bedrooms="($bedrooms)"

sqlite3 --separator $'\t' ~/Downloads/cl.db "select bedrooms, price, loc1, time from ad where bedrooms in $bedrooms and price > $guardmin and price < $guardmax and loc1 in $vancouverloc and furnished=$furnished and $date order by price;" > $file

tail -n +$(((`cat $file | wc -l` / 2) + 1)) $file | head -n 1
#wc -l $file
}

for b in 0 1 2 3; do
    do_median $b
done
