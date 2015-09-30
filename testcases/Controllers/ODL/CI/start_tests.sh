#!/bin/bash
# Script requires that test environment is created already
# it includes python2.7 virtual env with robot packages and git
# use create_env.sh script for creating python virtualenv

BASEDIR=`dirname $0`
# Colors
green='\033[0;32m'
light_green='\033[1;32m'
red='\033[1;31m'
nc='\033[0m' # No Color

usage="Script for starting ODL tests. Tests to be executed are specified in test_list.txt file.

usage:
[var=value] bash $(basename "$0") [-h]

where:
    -h     show this help text
    var    one of the following: ODL_IP, ODL_PORT, USR_NAME, PASS, NEUTRON_IP
    value  new value for var

example:
    ODL_IP=oscontro1 ODL_PORT=8080 bash $(basename "$0")"

while getopts ':h' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done

echo -e "${green}Current environment parameters for ODL suite.${nc}"
# Following vars might be also specified as CLI params
set -x
ODL_IP=${ODL_IP:-'192.168.1.5'}
ODL_PORT=${ODL_PORT:-8081}
USR_NAME=${USR_NAME:-'neutron'}
PASS=${PASS:-'octopus'}
NEUTRON_IP=${NEUTRON_IP:-192.168.0.68}
set +x

echo -e "${green}Cloning ODL integration git repo.${nc}"
if [ -d ${BASEDIR}/integration ]; then
    cd ${BASEDIR}/integration
    git checkout -- .
    git pull
    cd -
else
    git clone https://github.com/opendaylight/integration.git ${BASEDIR}/integration
fi

# Change openstack password for admin tenant in neutron suite
sed -i "s/\"password\": \".*\"/\"password\": \"${PASS}\"/" ${BASEDIR}/integration/test/csit/suites/openstack/neutron/__init__.robot

# Add Start Suite and Teardown Suite
sed -i "/^Documentation.*/a Suite Teardown     Stop Suite" ${BASEDIR}/integration/test/csit/suites/openstack/neutron/__init__.robot
sed -i "/^Documentation.*/a Suite Setup        Start Suite" ${BASEDIR}/integration/test/csit/suites/openstack/neutron/__init__.robot
exit 0
if source $BASEDIR/venv/bin/activate; then
    echo -e "${green}Python virtualenv activated.${nc}"
else
    echo -e "${red}ERROR${nc}"
    exit 1
fi

# add custom tests to suite, if there are more custom tests needed this will be reworked
echo -e "${green}Copy custom tests to suite.${nc}"
cp -vf $BASEDIR/custom_tests/neutron/* $BASEDIR/integration/test/csit/suites/openstack/neutron/

# List of tests are specified in test_list.txt
# those are relative paths to test directories from integartion suite
echo -e "${green}Executing chosen tests.${nc}"
test_num=0
while read line
do
    # skip comments
    [[ ${line:0:1} == "#" ]] && continue
    # skip empty lines
    [[ -z "${line}" ]] && continue

    ((test_num++))
    echo -e "${light_green}Starting test: $line ${nc}"
    pybot -v OPENSTACK:${NEUTRON_IP} -v PORT:${ODL_PORT} -v CONTROLLER:${ODL_IP} ${BASEDIR}/$line
    mkdir -p $BASEDIR/logs/${test_num}
    mv log.html $BASEDIR/logs/${test_num}/
    mv report.html $BASEDIR/logs/${test_num}/
    mv output.xml $BASEDIR/logs/${test_num}/
done < ${BASEDIR}/test_list.txt

# create final report which includes all partial test reports
for i in $(seq $test_num); do
  rebot_params="$rebot_params $BASEDIR/logs/$i/output.xml"
done

echo -e "${green}Final report is located:${nc}"
rebot $rebot_params

# deactivate venv
echo -e "${green}Deactivate venv.${nc}"
deactivate
