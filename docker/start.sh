#!/bin/bash

#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# Installs the Functest framework within the Docker container
# and run the tests automatically
#


REPOS_DIR=/home/repos
FUNCTEST_REPO_DIR=${REPOS_DIR}/functest
HOME=/home


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
cd ${REPOS_DIR}/functest
git pull
cd ${REPOS_DIR}/releng
git pull


# Detect type of installer
# NOTE: this is tricky, since the IPs will have to be the same ALWAYS



# Create Openstack credentials file
${REPOS_DIR}/releng/utils/fetch_os_creds.sh -d /root/openstack.creds \
    -i ${INSTALLER_TYPE} -a ${INSTALLER_IP}

if [ $? -ne 0 ]; then
    error "Cannot retrieve credentials file from installation. Check logs."
    exit 1
fi

# Source credentials
source /root/openstack.creds


# Prepare Functest Environment
echo "Functest: prepare Functest environment"
    python ${FUNCTEST_REPO_DIR}/testcases/config_functest.py --debug ${FUNCTEST_REPO_DIR}/ start
    if [ $? != 0 ]; then
        echo "Error when configuring Functest environment"
        exit 1
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
cp -Rf ${FUNCTEST_REPO_DIR}/testcases/Controllers/ODL/CI/logs $HOME/functest/results/ODL

# save tempest.conf for further troubleshooting
cp $HOME/.rally/tempest/for-deployment-*/tempest.conf $HOME/functest/results


