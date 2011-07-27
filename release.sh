#!/bin/bash

git archive --format=tar master > ecl_twitter-$1.tar
gzip -f ecl_twitter-$1.tar
s3cmd put ecl_twitter-$1.tar.gz s3://packages.elmcitylabs.com/ -P
