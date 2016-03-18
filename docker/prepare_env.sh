#!/bin/bash

#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# Installs the Functest framework within the Docker container
# and run the tests automatically
#
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
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

# definition of available installer names
INSTALLERS=(fuel compass apex joid)

if [ ! -f ${FUNCTEST_CONF_DIR}/openstack.creds ]; then
    # If credentials file is not given, check if environment variables are set
    # to get the creds using fetch_os_creds.sh later on
    info "Checking environment variables INSTALLER_TYPE and INSTALLER_IP"
    if [ -z ${INSTALLER_TYPE} ]; then
        error "Environment variable 'INSTALLER_TYPE' is not defined."
    elif [[ ${INSTALLERS[@]} =~ ${INSTALLER_TYPE} ]]; then
        info "INSTALLER_TYPE env variable found: ${INSTALLER_TYPE}"
    else
        error "Invalid environment variable INSTALLER_TYPE=${INSTALLER_TYPE}"
    fi

    if [ -z ${INSTALLER_IP} ]; then
        error "Environment variable 'INSTALLER_IP' is not defined."
    fi
    info "INSTALLER_IP env variable found: ${INSTALLER_IP}"
fi


if [ $offline == false ]; then
    # Update repos
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
    if [ ${RALLY_BRANCH} != "master" ]; then
        info "Rally repo: checkout ${RALLY_BRANCH} branch..."
        git checkout ${RALLY_BRANCH}
    fi
    info "Rally repo: pulling to latest..."
    git pull
    # We leave the reset command for later.

    info "Updating vIMS test repository...."
    cd ${VIMS_REPO_DIR}
    if [ ${VIMS_BRANCH} != "stable" ]; then
        info "Releng repo: checkout ${VIMS_TEST_BRANCH} branch..."
        git checkout ${VIMS_BRANCH}
    fi
    info "vIMS test repo: pulling to latest..."
    git pull
    if [ ${VIMS_COMMIT} != "latest" ]; then
        info "vIMS test repo: given commit is ${VIMS_TEST_COMMIT}. Reseting..."
        git reset --hard ${VIMS_COMMIT}
    fi

    info "Updating BGPVPN repository...."
    cd ${BGPVPN_REPO_DIR}
    if [ ${BGPVPN_BRANCH} != "master" ]; then
        info "BGPVPN repo: checkout ${BGPVPN_BRANCH} branch..."
        git checkout ${BGPVPN_BRANCH}
    fi
    info "BGPVPN repo: pulling to latest..."
    git pull
    if [ ${BGPVPN_COMMIT} != "latest" ]; then
        info "BGPVPN repo: given commit is ${BGPVPN_COMMIT}. Reseting..."
        git reset --hard ${BGPVPN_COMMIT}
    fi

    info "Updating ONOS repository...."
    cd ${ONOS_REPO_DIR}
    if [ ${ONOS_BRANCH} != "master" ]; then
        info "ONOS repo: checkout ${ONOS} branch..."
        git checkout ${ONOS_BRANCH}
    fi
    info "ONOS repo: pulling to latest..."
    git pull
    if [ ${ONOS_COMMIT} != "latest" ]; then
        info "ONOS repo: given commit is ${ONOS_COMMIT}. Reseting..."
        git reset --hard ${ONOS_COMMIT}
    fi

    info "Updating PROMISE repository...."
    cd ${PROMISE_REPO_DIR}
    if [ ${PROMISE_BRANCH} != "master" ]; then
        info "PROMISE repo: checkout ${PROMISE} branch..."
        git checkout ${PROMISE_BRANCH}
    fi
    info "PROMISE repo: pulling to latest..."
    git pull
    if [ ${PROMISE_COMMIT} != "latest" ]; then
        info "PROMISE repo: given commit is ${PROMISE_COMMIT}. Reseting..."
        git reset --hard ${PROMISE_COMMIT}
    fi

    info "Updating OVNO repository...."
    cd ${OVNO_REPO_DIR}
    if [ ${OVNO_BRANCH} != "master" ]; then
        info "OVNO repo: checkout ${OVNO} branch..."
        git checkout ${OVNO_BRANCH}
    fi
    info "OVNO repo: pulling to latest..."
    git pull
    if [ ${OVNO_COMMIT} != "latest" ]; then
        info "OVNO repo: given commit is ${OVNO_COMMIT}. Reseting..."
        git reset --hard ${OVNO_COMMIT}
    fi

    info "Updating DOCTOR repository...."
    cd ${DOCTOR_REPO_DIR}
    if [ ${DOCTOR_BRANCH} != "master" ]; then
        info "DOCTOR repo: checkout ${DOCTOR} branch..."
        git checkout ${DOCTOR_BRANCH}
    fi
    info "DOCTOR repo: pulling to latest..."
    git pull
    if [ ${DOCTOR_COMMIT} != "latest" ]; then
        info "DOCTOR repo: given commit is ${DOCTOR_COMMIT}. Reseting..."
        git reset --hard ${DOCTOR_COMMIT}
    fi
fi

# We do this regardless if its online or offline mode.
# Assumption: the docker image contains a newer rally repo than the given commit.
if [ ${RALLY_COMMIT} != "latest" ]; then
    cd ${RALLY_REPO_DIR}
    info "Rally repo: given commit is ${RALLY_COMMIT}. Reseting..."
    git reset --hard ${RALLY_COMMIT}
fi

# IMPORTANT: To be removed when version 0.2.1 is out
git config --global user.email "functest@opnfv.com"
git config --global user.name "opnfv/functest"
git fetch https://review.openstack.org/openstack/rally refs/changes/06/270506/9 && git cherry-pick FETCH_HEAD


# Create directories
mkdir -p ${FUNCTEST_CONF_DIR}
mkdir -p ${FUNCTEST_DATA_DIR}
mkdir -p ${FUNCTEST_RESULTS_DIR}/ODL



# Create Openstack credentials file
# $creds is an env varialbe in the docker container pointing to
# /home/opnfv/functest/conf/openstack.creds
if [ ! -f ${creds} ]; then
    ${REPOS_DIR}/releng/utils/fetch_os_creds.sh -d ${creds} \
        -i ${INSTALLER_TYPE} -a ${INSTALLER_IP}
    retval=$?
    if [ $retval != 0 ]; then
        error "Cannot retrieve credentials file from installation. Check logs."
        exit $retval
    fi
else
    info "OpenStack credentials file given to the docker and stored in ${FUNCTEST_CONF_DIR}/openstack.creds."
fi

# If we use SSL, by default use option OS_INSECURE=true which means that
# the cacert will be self-signed
if grep -Fq "OS_CACERT" ${creds}; then
    echo "OS_INSECURE=true">>${creds};
fi

# Source credentials
source ${creds}

# Check OpenStack
info "Checking that the basic OpenStack services are functional..."
${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/check_os.sh
RETVAL=$?
if [ $RETVAL -ne 0 ]; then
    exit 1
fi

# Prepare Functest Environment
info "Preparing Functest environment..."
python ${FUNCTEST_REPO_DIR}/testcases/config_functest.py --debug start
retval=$?
if [ $retval != 0 ]; then
    error "Error when configuring Functest environment"
    exit $retval
fi


# Generate OpenStack defaults
info "Generating OpenStack defaults..."
python ${FUNCTEST_REPO_DIR}/testcases/VIM/OpenStack/CI/libraries/generate_defaults.py -d


ifconfig eth0 mtu 1450

echo "1" > ${FUNCTEST_CONF_DIR}/env_active
