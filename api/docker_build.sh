#!/bin/bash
set -e
if [ $# -lt 3 ]
  then
    echo "Arguments required : project repo tagfile --no-cache"
    exit 1
fi
project=${1}
repo=${2}
tagfile=${3}
nocache=${4:-false}
if [ ! -f "$tagfile" ]
then
    echo "$file does not exist"
    exit 1
fi
tag=`cat $tagfile`

cp Dockerfile.tmpl Dockerfile
echo "Building... project=>$project repo=>$repo tag=>$tag --no-cache=>$nocache"
#docker build --build-arg COMMIT_TAG=$tag -t $project/$repo .
docker build --no-cache=$nocache --rm=true -t $project/$repo .
rm Dockerfile