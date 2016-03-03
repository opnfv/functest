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
    -s|--serial       run tests in one thread
    -t|--test         run specific set of tests
      <test_name>     one or more of the following separated by comma:
                            vping_ssh,vping_userdata,odl,onos,tempest,rally,vims,promise,doctor


examples:
    $(basename "$0")
    $(basename "$0") --test vping_ssh,odl
    $(basename "$0") -t tempest,rally"


# Support for Functest offline
# NOTE: Still not 100% working when running the tests
offline=false
report=""
clean=true
serial=false

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

function odl_tests(){
    keystone_ip=$(openstack catalog show identity |grep publicURL| cut -f3 -d"/" | cut -f1 -d":")
    # historically most of the installers use the same IP for neutron and keystone API
    neutron_ip=$keystone_ip
    odl_ip=$(openstack catalog show network | grep publicURL | cut -f3 -d"/" | cut -f1 -d":")
    usr_name=$(env | grep OS | grep OS_USERNAME | cut -f2 -d'=')
    password=$(env | grep OS | grep OS_PASSWORD | cut -f2 -d'=')
    odl_port=8181
    if [ $INSTALLER_TYPE == "fuel" ]; then
        odl_port=8282
    elif [ $INSTALLER_TYPE == "apex" ]; then
        :
    elif [ $INSTALLER_TYPE == "joid" ]; then
        odl_ip=$(env | grep SDN_CONTROLLER | cut -f2 -d'=')
        neutron_ip=$(openstack catalog show network | grep publicURL | cut -f3 -d"/" | cut -f1 -d":")
        odl_port=8080
        :
    elif [ $INSTALLER_TYPE == "compass" ]; then
        :
    else
        error "INSTALLER_TYPE not valid."
        exit 1
    fi
}
function run_test(){
    test_name=$1
    echo -e "\n\n\n\n"
    echo "----------------------------------------------"
    echo "  Running test case: $i"
    echo "----------------------------------------------"
    echo ""
    clean_flag=""
    if [ $clean == "false" ]; then
        clean_flag="-n"
    fi
    serial_flag=""
    if [ $serial == "true" ]; then
        serial_flag="-s"
    fi

    case $test_name in
        "vping_ssh")
            info "Running vPing-SSH test..."
            python ${FUNCTEST_REPO_DIR}/testcases/vPing/CI/libraries/vPing_ssh.py \
                --debug $clean_flag ${report}
        ;;
        "vping_userdata")
            info "Running vPing-userdata test... "
            python ${FUNCTEST_REPO_DIR}/testcases/vPing/CI/libraries/vPing_userdata.py \
                --debug $clean_flag ${report}
        ;;
        "odl")
            info "Running ODL test..."
            odl_tests
            ODL_PORT=$odl_port ODL_IP=$odl_ip KEYSTONE_IP=$keystone_ip NEUTRON_IP=$neutron_ip USR_NAME=$usr_name PASS=$password \
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
                --debug $serial_flag $clean_flag -m custom ${report}
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
                --debug $clean_flag ${report}
            clean_openstack
        ;;
        "rally")
            info "Running Rally benchmark suite..."
            python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/run_rally-cert.py \
                --debug $clean_flag all ${report}
            clean_openstack

        ;;
        "bgpvpn")
            info "Running BGPVPN Tempest test case..."
            tempest_dir=$(ls -t /home/opnfv/.rally/tempest/ |grep for-deploy |tail -1)
            tempest_dir=/home/opnfv/.rally/tempest/$tempest_dir
            if [[ $tempest_dir == "" ]]; then
                echo "Make sure tempest was running before"
                exit 1
            fi

            tempest_conf=$(find $tempest_dir -name tempest.conf)
            pushd $tempest_dir
              . .venv/bin/activate
              pip install --no-deps -e ~/repos/bgpvpn/.
              mkdir -p /etc/tempest/
              cp $tempest_conf /etc/tempest/tempest.conf
              echo "[service_available]
bgpvpn = True" >> /etc/tempest/tempest.conf
              ./run_tempest.sh -- networking_bgpvpn_tempest
              rm -rf /etc/tempest/tempest.conf
            popd
        ;;
        "odl-vpnservice")
            info "Running VPNSERVICE Robot test case..."
            odl_tests
            cp ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/test_list.txt \
                ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/test_list.txt.bak
            echo "test/csit/suites/vpnservice" > ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/test_list.txt
            ODL_PORT=$odl_port ODL_IP=$odl_ip KEYSTONE_IP=$keystone_ip NEUTRON_IP=$neutron_ip USR_NAME=$usr_name PASS=$password \
                ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/start_tests.sh
            cp ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/test_list.txt.bak \
                ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/test_list.txt
            # TODO: copy logs
       ;;
        "onos")
            info "Running ONOS test case..."
            if [ $INSTALLER_TYPE == "joid" ]; then
                python ${FUNCTEST_REPO_DIR}/testcases/Controllers/ONOS/Teston/CI/onosfunctest.py -i joid
            else
                python ${FUNCTEST_REPO_DIR}/testcases/Controllers/ONOS/Teston/CI/onosfunctest.py
            fi
      ;;
        "promise")
            info "Running PROMISE test case..."
            python ${FUNCTEST_REPO_DIR}/testcases/features/promise.py --debug ${report}
            sleep 10 #to let the instances terminate
            clean_openstack
        ;;
        "doctor")
            info "Running Doctor test..."
            python ${FUNCTEST_REPO_DIR}/testcases/features/doctor.py
        ;;
        "ovno")
            info "Running OpenContrail test..."
            ${repos_dir}/ovno/Testcases/RunTests.sh
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


tests_file="/home/opnfv/functest/conf/testcase-list.txt"
if [[ -n "$DEPLOY_SCENARIO" && "$DEPLOY_SCENARIO" != "none" ]] &&\
   [[ -f $tests_file ]]; then
    arr_test=($(cat $tests_file))
else
    arr_test=(vping_ssh tempest vims rally)
fi

BASEDIR=`dirname $0`
source ${BASEDIR}/common.sh

info "Tests to be executed: ${arr_test[@]}"

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
