#!/bin/bash
set -e
if [ $# -ne 3 ]
  then
    echo "Missing arguments project=>${1} repo=>${2} tagfile=>${3}"
    exit 1
fi

file=${3}
if [ ! -f "$file" ]
then
    echo "$file does not exist"
    exit 1
fi
tag=`cat $file`

project=${1}
repo=${2}
base_url='docker-registry.askme.com'
full_url=$base_url/$project/$repo:$tag

echo "Pushing $full_url"
docker tag -f $project/$repo $full_url
docker push $full_url