#!/bin/bash
# it includes python2.7 virtual env with robot packages and git
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

BASEDIR=`dirname $0`
RESULTS_DIR='/home/opnfv/functest/results/odl/'
REPO_DIR='/home/opnfv/repos/odl_test'
#TODO: read this form config_functest.yaml

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
    var    one of the following: ODL_IP, ODL_PORT, ODL_USER, ODL_PASS, TENANT_NAME, USR_NAME, PASS, NEUTRON_IP, KEYSTONE_IP
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
ODL_IP=${ODL_IP:-'127.0.0.1'}
ODL_PORT=${ODL_PORT:-8181}
ODL_USER=${ODL_USER:-'admin'}
ODL_PASS=${ODL_PASS:-'admin'}
TENANT_NAME=${TENANT_NAME:-'admin'}
USR_NAME=${USR_NAME:-'admin'}
PASS=${PASS:-'admin'}
NEUTRON_IP=${NEUTRON_IP:-'127.0.0.1'}
KEYSTONE_IP=${KEYSTONE_IP:-'127.0.0.1'}
set +x

# set ODL credentials in ${REPO_DIR}/csit/variables/Variables.py
sed -i "s/^AUTH\ =.*$/AUTH\ =\ [u'$ODL_USER', u'$ODL_PASS']/"  \
    ${REPO_DIR}/csit/variables/Variables.py

# add custom tests to suite, if there are more custom tests needed this will be reworked
echo -e "${green}Copy custom tests to suite.${nc}"
cp -vf ${BASEDIR}/custom_tests/neutron/* ${REPO_DIR}/csit/suites/openstack/neutron/

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
    pybot -v KEYSTONE:${KEYSTONE_IP} -v NEUTRON:${NEUTRON_IP} \
        -v OSUSERNAME:\"${USR_NAME}\" -v OSTENANTNAME:\"${TENANT_NAME}\" -v OSPASSWORD:\"${PASS}\"  \
        -v PORT:${ODL_PORT} -v ODL_SYSTEM_IP:${ODL_IP} \
        ${REPO_DIR}/$line
    mkdir -p $RESULTS_DIR/logs/${test_num}
    mv log.html $RESULTS_DIR/logs/${test_num}/
    mv report.html $RESULTS_DIR/logs/${test_num}/
    mv output.xml $RESULTS_DIR/logs/${test_num}/
done < ${BASEDIR}/test_list.txt

# create final report which includes all partial test reports
for i in $(seq $test_num); do
  rebot_params="$rebot_params $RESULTS_DIR/logs/$i/output.xml"
done

echo -e "${green}Final report is located:${nc}"
rebot $rebot_params
