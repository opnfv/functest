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
config_file=/home/opnfv/functest/conf/config_functest.yaml
if [ ! -f ${config_file} ]; then
    config_file=$(find / -name config_functest.yaml)
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

FUNCTEST_DIR=$(cat $config_file | grep -w dir_functest | awk 'END {print $NF}')
FUNCTEST_RESULTS_DIR=$(cat $config_file | grep -w dir_results | awk 'END {print $NF}')
FUNCTEST_CONF_DIR=$(cat $config_file | grep -w dir_functest_conf | awk 'END {print $NF}')
FUNCTEST_DATA_DIR=$(cat $config_file | grep -w dir_functest_data | awk 'END {print $NF}')
RALLY_VENV_DIR=$(cat $config_file | grep -w dir_rally_inst | awk 'END {print $NF}')

# Repos
RALLY_BRANCH=$(cat $config_file | grep -w rally_branch | awk 'END {print $NF}')
RALLY_COMMIT=$(cat $config_file | grep -w rally_commit | awk 'END {print $NF}')
FUNCTEST_BRANCH=$(cat $config_file | grep -w functest_branch | awk 'END {print $NF}')
FUNCTEST_COMMIT=$(cat $config_file | grep -w functest_commit | awk 'END {print $NF}')
RELENG_BRANCH=$(cat $config_file | grep -w releng_branch | awk 'END {print $NF}')
RELENG_COMMIT=$(cat $config_file | grep -w releng_commit | awk 'END {print $NF}')
VIMS_BRANCH=$(cat $config_file | grep -w vims_test_branch | awk 'END {print $NF}')
VIMS_COMMIT=$(cat $config_file | grep -w vims_test_commit | awk 'END {print $NF}')
BGPVPN_BRANCH=$(cat $config_file | grep -w bgpvpn_branch | awk 'END {print $NF}')
BGPVPN_COMMIT=$(cat $config_file | grep -w bgpvpn_commit | awk 'END {print $NF}')


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
echo "FUNCTEST_BRANCH=${FUNCTEST_BRANCH}"
echo "FUNCTEST_COMMIT=${FUNCTEST_COMMIT}"
echo "RELENG_BRANCH=${RELENG_BRANCH}"
echo "RELENG_COMMIT=${RELENG_COMMIT}"
echo "RALLY_BRANCH=${RALLY_BRANCH}"
echo "RALLY_COMMIT=${RALLY_COMMIT}"
echo "VIMS_BRANCH=${VIMS_BRANCH}"
echo "VIMS_COMMIT=${VIMS_COMMIT}"
echo "############################"

info ()  {
    logger -s -t "FUNCTEST.info" "$*"
}


error () {
    logger -s -t "FUNCTEST.error" "$*"
    exit 1
}
