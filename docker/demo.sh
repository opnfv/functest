#!/bin/bash

#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# Installs the Functest framework within the Docker container
# and run the tests automatically
#
# DO NOT USE FOR PRODUCTION.
# Changes:
#     It runs only 1 Rally bench scenario
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

echo "#############################################"
echo "############### FUNCTEST DEMO ###############"
echo "#############################################"

# Update repos
echo "---------- Updating repositories ----------"
cd ${FUNCTEST_REPO_DIR}
git pull
echo "Functest repository updated."
cd ${RELENG_REPO_DIR}
git pull
echo "Releng repository updated."
cd ${RALLY_REPO_DIR}
git reset --hard ${RALLY_COMMIT}
echo "Rally repository reset to commit ${RALLY_COMMIT}."


# Create directories
echo "---------- Creating directories ----------"
mkdir -p ${FUNCTEST_CONF_DIR}
echo "${FUNCTEST_CONF_DIR} created."
mkdir -p ${FUNCTEST_DATA_DIR}
echo "${FUNCTEST_DATA_DIR} created."
mkdir -p ${FUNCTEST_RESULTS_DIR}/ODL
echo "${FUNCTEST_RESULTS_DIR}/ODL created."



# Create Openstack credentials file
echo "---------- Retrieving Credentials from Fuel ----------"
${REPOS_DIR}/releng/utils/fetch_os_creds.sh -d ${FUNCTEST_CONF_DIR}/openstack.creds \
    -i ${INSTALLER_TYPE} -a ${INSTALLER_IP}
retval=$?
if [ $retval != 0 ]; then
    echo "Cannot retrieve credentials file from installation. Check logs."
    exit $retval
fi
echo "Credentials succesfully stored in ${FUNCTEST_CONF_DIR}/openstack.creds"

# Source credentials
echo "---------- Sourcing Openstack Credentials  ----------"
source ${FUNCTEST_CONF_DIR}/openstack.creds


# Prepare Functest Environment
echo "---------- Preparing Functest environment  ----------"
python ${FUNCTEST_REPO_DIR}/testcases/config_functest.py --debug ${FUNCTEST_REPO_DIR}/ start
retval=$?
if [ $retval != 0 ]; then
    echo "Error when configuring Functest environment"
    exit $retval
fi

# vPing
echo "----------------------------------------------"
echo "---------- Running vPING test case  ----------"
echo "----------------------------------------------"
python ${FUNCTEST_REPO_DIR}/testcases/vPing/CI/libraries/vPing.py --debug ${FUNCTEST_REPO_DIR}/ -r

# ODL
echo "----------------------------------------------"
echo "---------- Running ODL test case  ----------"
echo "----------------------------------------------"
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
echo "----------------------------------------------"
echo "------- Running Rally bench test case  -------"
echo "----------------------------------------------"
echo "Functest: run Functest Rally Bench suites"
python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/run_rally.py --debug ${FUNCTEST_REPO_DIR}/ glance

# tempest
echo "----------------------------------------------"
echo "-------- Running Tempest smoke tests  --------"
echo "----------------------------------------------"
echo "Functest: run Tempest suite"
rally verify start smoke
rally verify list
