#!/bin/bash

#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# Installs the Functest framework within the Docker container
# and run the tests automatically
#

usage="Script to prepare the Functest environment.

usage:
    bash $(basename "$0") [--offline] [-h|--help] [-t <test_name>]

where:
    -o|--offline      optional offline mode (experimental)
    -h|--help         show this help text

examples:
    $(basename "$0")
    $(basename "$0") --offline"

offline=false

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
        *)
            error "unknown option $1"
            exit 1
        ;;
    esac
    shift # past argument or value
done

BASEDIR=`dirname $0`
source ${BASEDIR}/common.sh

# Support for Functest offline
# NOTE: Still not 100% working when running the tests

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

    info "Updating vIMS test repository...."
    cd ${VIMS_TEST_REPO_DIR}
    if [ ${VIMS_TEST_BRANCH} != "stable" ]; then
        info "Releng repo: checkout ${VIMS_TEST_BRANCH} branch..."
        git checkout ${VIMS_TEST_BRANCH}
    fi
    info "vIMS test repo: pulling to latest..."
    git pull
    if [ ${VIMS_TEST_COMMIT} != "latest" ]; then
        info "vIMS test repo: given commit is ${VIMS_TEST_COMMIT}. Reseting..."
        git reset --hard ${VIMS_TEST_COMMIT}
    fi
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



# Create Openstack credentials file
${REPOS_DIR}/releng/utils/fetch_os_creds.sh -d ${FUNCTEST_CONF_DIR}/openstack.creds \
    -i ${INSTALLER_TYPE} -a ${INSTALLER_IP}
retval=$?
if [ $retval != 0 ]; then
    error "Cannot retrieve credentials file from installation. Check logs."
    exit $retval
fi


# Source credentials
source ${FUNCTEST_CONF_DIR}/openstack.creds


# Prepare Functest Environment
info "Functest: prepare Functest environment"
python ${FUNCTEST_REPO_DIR}/testcases/config_functest.py --debug ${FUNCTEST_REPO_DIR}/ start
retval=$?
if [ $retval != 0 ]; then
    error "Error when configuring Functest environment"
    exit $retval
fi

echo "1" > ${FUNCTEST_CONF_DIR}/env_active
