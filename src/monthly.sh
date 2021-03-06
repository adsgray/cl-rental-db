#!/bin/bash

vancouverloc="( 'Vancouver','Coal Harbour','West End','East Vancouver','Yaletown','Kitsilano','Vancouver West Side', 'Cambie','South Vancouver','Downtown','Gastown','False Creek','Point Grey','Shaughnessy', 'Chinatown', 'UBC')"
guardmin=100
guardmax=10000
file=/tmp/clrent.tsv

do_median() {
    bedrooms=$1
    bedrooms="($bedrooms)"
    furnished=$2

sqlite3 --separator $'\t' ~/Downloads/cl.db "select bedrooms, price, loc1, time from ad where bedrooms in $bedrooms and price > $guardmin and price < $guardmax and loc1 in $vancouverloc and furnished=$furnished and $date order by price;" > $file

#sqlite3 --separator $'\t' ~/Downloads/cl.db "select bedrooms, price, loc1, time from ad where bedrooms in $bedrooms and price > $guardmin and price < $guardmax and loc1 in $vancouverloc and $date order by price;" > $file

count=`wc -l $file|awk '{print $1}'`
echo -n "$count,"
tail -n +$(((`cat $file | wc -l` / 2) + 1)) $file | head -n 1|awk '{print $2}'
#wc -l $file
}


get_query_month() {
    m=$1
    if [ "$m" -lt "10" ]; then
	echo "0$m"
    else
	echo "$m"
    fi

}

# really ugly script to create a CSV of median rents
for b in 0 1 2 3; do
for year in 2016 2017 2018 2019 2020; do
	    for month in `seq 1 12`; do #1 2 3 4 5 6 7 8 9 10 11 12; do
		y=$year
		nextmonth=$(( $month + 1 ))
		if [ "$nextmonth" -eq "13" ]; then
		    nextmonth=1
		    y=$(( $year + 1 ))
		fi

		qm=`get_query_month $month`
		nqm=`get_query_month $nextmonth`
		date="time >= '$year-$qm-01' and time < '$y-$nqm-01'"

		for furn in 0 1; do
		    echo -n "$year,$month,$b,$furn,"
		    do_median $b $furn
		    echo ""
		done
	    done
done
done




#for b in 0 1 2 3; do
    #do_median $b
#done
