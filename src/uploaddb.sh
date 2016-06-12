#!/bin/bash

# config.sh must:
# export AWS_ACCESS_KEY_ID="KEY_ID"
# export AWS_SECRET_ACCESS_KEY="ACCESS_KEY"
. config.sh

export S3_BUCKET="adsgb02usw"
PREFIX="/home/ec2-user/code/craigslist-search/db"
FOLDER="cl-rental-db"
DBFILE="/home/ec2-user/code/craigslist-search/db/cl.db"

s3put --prefix $PREFIX --key_prefix $FOLDER --bucket $S3_BUCKET --grant public-read $DBFILE
