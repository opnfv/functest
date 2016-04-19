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
FUNCTEST_DIR=$(cat $config_file | grep -w dir_functest | awk 'END {print $NF}')
FUNCTEST_RESULTS_DIR=$(cat $config_file | grep -w dir_results | awk 'END {print $NF}')
FUNCTEST_CONF_DIR=$(cat $config_file | grep -w dir_functest_conf | awk 'END {print $NF}')
FUNCTEST_DATA_DIR=$(cat $config_file | grep -w dir_functest_data | awk 'END {print $NF}')
RALLY_VENV_DIR=$(cat $config_file | grep -w dir_rally_inst | awk 'END {print $NF}')


info ()  {
    logger -s -t "FUNCTEST.info" "$*"
}

error () {
    logger -s -t "FUNCTEST.error" "$*"
    exit 1
}
