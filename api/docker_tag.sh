#!/bin/bash
set -e
if [ $# -ne 1 ]
  then
    echo "Argument required. tagfile"
    exit 1
fi
filename=$1
branch_name=$(git symbolic-ref -q HEAD)
branch_name=${branch_name##refs/heads/}
branch_name=${branch_name:-HEAD}

commithash=`git log -n 1 origin/$branch_name | sed -n 1p | awk '{split($0,a," "); print a[2]}'`
tag=$branch_name-$commithash
echo "-- TAG : $tag FILENAME : $filename --"
echo $tag>$1