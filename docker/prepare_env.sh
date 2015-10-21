#!/bin/bash

#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# Installs the Functest framework within the Docker container
# and run the tests automatically
#

BASEDIR=`dirname $0`
source ${BASEDIR}/common.sh

# Support for Functest offline
# NOTE: Still not 100% working when running the tests
offline=false
if [ ! -z "$1" ] && [ $1 == "--offline" ]; then
    offline=true
fi

info "######### Preparing Functest environment #########"
if [ $offline == false ]; then
    info "MODE: online"
else
    info "MODE: offline"
fi


# Check if environment variables are set
info "Checking environment variables INSTALLER_TYPE and INSTALLER_IP"
if [ -z ${INSTALLER_TYPE} ]; then
    error "Environment variable 'INSTALLER_TYPE' is not defined."
elif [ "${INSTALLER_TYPE}" != "fuel" ] && [ "${INSTALLER_TYPE}" != "foreman" ]; then
    error "Invalid environment variable INSTALLER_TYPE=${INSTALLER_TYPE}"
fi
info "INSTALLER_TYPE env variable found: ${INSTALLER_TYPE}"

if [ -z ${INSTALLER_IP} ]; then
    error "Environment variable 'INSTALLER_IP' is not defined."
fi
info "INSTALLER_IP env variable found: ${INSTALLER_IP}"


if [ $offline == false ]; then
    # Update repos
    info "Updating Functest repository...."
    cd ${FUNCTEST_REPO_DIR}
    if [ ${FUNCTEST_BRANCH} != "master" ]; then
        info "Functest repo: checkout ${FUNCTEST_BRANCH} branch..."
        git checkout ${FUNCTEST_BRANCH}
    fi
    info "Functest repo: pulling to latest..."
    git pull
    if [ ${FUNCTEST_COMMIT} != "latest" ]; then
        info "Functest repo: given commit is ${FUNCTEST_COMMIT}. Reseting..."
        git reset --hard ${FUNCTEST_COMMIT}
    fi

    info "Updating Releng repository...."
    cd ${RELENG_REPO_DIR}
    if [ ${RELENG_BRANCH} != "master" ]; then
        info "Releng repo: checkout ${RELENG_BRANCH} branch..."
        git checkout ${RELENG_BRANCH}
    fi
    info "Releng repo: pulling to latest..."
    git pull
    if [ ${RELENG_COMMIT} != "latest" ]; then
        info "Releng repo: given commit is ${RELENG_COMMIT}. Reseting..."
        git reset --hard ${RELENG_COMMIT}
    fi

    info "Updating Rally repository...."
    cd ${RALLY_REPO_DIR}
    info "Rally repo: pulling to latest..."
    git pull
fi

# We do this regardless if its online or offline mode.
if [ ${RALLY_COMMIT} != "latest" ]; then
    info "Rally repo: given commit is ${RALLY_COMMIT}. Reseting..."
    git reset --hard ${RALLY_COMMIT}
fi


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

echo "1" > ${FUNCTEST_CONF_DIR}/env_active
