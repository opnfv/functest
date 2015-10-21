#!/bin/bash

#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# Installs the Functest framework within the Docker container
# and run the tests automatically
#

BASEDIR=`dirname $0`
source ${BASEDIR}/common.sh

if [ ! -f ${FUNCTEST_CONF_DIR}/env_active ]; then
    error "The Functest environment is not installed. \
        Please run prepare_env.sh before running this script...."
fi

# Support for Functest offline
# NOTE: Still not 100% working when running the tests
offline=false
if [ ! -z "$1" ] && [ $1 == "--offline" ]; then
    offline=true
fi


# Source credentials
info "Sourcing Credentials ${FUNCTEST_CONF_DIR}/openstack.creds again to run the tests.."
source ${FUNCTEST_CONF_DIR}/openstack.creds


# vPing
echo "----------------------------------------------"
echo "---------- Running vPING test case  ----------"
echo "----------------------------------------------"
info "Running vPing"
python ${FUNCTEST_REPO_DIR}/testcases/vPing/CI/libraries/vPing.py --debug ${FUNCTEST_REPO_DIR}/ -r



# ODL
echo "----------------------------------------------"
echo "----------- Running ODL test case  -----------"
echo "----------------------------------------------"
info "Functest: run ODL suite"
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



# rally
echo "----------------------------------------------"
echo "--------- Running Rally bench suite  ---------"
echo "----------------------------------------------"
info "Running Rally Bench suites"
python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/run_rally.py --debug ${FUNCTEST_REPO_DIR}/ all



# tempest
echo "----------------------------------------------"
echo "-------- Running Tempest smoke tests  --------"
echo "----------------------------------------------"
info "Running Tempest suite..."
rally verify start smoke
rally verify list




# collect results
# NOTE: To be removed when all the resuls are pushed to the DB
info "Functest: copy results and clean Functest environment"

# save ODL results
odl_logs="${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/logs"
if [ -d ${tempest_conf} ]; then
    cp -Rf  ${odl_logs} ${FUNCTEST_CONF_DIR}/ODL/
fi

# save tempest.conf for further troubleshooting
tempest_conf="${RALLY_VENV_DIR}/tempest/for-deployment-*/tempest.conf"
if [ -f ${tempest_conf} ]; then
    cp $tempest_conf ${FUNCTEST_CONF_DIR}
fi
