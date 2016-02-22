#!/bin/bash

#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# Installs the Functest framework within the Docker container
# and run the tests automatically
#
# If config_functest.yaml is given by the docker run command,
# it must be run like this:
#
#   docker run -ti \
#      -e "INSTALLER_TYPE=<something>" \
#      -e "INSTALLER_IP=<ip>" \
#      -v $(pwd)/config_functest.yaml:/home/opnfv/functest/conf/config_functest.yaml \
#      opnfv/functest /bin/bash
#
# NOTE: $(pwd)/config_functest.yaml means that it will take the one in the
#       current directory.
#
# If it is not provided, take the existing one in the functest repo
#

# this pull is to be removed right before the B release, once we build
# a release candidate docker
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

mkdir -p /home/opnfv/functest/conf
config_file=/home/opnfv/functest/conf/config_functest.yaml
if [ ! -f ${config_file} ]; then
    default_config_file=$(find /home/opnfv/repos -name config_functest.yaml)
    cp $default_config_file $config_file
    echo "config_functest.yaml not provided. Using default one"
fi


# Parse config_functest.yaml file
# TODO: this is not the best way to parse a yaml file in bash...

# Directories
REPOS_DIR=$(cat $config_file | grep -w dir_repos | awk 'END {print $NF}')
FUNCTEST_REPO_DIR=$(cat $config_file | grep -w dir_repo_functest | awk 'END {print $NF}')
RALLY_REPO_DIR=$(cat $config_file | grep -w dir_repo_rally | awk 'END {print $NF}')
RELENG_REPO_DIR=$(cat $config_file | grep -w dir_repo_releng | awk 'END {print $NF}')
VIMS_REPO_DIR=$(cat $config_file | grep -w dir_repo_vims_test | awk 'END {print $NF}')
BGPVPN_REPO_DIR=$(cat $config_file | grep -w dir_repo_bgpvpn | awk 'END {print $NF}')
ONOS_REPO_DIR=$(cat $config_file | grep -w dir_repo_onos | awk 'END {print $NF}')
PROMISE_REPO_DIR=$(cat $config_file | grep -w dir_repo_promise | awk 'END {print $NF}')
OVNO_REPO_DIR=$(cat $config_file | grep -w dir_repo_ovno | awk 'END {print $NF}')
DOCTOR_REPO_DIR=$(cat $config_file | grep -w dir_repo_doctor | awk 'END {print $NF}')


FUNCTEST_DIR=$(cat $config_file | grep -w dir_functest | awk 'END {print $NF}')
FUNCTEST_RESULTS_DIR=$(cat $config_file | grep -w dir_results | awk 'END {print $NF}')
FUNCTEST_CONF_DIR=$(cat $config_file | grep -w dir_functest_conf | awk 'END {print $NF}')
FUNCTEST_DATA_DIR=$(cat $config_file | grep -w dir_functest_data | awk 'END {print $NF}')
RALLY_VENV_DIR=$(cat $config_file | grep -w dir_rally_inst | awk 'END {print $NF}')

# Repos
RALLY_BRANCH=$(cat $config_file | grep -w rally_branch | awk 'END {print $NF}')
RALLY_COMMIT=$(cat $config_file | grep -w rally_commit | awk 'END {print $NF}')
RELENG_BRANCH=$(cat $config_file | grep -w releng_branch | awk 'END {print $NF}')
RELENG_COMMIT=$(cat $config_file | grep -w releng_commit | awk 'END {print $NF}')
VIMS_BRANCH=$(cat $config_file | grep -w vims_test_branch | awk 'END {print $NF}')
VIMS_COMMIT=$(cat $config_file | grep -w vims_test_commit | awk 'END {print $NF}')
BGPVPN_BRANCH=$(cat $config_file | grep -w bgpvpn_branch | awk 'END {print $NF}')
BGPVPN_COMMIT=$(cat $config_file | grep -w bgpvpn_commit | awk 'END {print $NF}')
ONOS_BRANCH=$(cat $config_file | grep -w onos_branch | awk 'END {print $NF}')
ONOS_COMMIT=$(cat $config_file | grep -w onos_commit | awk 'END {print $NF}')
PROMISE_BRANCH=$(cat $config_file | grep -w promise_branch | awk 'END {print $NF}')
PROMISE_COMMIT=$(cat $config_file | grep -w promise_commit | awk 'END {print $NF}')
OVNO_BRANCH=$(cat $config_file | grep -w ovno_branch | awk 'END {print $NF}')
OVNO_COMMIT=$(cat $config_file | grep -w ovno_commit | awk 'END {print $NF}')
DOCTOR_BRANCH=$(cat $config_file | grep -w doctor_branch | awk 'END {print $NF}')
DOCTOR_COMMIT=$(cat $config_file | grep -w doctor_commit | awk 'END {print $NF}')

echo "_____Parsed needed data from ${config_file}:"
echo "####### Directories #######"
echo "REPOS_DIR=${REPOS_DIR}"
echo "FUNCTEST_REPO_DIR=${FUNCTEST_REPO_DIR}"
echo "RALLY_REPO_DIR=${RALLY_REPO_DIR}"
echo "RELENG_REPO_DIR=${RELENG_REPO_DIR}"
echo "VIMS_REPO_DIR=${VIMS_REPO_DIR}"
echo "FUNCTEST_DIR=${FUNCTEST_DIR}"
echo "FUNCTEST_RESULTS_DIR=${FUNCTEST_RESULTS_DIR}"
echo "FUNCTEST_CONF_DIR=${FUNCTEST_CONF_DIR}"
echo "FUNCTEST_DATA_DIR=${FUNCTEST_DATA_DIR}"
echo "RALLY_VENV_DIR=${RALLY_VENV_DIR}"
echo "####### Repositories #######"
echo "RELENG_BRANCH=${RELENG_BRANCH}"
echo "RELENG_COMMIT=${RELENG_COMMIT}"
echo "RALLY_BRANCH=${RALLY_BRANCH}"
echo "RALLY_COMMIT=${RALLY_COMMIT}"
echo "VIMS_BRANCH=${VIMS_BRANCH}"
echo "VIMS_COMMIT=${VIMS_COMMIT}"
echo "ONOS_BRANCH=${ONOS_BRANCH}"
echo "ONOS_COMMIT=${ONOS_COMMIT}"
echo "PROMISE_BRANCH=${PROMISE_BRANCH}"
echo "PROMISE_COMMIT=${PROMISE_COMMIT}"
echo "OVNO_BRANCH=${OVNO_BRANCH}"
echo "OVNO_COMMIT=${OVNO_COMMIT}"
echo "DOCTOR_BRANCH=${DOCTOR_BRANCH}"
echo "DOCTOR_COMMIT=${DOCTOR_COMMIT}"
echo "############################"

info ()  {
    logger -s -t "FUNCTEST.info" "$*"
}


error () {
    logger -s -t "FUNCTEST.error" "$*"
    exit 1
}
