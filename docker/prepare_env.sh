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
    bash $(basename "$0") [-h|--help] [-t <test_name>]

where:
    -h|--help         show this help text

examples:
    $(basename "$0")"


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
        *)
            error "unknown option $1"
            exit 1
        ;;
    esac
    shift # past argument or value
done

BASEDIR=`dirname $0`
source ${BASEDIR}/common.sh

debug=""
if [[ "${CI_DEBUG,,}" == "true" ]];then
    debug="--debug"
fi


info "######### Preparing Functest environment #########"

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
python ${FUNCTEST_REPO_DIR}/testcases/config_functest.py $debug start
retval=$?
if [ $retval != 0 ]; then
    error "Error when configuring Functest environment"
    exit $retval
fi


# Generate OpenStack defaults
info "Generating OpenStack defaults..."
python ${FUNCTEST_REPO_DIR}/utils/generate_defaults.py $debug

ifconfig eth0 mtu 1450

echo "1" > ${FUNCTEST_CONF_DIR}/env_active
