#!/bin/bash
set -o errexit
set -o pipefail

# date +"%T"
echo "Running unit tests..."
cd .

# Set some en variables if not already set
if [ -z "$CONFIG_FUNCTEST_YAML" ]; then
    echo "set CONFIG_FUNCTEST_YAML (not found in env variables)"
    export CONFIG_FUNCTEST_YAML="./ci/config_functest.yaml"
fi 

if [ -z "$repos_dir" ]; then
    echo "set repos_dir (not found in env variables)"
    export repos_dir=".."
fi 

# start vitual env
virtualenv ./functest_venv
source ./functest_venv/bin/activate

# install python packages
easy_install -U setuptools
easy_install -U pip
pip install -r docker/requirements.pip
pip install -e .

# unit tests
nosetests --with-xunit \
         --with-coverage \
         --cover-package=functest\
         --cover-xml \
         tests
         
deactivate
# date +"%T"
