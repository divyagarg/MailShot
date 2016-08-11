#!/bin/bash
set -e
if [ $# -ne 5 ]
  then
    echo "Missing arguments project=>${1} repo=>${2} tagfile=>${3} environment=>${4} operation=>${5}"
    exit 1
fi

project=${1}
repo=${2}
tagfile=${3}
environment=${4}
operation=${5}
echo "--Tagging--"
./docker_tag.sh $tagfile
echo "--Building Image--"
./docker_build.sh $project $repo $tagfile
echo "--Pushing Image--"
./docker_push.sh $project $repo $tagfile
echo "--Deploying Containers--"
./marathon_deploy.sh $environment $operation $project $repo $tagfile