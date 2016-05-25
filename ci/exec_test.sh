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

FUNCTEST_REPO_DIR=${repos_dir}/functest/
FUNCTEST_CONF_DIR=/home/opnfv/functest/conf/


function odl_tests(){
    keystone_ip=$(openstack catalog show identity |grep publicURL| cut -f3 -d"/" | cut -f1 -d":")
    neutron_ip=$(openstack catalog show network | grep publicURL | cut -f3 -d"/" | cut -f1 -d":")
    odl_ip=${neutron_ip}
    odl_port=8181
    if [ "$INSTALLER_TYPE" == "fuel" ]; then
        odl_port=8282
    elif [ "$INSTALLER_TYPE" == "apex" ]; then
        :
    elif [ "$INSTALLER_TYPE" == "joid" ]; then
        odl_ip=$SDN_CONTROLLER
        odl_port=8080
        :
    elif [ "$INSTALLER_TYPE" == "compass" ]; then
        :
    else
        odl_ip=$SDN_CONTROLLER
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
            ${FUNCTEST_REPO_DIR}/testcases/OpenStack/healthcheck/healthcheck.sh
        ;;
        "vping_ssh")
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/vPing/vPing_ssh.py $report
        ;;
        "vping_userdata")
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/vPing/vPing_userdata.py $report
        ;;
        "odl")
            odl_tests
            ODL_PORT=$odl_port ODL_IP=$odl_ip KEYSTONE_IP=$keystone_ip NEUTRON_IP=$neutron_ip USR_NAME=${OS_USERNAME} PASS=${OS_PASSWORD} \
                ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/start_tests.sh

            # push results to the DB in case of CI
            if [[ -n "$DEPLOY_SCENARIO" && "$DEPLOY_SCENARIO" != "none" &&
                  -n "$INSTALLER_TYPE" && "$INSTALLER_TYPE" != "none" ]]; then
                odl_logs="/home/opnfv/functest/results/odl/logs/2"
                odl_path="${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/"
                node_name=$(env | grep NODE_NAME | cut -f2 -d'=')
                python ${odl_path}/odlreport2db.py -x ${odl_logs}/output.xml -i ${INSTALLER_TYPE} -p ${node_name} -s ${DEPLOY_SCENARIO}
            fi
        ;;
        "tempest_smoke_serial")
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/tempest/run_tempest.py \
                $clean_flag -s -m smoke $report
        ;;
        "tempest_full_parallel")
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/tempest/run_tempest.py \
                $serial_flag $clean_flag -m full $report
        ;;
        "vims")
            python ${FUNCTEST_REPO_DIR}/testcases/vIMS/vIMS.py $clean_flag $report
        ;;
        "rally_full")
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/rally/run_rally-cert.py $clean_flag all $report
        ;;
        "rally_sanity")
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/rally/run_rally-cert.py \
                $clean_flag --sanity all $report
        ;;
        "bgpvpn")
            python ${FUNCTEST_REPO_DIR}/testcases/features/bgpvpn.py
        ;;
        "onos")
            if [ "$INSTALLER_TYPE" == "joid" ]; then
                python ${FUNCTEST_REPO_DIR}/testcases/Controllers/ONOS/Teston/onosfunctest.py -i joid
            else
                python ${FUNCTEST_REPO_DIR}/testcases/Controllers/ONOS/Teston/onosfunctest.py
            fi
      ;;
        "promise")
            python ${FUNCTEST_REPO_DIR}/testcases/features/promise.py $report
            sleep 10 # to let the instances terminate
        ;;
        "doctor")
            python ${FUNCTEST_REPO_DIR}/testcases/features/doctor.py
        ;;
        "ovno")
            ${repos_dir}/ovno/Testcases/RunTests.sh
        ;;
        *)
            echo "The test case '${test_name}' does not exist."
            exit 1
    esac
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
echo "Sourcing Credentials ${FUNCTEST_CONF_DIR}/openstack.creds to run the test.."
source ${FUNCTEST_CONF_DIR}/openstack.creds


# Run test
run_test $TEST
