#!/bin/bash

#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# Installs the Functest framework within the Docker container
# and run the tests automatically
#

usage="Script to trigger the tests automatically.

usage:
    bash $(basename "$0") [--offline] [-h|--help] [-t <test_name>]

where:
    -o|--offline      optional offline mode (experimental)
    -h|--help         show this help text
    -t|--test         run specific set of tests
      <test_name>     one or more of the following: vping,odl,rally,tempest. Separated by comma.


examples:
    $(basename "$0")
    $(basename "$0") --test vping,odl
    $(basename "$0") --offline -t tempest,rally"


# Support for Functest offline
# NOTE: Still not 100% working when running the tests
offline=false
arr_test=(vping odl rally tempest)


function run_test(){
    test_name=$1
    echo "----------------------------------------------"
    echo "------------- Running $i test case  "
    echo "----------------------------------------------"
    case $test_name in
        "vping")
            python ${FUNCTEST_REPO_DIR}/testcases/vPing/CI/libraries/vPing.py --debug ${FUNCTEST_REPO_DIR}/ -r
        ;;
        "odl")
            if [ $INSTALLER_TYPE == "fuel" ]; then
                odl_ip=$(keystone catalog --service network | grep publicURL | cut -f3 -d"/" | cut -f1 -d":")
                neutron_ip=$(keystone catalog --service identity | grep publicURL | cut -f3 -d"/" | cut -f1 -d":")
                usr_name=$(env | grep OS | grep OS_USERNAME | cut -f2 -d'=')
                pass=$(env | grep OS | grep OS_PASSWORD | cut -f2 -d'=')
                odl_port=8181
                ODL_PORT=$odl_port ODL_IP=$odl_ip NEUTRON_IP=$neutron_ip USR_NAME=$usr_name PASS=$pass \
                ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/start_tests.sh
            elif [ $INSTALLER_TYPE == "foreman" ]; then
                #odl_port=8081
                ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/start_tests.sh
            else
                error "INSTALLER_TYPE not valid."
                exit 1
            fi
            # save ODL results
            odl_logs="${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/logs"
            if [ -d ${odl_logs} ]; then
                cp -Rf  ${odl_logs} ${FUNCTEST_CONF_DIR}/ODL/
            fi
        ;;
        "rally")
            python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/run_rally.py --debug ${FUNCTEST_REPO_DIR}/ all
        ;;
        "tempest")
            rally verify start smoke
            rally verify list
            # save tempest.conf for further troubleshooting
            tempest_conf="${RALLY_VENV_DIR}/tempest/for-deployment-*/tempest.conf"
            if [ -f ${tempest_conf} ]; then
                cp $tempest_conf ${FUNCTEST_CONF_DIR}
            fi
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
        -t|--tests)
            TEST="$2"
            shift
        ;;
        --default)
            DEFAULT=YES
        ;;
        *)
            echo "unknown option $1 $2"
            exit 1
        ;;
    esac
    shift # past argument or value
done

BASEDIR=`dirname $0`
source ${BASEDIR}/common.sh


# Check that the given tests are correct
if [ $TEST != "" ]; then
    arr_test_exec=(${TEST//,/ })
    for i in "${arr_test_exec[@]}"; do
        if [[ " ${arr_test[*]} " != *" $i "* ]]; then
            error "Unknown test: $i. Available tests are: ${arr_test[@]}"
        fi
    done
    info "Tests to execute: ${TEST}."
fi

if [ $offline == true ]; then
    info "OFFLINE_MODE..."
fi

# Check that the functest environment has been installed
if [ ! -f ${FUNCTEST_CONF_DIR}/env_active ]; then
    error "The Functest environment is not installed. \
        Please run prepare_env.sh before running this script...."
fi


# Source credentials
info "Sourcing Credentials ${FUNCTEST_CONF_DIR}/openstack.creds to run the tests.."
source ${FUNCTEST_CONF_DIR}/openstack.creds




if [ $TEST != "" ]; then
    for i in "${arr_test_exec[@]}"; do
        run_test $i
    done
else
    info "Executing all the tests"
    for i in "${arr_test[@]}"; do
        run_test $i
    done
fi




