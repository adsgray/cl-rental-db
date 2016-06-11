#!/bin/bash

export PATH=$PATH:/usr/bin:/bin

url="http://vancouver.craigslist.ca/search/apa"
today=`date "+%Y-%m-%d"`

mkdir -p $today
cd $today

# silent mode
options="-s"
useragent='Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
curlcmd="curl $options --user-agent $useragent"

$curlcmd $url > 0.html

for s in `seq 1 10`; do
	sleep `expr $RANDOM % 40 + 20`
	surl="$url?s=${s}00"
	$curlcmd $surl > $s.html
done
