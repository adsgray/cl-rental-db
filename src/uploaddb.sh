#!/bin/bash

# AWS creds (via key/secret or instance IAM role must allow:
# "s3:PutObject", "s3:PutObjectAcl" on the destination bucket/folder

S3_BUCKET="adsgb02usw"
FOLDER="cl-rental-db"
DBFILE="/home/ec2-user/code/craigslist-search/db/cl.db"

#s3put --prefix $PREFIX --key_prefix $FOLDER --bucket $S3_BUCKET --grant public-read $DBFILE
aws s3 cp $DBFILE s3://$S3_BUCKET/$FOLDER/ --acl public-read
