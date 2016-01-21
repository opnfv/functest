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
    -n|--no-clean     do not clean OpenStack resources after test run
    -t|--test         run specific set of tests
      <test_name>     one or more of the following: vping,odl,rally,tempest,vims,onos,promise,ovno. Separated by comma.


examples:
    $(basename "$0")
    $(basename "$0") --test vping,odl
    $(basename "$0") -t tempest,rally"


# Support for Functest offline
# NOTE: Still not 100% working when running the tests
offline=false
report=""
clean=true
# Get the list of runnable tests
# Check if we are in CI mode


function clean_openstack(){
    if [ $clean == true ]; then
        echo -e "\n\nCleaning Openstack environment..."
        python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/clean_openstack.py \
            --debug
        echo -e "\n\n"
    fi
}

function run_test(){
    test_name=$1
    echo ""
    echo "----------------------------------------------"
    echo "  Running test cases: $i"
    echo "----------------------------------------------"
    echo ""
    case $test_name in
        "vping")
            info "Running vPing test..."
            python ${FUNCTEST_REPO_DIR}/testcases/vPing/CI/libraries/vPing2.py \
                --debug ${report}
        ;;
        "vping_userdata")
            info "Running vPing test using userdata/cloudinit.... "
            python ${FUNCTEST_REPO_DIR}/testcases/vPing/CI/libraries/vPing.py \
                --debug ${report}
        ;;
        "odl")
            info "Running ODL test..."
            neutron_ip=$(keystone catalog --service identity | grep publicURL | cut -f3 -d"/" | cut -f1 -d":")
            odl_ip=$(keystone catalog --service network | grep publicURL | cut -f3 -d"/" | cut -f1 -d":")
            usr_name=$(env | grep OS | grep OS_USERNAME | cut -f2 -d'=')
            password=$(env | grep OS | grep OS_PASSWORD | cut -f2 -d'=')
            odl_port=8181
            if [ $INSTALLER_TYPE == "fuel" ]; then
                odl_port=8282
            elif [ $INSTALLER_TYPE == "apex" ]; then
                :
            elif [ $INSTALLER_TYPE == "joid" ]; then
                :
            elif [ $INSTALLER_TYPE == "compass" ]; then
                :
            else
                error "INSTALLER_TYPE not valid."
                exit 1
            fi
            ODL_PORT=$odl_port ODL_IP=$odl_ip NEUTRON_IP=$neutron_ip USR_NAME=$usr_name PASS=$password \
                ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/start_tests.sh

            # push results to the DB in case of CI
            if [[ -n "$DEPLOY_SCENARIO" && "$DEPLOY_SCENARIO" != "none" ]]; then
                odl_logs="/home/opnfv/functest/results/odl/logs/2"
                odl_path="${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI"
                node_name=$(env | grep NODE_NAME | cut -f2 -d'=')
                python ${odl_path}/odlreport2db.py -x ${odl_logs}/output.xml -i ${INSTALLER_TYPE} -p ${node_name} -s ${DEPLOY_SCENARIO}
            fi
        ;;
        "tempest")
            info "Running Tempest tests..."
            python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/run_tempest.py \
                --debug -m custom ${report}
            # save tempest.conf for further troubleshooting
            tempest_conf="${RALLY_VENV_DIR}/tempest/for-deployment-*/tempest.conf"
            if [ -f ${tempest_conf} ]; then
                cp $tempest_conf ${FUNCTEST_CONF_DIR}
            fi
            clean_openstack
        ;;
        "vims")
            info "Running vIMS test..."
            python ${FUNCTEST_REPO_DIR}/testcases/vIMS/CI/vIMS.py \
                --debug ${report}
            clean_openstack
        ;;
        "rally")
            info "Running Rally benchmark suite..."
            cinder type-create volume-test #provisional
            python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/run_rally.py \
                --debug all ${report}
            cinder type-delete $(cinder type-list|grep test|awk '{print $2}')
            clean_openstack

        ;;
        "bgpvpn_template")
            info "Running BGPVPN Tempest test case..."
            tempest_dir=$(find /root/.rally -type d -name for-deploy*)
            # TODO:
            # do the call of your test case here.
            # the bgpvpn repo is cloned in $BGPVPN_REPO_DIR
            # tempest is installed in $tempest_dir
            # Suggestion:
            #   mkdir ${tempest_dir}/tempest/api/bgpvpn/
            #   cp ${BGPVPN_REPO_DIR}/networking_bgpvpn_tempest/<whatever you need> \
            #       ${tempest_dir}/tempest/api/bgpvpn/
            #   ${tempest_dir}/run_tempest.sh tempest.api.bgpvpn.<test_case_name>
       ;;
        "onos")
            info "Running ONOS test case..."
            python ${FUNCTEST_REPO_DIR}/testcases/Controllers/ONOS/Teston/CI/onosfunctest.py
      ;;
        "promise")
            info "Running PROMISE test case..."
            python ${FUNCTEST_REPO_DIR}/testcases/features/promise.py --debug all ${report}
            clean_openstack
        ;;
        "doctor")
            info "Running Doctor test..."
            python ${FUNCTEST_REPO_DIR}/testcases/features/doctor.py
        ;;
        "ovno")
            info "Running OpenContrail test..."
            # TODO
        ;;
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
        -o|--offline)
            offline=true
        ;;
        -r|--report)
            report="-r"
        ;;
        -n|--no-clean)
            clean=false
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


tests_file="/home/opnfv/functest/conf/testcase-list.txt"
if [[ -n "$DEPLOY_SCENARIO" && "$DEPLOY_SCENARIO" != "none" ]] &&\
   [[ -f $tests_file ]]; then
    arr_test=($(cat $tests_file))
else
    arr_test=(vping tempest vims rally)
fi
echo "arr_test: "${arr_test[@]}

BASEDIR=`dirname $0`
source ${BASEDIR}/common.sh


# Check that the given tests are correct
if [ "${TEST}" != "" ]; then
    arr_test_exec=(${TEST//,/ })
    for i in "${arr_test_exec[@]}"; do
        if [[ " ${arr_test[*]} " != *" $i "* ]]; then
            error "Unknown test: $i. Available tests are: ${arr_test[@]}"
        fi
    done
    info "Tests to execute: ${TEST}."
fi

if [ $offline == false ]; then
    info "MODE: online"
else
    info "MODE: offline"
fi

# Check that the functest environment has been installed
if [ ! -f ${FUNCTEST_CONF_DIR}/env_active ]; then
    error "The Functest environment is not installed. \
        Please run prepare_env.sh before running this script...."
fi


# Source credentials
info "Sourcing Credentials ${FUNCTEST_CONF_DIR}/openstack.creds to run the tests.."
source ${FUNCTEST_CONF_DIR}/openstack.creds

# Run tests
if [ "${TEST}" != "" ]; then
    for i in "${arr_test_exec[@]}"; do
        run_test $i
    done
else
    info "Executing tests..."
    for i in "${arr_test[@]}"; do
        run_test $i
    done
fi
