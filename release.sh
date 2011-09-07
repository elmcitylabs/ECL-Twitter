#!/bin/bash

git cim "bump version number to $1"
git archive --format=tar master > ecl_twitter-$1.tar
gzip -f ecl_twitter-$1.tar
s3cmd put ecl_twitter-$1.tar.gz s3://packages.elmcitylabs.com/ -P
