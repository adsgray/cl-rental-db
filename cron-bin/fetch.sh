#!/bin/sh

today=`date "+%Y-%m-%d"`

cd /home/ec2-user/code/craigslist-search/src

# fetch CL pages
./fetch.sh

# process the files
for f in $today/*html; do
	./bs.py $f
done

# upload the db to S3
./uploaddb.sh
