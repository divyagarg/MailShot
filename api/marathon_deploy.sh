#!/bin/bash
# ./mesos_deploy.sh staging update
# ./mesos_deploy.sh staging create
if [ $# -ne 5 ]
  then
    echo "Missing arguments. environment=>${1} operation=>${2} project=>${3} repo=>${4} tagfile=>${5}"
    exit 1
fi
environment=${1}
operation=${2}
project=${3}
repo=${4}
tagfile=${5}
containerport=9048
if [ ! -f "$tagfile" ]
then
    echo "$tagfile does not exist"
    exit 1
fi
tag=`cat $tagfile`
mesosid="${environment//_/-}-$project-$repo"
case $environment in 
    "staging")
        mesos_url=http://marathon.staging.askme.com:8080/v2
    ;;
    "production")
        mesos_url=http://marathon.production.askme.com:8080/v2
    ;;
esac

case $operation in
    "create")
        url=$mesos_url/apps
        method=POST
    ;;
    "update")
        url=$mesos_url/apps/$mesosid
        method=PUT
    ;;
esac

configfile='marathon_config.json'
sed -e "s/\${project}/$project/" -e "s/\${containerport}/$containerport/" -e "s/\${repo}/$repo/"  -e "s/\${environment}/$environment/" -e "s/\${tag}/$tag/" -e "s/\${mesosid}/$mesosid/" marathon_config.json.tmpl >$configfile
if [ ! -f "$configfile" ]
then
    echo "$configfile does not exist"
    exit 1
fi
config=`cat $configfile`

echo "Deploying on $mesos_url with $config"
curl -X $method $url -d @$configfile -H "Content-type: application/json"