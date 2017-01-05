#!/bin/bash
set -o errexit
set -o pipefail

function clean_results_dir {
    if [ -d "/home/opnfv/functest/results" ]
    then
        sudo rm -rf /home/opnfv/functest/results
    fi
}

# ******************************
# prepare the env for the tests
# ******************************
# clean useless results dir
# should be done at the end
# but in case of crash during unit test
# clean it anyway
clean_results_dir

# TODO clean that...
# Create log dir if needed
# log shall be disabled during unit tests
# fix to be done in Logger
sudo mkdir -p /home/opnfv/functest/results/odl
sudo touch /home/opnfv/functest/results/odl/stdout.txt
sudo chmod -Rf a+rw /home/opnfv

# Either Workspace is set (CI)
if [ -z $WORKSPACE ]
then
    WORKSPACE="."
fi


# ***************
# Run unit tests
# ***************
echo "Running unit tests..."

# start vitual env
virtualenv $WORKSPACE/functest_venv
source $WORKSPACE/functest_venv/bin/activate

# install python packages
sudo apt-get install -y build-essential python-dev python-pip
pip install --upgrade pip
pip install -r $WORKSPACE/test-requirements.txt
pip install $WORKSPACE

export CONFIG_FUNCTEST_YAML=$(pwd)/functest/ci/config_functest.yaml
# unit tests
# TODO: remove cover-erase
# To be deleted when all functest packages will be listed
nosetests --with-xunit \
         --with-coverage \
         --cover-erase \
         --cover-tests \
         --cover-package=functest.cli \
         --cover-package=functest.core.testcase_base \
         --cover-package=functest.opnfv_tests.sdn.odl.odl \
         --cover-package=functest.utils \
         --cover-xml \
         --cover-html \
         functest/tests/unit
rc=$?

deactivate

# *******
# clean
# *******
# Clean useless logs
clean_results_dir

exit $rc
