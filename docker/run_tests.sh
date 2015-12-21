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
    -r|--report       push results to database (false by default)
    -t|--test         run specific set of tests
      <test_name>     one or more of the following: vping,odl,rally,tempest,vims. Separated by comma.


examples:
    $(basename "$0")
    $(basename "$0") --test vping,odl
    $(basename "$0") --offline -t tempest,rally"


# Support for Functest offline
# NOTE: Still not 100% working when running the tests
offline=false
report=""
arr_test=(vping odl tempest vims rally)

function clean_openstack(){
    python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/clean_openstack.py \
        --debug ${FUNCTEST_REPO_DIR}/
}

function run_test(){
    test_name=$1
    echo "----------------------------------------------"
    echo "------------- Running $i test case  "
    echo "----------------------------------------------"
    case $test_name in
        "vping")
            info "Running vPing test..."
            python ${FUNCTEST_REPO_DIR}/testcases/vPing/CI/libraries/vPing.py \
                --debug ${FUNCTEST_REPO_DIR}/ ${report}
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
                pass
            elif [ $INSTALLER_TYPE == "joid" ]; then
                pass
            elif [ $INSTALLER_TYPE == "compass" ]; then
                pass
            else
                error "INSTALLER_TYPE not valid."
                exit 1
            fi
            ODL_PORT=$odl_port ODL_IP=$odl_ip NEUTRON_IP=$neutron_ip USR_NAME=$usr_name PASS=$password \
                ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/start_tests.sh

            # save ODL results
            odl_logs="${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/logs"
            if [ -d ${odl_logs} ]; then
                cp -Rf  ${odl_logs} ${FUNCTEST_CONF_DIR}/ODL/
            fi
        ;;
        "tempest")
            info "Running Tempest smoke tests..."
            python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/run_tempest.py \
                --debug ${FUNCTEST_REPO_DIR}/ -m smoke ${report}
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
                --debug ${FUNCTEST_REPO_DIR}/ ${report}
            clean_openstack
        ;;
        "rally")
            info "Running Rally benchmark suite..."
            python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/run_rally.py \
                --debug ${FUNCTEST_REPO_DIR}/ all ${report}
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

# Check OpenStack
info "Checking that the basic OpenStack services are functional..."
${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/check_os.sh

# Run tests
if [ "${TEST}" != "" ]; then
    for i in "${arr_test_exec[@]}"; do
        run_test $i
    done
else
    info "Executing all the tests"
    for i in "${arr_test[@]}"; do
        run_test $i
    done
fi
