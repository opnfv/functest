#!/bin/bash

#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#         Morgan Richomme (morgan.richomme@orange.com)
# Installs the Functest framework within the Docker container
# and run the tests automatically
#
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

usage="Script to trigger the tests automatically.

usage:
    bash $(basename "$0") [-h|--help] [-t <test_name>]

where:
    -h|--help         show this help text
    -r|--report       push results to database (false by default)
    -s|--serial       run Tempest tests in one thread
    -t|--test         run specific test case
      <test_name>"


report=""
serial=false

# Get the list of runnable tests
# Check if we are in CI mode
debug=""
if [[ "${CI_DEBUG,,}" == "true" ]];then
    debug="--debug"
fi

FUNCTEST_REPO_DIR=${REPOS_DIR}/functest
FUNCTEST_TEST_DIR=${REPOS_DIR}/functest/functest/opnfv_tests
FUNCTEST_CONF_DIR=/home/opnfv/functest/conf

export PYTHONUNBUFFERED=1

function odl_tests(){
    keystone_ip=$(openstack catalog show identity |grep publicURL| cut -f3 -d"/" | cut -f1 -d":")
    neutron_ip=$(openstack catalog show network | grep publicURL | cut -f3 -d"/" | cut -f1 -d":")
    odl_ip=${neutron_ip}
    odl_port=8080
    odl_restport=8181
    if [ "$INSTALLER_TYPE" == "fuel" ]; then
        odl_port=8282
    elif [ "$INSTALLER_TYPE" == "apex" ]; then
        odl_ip=$SDN_CONTROLLER_IP
        odl_port=8081
        odl_restport=8081
    elif [ "$INSTALLER_TYPE" == "netvirt" ]; then
        odl_ip=$SDN_CONTROLLER_IP
        odl_port=8081
        odl_restport=8081
    elif [ "$INSTALLER_TYPE" == "joid" ]; then
        odl_ip=$SDN_CONTROLLER
    elif [ "$INSTALLER_TYPE" == "compass" ]; then
        odl_port=8181
    else
        odl_ip=$SDN_CONTROLLER_IP
    fi
}



function run_test(){
    test_name=$1
    serial_flag=""
    if [ $serial == "true" ]; then
        serial_flag="-s"
    fi

    case $test_name in
        "healthcheck")
            ${FUNCTEST_TEST_DIR}/openstack/healthcheck/healthcheck.sh
        ;;
        "odl")
            odl_tests
            [[ "$report" == "-r" ]] && args=-p
            ${FUNCTEST_TEST_DIR}/sdn/odl/odl.py \
                --keystoneip $keystone_ip \
                --neutronip $neutron_ip \
                --odlip $odl_ip \
                --odlrestconfport $odl_restport \
                --odlwebport $odl_port \
                --ospassword ${OS_PASSWORD} \
                --ostenantname ${OS_TENANT_NAME} \
                --osusername ${OS_USERNAME} \
                ${args}
        ;;
        "ovno")
            # suite under rewritting for colorado
            # no need to run anything until refactoring done
            # ${REPOS_DIR}/ovno/Testcases/RunTests.sh
        ;;
        *)
            echo "The test case '${test_name}' does not exist."
            exit 1
    esac

    if [[ $? != 0 ]]; then exit 1
    else exit 0
    fi
}


# Parse parameters
while [[ $# > 0 ]]
    do
    key="$1"
    case $key in
        -h|--help)
            echo "$usage"
            exit 0
            shift
        ;;
        -r|--report)
            report="-r"
        ;;
        -s|--serial)
            serial=true
        ;;
        -t|--test|--tests)
            TEST="$2"
            shift
        ;;
        *)
            echo "unknown option $1 $2"
            exit 1
        ;;
    esac
    shift # past argument or value
done


# Source credentials
echo "Sourcing Credentials ${creds} to run the test.."
source ${creds}


# Run test
run_test $TEST
