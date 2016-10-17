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

FUNCTEST_REPO_DIR=${repos_dir}/functest
FUNCTEST_CONF_DIR=/home/opnfv/functest/conf

export PYTHONUNBUFFERED=1

function odl_tests(){
    keystone_ip=$(openstack catalog show identity |grep publicURL| cut -f3 -d"/" | cut -f1 -d":")
    neutron_ip=$(openstack catalog show network | grep publicURL | cut -f3 -d"/" | cut -f1 -d":")
    odl_ip=${neutron_ip}
    odl_port=8080
    if [ "$INSTALLER_TYPE" == "fuel" ]; then
        odl_port=8282
    elif [ "$INSTALLER_TYPE" == "apex" ]; then
        odl_ip=$SDN_CONTROLLER_IP
        odl_port=8181
    elif [ "$INSTALLER_TYPE" == "joid" ]; then
        odl_ip=$SDN_CONTROLLER
    elif [ "$INSTALLER_TYPE" == "compass" ]; then
        odl_port=8181
    else
        odl_ip=$SDN_CONTROLLER_IP
    fi
}

function sfc_prepare(){
    ids=($(neutron security-group-list|grep default|awk '{print $2}'))
    for id in ${ids[@]}; do
        if ! neutron security-group-show $id|grep "22/tcp" &>/dev/null; then
            neutron security-group-rule-create --protocol tcp \
                --port-range-min 22 --port-range-max 22 --direction ingress $id
            neutron security-group-rule-create --protocol tcp \
                --port-range-min 22 --port-range-max 22 --direction egress $id
        fi
    done
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
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/vPing/vping.py -m ssh $report
        ;;
        "vping_userdata")
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/vPing/vping.py -m userdata $report
        ;;
        "odl")
            odl_tests
            [[ "$report" == "-r" ]] && args=-p
            ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/OpenDaylightTesting.py \
                --keystoneip $keystone_ip --neutronip $neutron_ip \
                --osusername ${OS_USERNAME} --ostenantname ${OS_TENANT_NAME} \
                --ospassword ${OS_PASSWORD} \
                --odlip $odl_ip --odlwebport $odl_port ${args}
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
            python ${FUNCTEST_REPO_DIR}/testcases/vnf/vIMS/vIMS.py $clean_flag $report
        ;;
        "vrouter")
            python ${FUNCTEST_REPO_DIR}/testcases/vnf/vRouter/vRouter.py $clean_flag $report
        ;;
        "rally_full")
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/rally/run_rally-cert.py $clean_flag all $report
        ;;
        "rally_sanity")
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/rally/run_rally-cert.py \
                $clean_flag --sanity all $report
        ;;
        "bgpvpn")
            sdnvpn_repo_dir=${repos_dir}/sdnvpn/test/functest/
            python ${sdnvpn_repo_dir}/run_tests.py $report
        ;;
        "onos")
            python ${FUNCTEST_REPO_DIR}/testcases/Controllers/ONOS/Teston/onosfunctest.py
        ;;
        "onos_sfc")
            python ${FUNCTEST_REPO_DIR}/testcases/Controllers/ONOS/Teston/onosfunctest.py -t sfc
        ;;
        "promise")
            python ${FUNCTEST_REPO_DIR}/testcases/features/promise.py $report
            sleep 10 # to let the instances terminate
        ;;
        "doctor")
            python ${FUNCTEST_REPO_DIR}/testcases/features/doctor.py $report
        ;;
        "ovno")
            # suite under rewritting for colorado
            # no need to run anything until refactoring done
            # ${repos_dir}/ovno/Testcases/RunTests.sh
        ;;
        "security_scan")
            echo "Sourcing Credentials ${FUNCTEST_CONF_DIR}/stackrc for undercloud .."
            source ${FUNCTEST_CONF_DIR}/stackrc
            python ${repos_dir}/securityscanning/security_scan.py --config ${repos_dir}/securityscanning/config.ini
        ;;
        "copper")
            python ${FUNCTEST_REPO_DIR}/testcases/features/copper.py $report
        ;;
        "moon")
            python ${repos_dir}/moon/tests/run_tests.py $report
        ;;
        "multisite")
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/tempest/gen_tempest_conf.py
            python ${FUNCTEST_REPO_DIR}/testcases/OpenStack/tempest/run_tempest.py \
                $clean_flag -s -m feature_multisite $report \
                -c ${FUNCTEST_REPO_DIR}/testcases/OpenStack/tempest/tempest_multisite.conf
        ;;
        "domino")
            python ${FUNCTEST_REPO_DIR}/testcases/features/domino.py $report
        ;;
        "odl-sfc")
            ODL_SFC_DIR=${FUNCTEST_REPO_DIR}/testcases/features/sfc
            # pass FUNCTEST_REPO_DIR inside prepare_odl_sfc.bash
            FUNCTEST_REPO_DIR=${FUNCTEST_REPO_DIR} bash ${ODL_SFC_DIR}/prepare_odl_sfc.bash || exit $?
            source ${ODL_SFC_DIR}/tackerc
            python ${ODL_SFC_DIR}/sfc_colorado1.py $report
        ;;
        "parser")
            python ${FUNCTEST_REPO_DIR}/testcases/vnf/vRNC/parser.py $report
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
echo "Sourcing Credentials ${FUNCTEST_CONF_DIR}/openstack.creds to run the test.."
source ${FUNCTEST_CONF_DIR}/openstack.creds

# ODL Boron workaround to create additional flow rules to allow port 22 TCP
if [[ $DEPLOY_SCENARIO == *"odl_l2-sfc"* ]]; then
    sfc_prepare
fi

# Run test
run_test $TEST
