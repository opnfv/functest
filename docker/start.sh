#!/bin/bash

#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# Installs the Functest framework within the Docker container
# and run the tests automatically
#


config_file=$(find / -name config_functest.yaml)

REPOS_DIR=$(cat $config_file | grep -w dir_repos | awk 'END {print $NF}')
FUNCTEST_REPO_DIR=$(cat $config_file | grep -w dir_repo_functest | awk 'END {print $NF}')
RALLY_REPO_DIR=$(cat $config_file | grep -w dir_repo_rally | awk 'END {print $NF}')
RELENG_REPO_DIR=$(cat $config_file | grep -w dir_repo_releng | awk 'END {print $NF}')

FUNCTEST_DIR=$(cat $config_file | grep -w dir_functest | awk 'END {print $NF}')
FUNCTEST_RESULTS_DIR=$(cat $config_file | grep -w dir_results | awk 'END {print $NF}')
FUNCTEST_CONF_DIR=$(cat $config_file | grep -w dir_functest_conf | awk 'END {print $NF}')
FUNCTEST_DATA_DIR=$(cat $config_file | grep -w dir_functest_data | awk 'END {print $NF}')
RALLY_VENV=$(cat $config_file | grep -w dir_rally_inst | awk 'END {print $NF}')
RALLY_COMMIT=$(cat $config_file | grep -w rally_stable_commit | awk 'END {print $NF}')


echo "REPOS_DIR=${REPOS_DIR}"
echo "FUNCTEST_REPO_DIR=${FUNCTEST_REPO_DIR}"
echo "RALLY_REPO_DIR=${RALLY_REPO_DIR}"
echo "RELENG_REPO_DIR=${RELENG_REPO_DIR}"
echo "FUNCTEST_DIR=${FUNCTEST_DIR}"
echo "FUNCTEST_RESULTS_DIR=${FUNCTEST_RESULTS_DIR}"
echo "FUNCTEST_CONF_DIR=${FUNCTEST_CONF_DIR}"
echo "FUNCTEST_DATA_DIR=${FUNCTEST_DATA_DIR}"
echo "RALLY_VENV=${RALLY_VENV}"
echo "RALLY_COMMIT=${RALLY_COMMIT}"


info ()  {
    logger -s -t "start.info" "$*"
}


error () {
    logger -s -t "start.error" "$*"
    exit 1
}

# Check if environment variables are set
if [ -z ${INSTALLER_TYPE} ]; then
    error "Environment variable 'INSTALLER_TYPE' is not defined."
elif [ "${INSTALLER_TYPE}" != "fuel" ] && [ "${INSTALLER_TYPE}" != "foreman" ]; then
    error "Invalid environment variable INSTALLER_TYPE=${INSTALLER_TYPE}"
fi

if [ -z ${INSTALLER_IP} ]; then
    error "Environment variable 'INSTALLER_IP' is not defined."
fi


# Update repos
cd ${FUNCTEST_REPO_DIR}
git pull
cd ${RELENG_REPO_DIR}
git pull
cd ${RALLY_REPO_DIR}
git reset --hard ${RALLY_COMMIT}


# Create directories
mkdir -p ${FUNCTEST_CONF_DIR}
mkdir -p ${FUNCTEST_DATA_DIR}
mkdir -p ${FUNCTEST_RESULTS_DIR}/ODL

# Detect type of installer
# NOTE: this is tricky, since the IPs will have to be the same ALWAYS


# Create Openstack credentials file
${REPOS_DIR}/releng/utils/fetch_os_creds.sh -d ${FUNCTEST_CONF_DIR}/openstack.creds \
    -i ${INSTALLER_TYPE} -a ${INSTALLER_IP}
retval=$?
if [ $retval != 0 ]; then
    echo "Cannot retrieve credentials file from installation. Check logs."
    exit $retval
fi


# Source credentials
source ${FUNCTEST_CONF_DIR}/openstack.creds


# Prepare Functest Environment
echo "Functest: prepare Functest environment"
python ${FUNCTEST_REPO_DIR}/testcases/config_functest.py --debug ${FUNCTEST_REPO_DIR}/ start
retval=$?
if [ $retval != 0 ]; then
    echo "Error when configuring Functest environment"
    exit $retval
fi

# vPing
echo "Functest: run vPing"
python ${FUNCTEST_REPO_DIR}/testcases/vPing/CI/libraries/vPing.py --debug ${FUNCTEST_REPO_DIR}/ -r

# ODL
echo "Functest: run ODL suite"

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
    echo "INSTALLER_TYPE not valid."
    exit 1
fi

# rally
echo "Functest: run Functest Rally Bench suites"
python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/run_rally.py --debug ${FUNCTEST_REPO_DIR}/ all

# tempest
echo "Functest: run Tempest suite"
rally verify start smoke
rally verify list

# collect results
echo "Functest: copy results and clean Functest environment"

# save ODL results
odl_logs="${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/logs"
if [ -d ${tempest_conf} ]; then
    cp -Rf  ${odl_logs} ${FUNCTEST_CONF_DIR}/ODL/
fi

# save tempest.conf for further troubleshooting
tempest_conf="${RALLY_VENV}/tempest/for-deployment-*/tempest.conf"
if [ -f ${tempest_conf} ]; then
    cp $tempest_conf ${FUNCTEST_CONF_DIR}
fi