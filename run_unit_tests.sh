#!/bin/bash
set -o errexit
set -o pipefail

# ******************************
# prepare the env for the tests
# ******************************
# clean useless results dir
# should be done at the end
# but in case of crash during unit test
# clean it anyway
if [ -d "/home/opnfv/functest/results" ]
then
    sudo rm -rf /home/opnfv/functest
fi

# TODO clean that...
# Create log dir if needed
# log shall be disabled during unit tests
# fix to be done in Logger
echo "Create dummy log file...."
sudo mkdir -p /home/opnfv/functest/results/odl
sudo touch /home/opnfv/functest/results/functest.log
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
easy_install -U setuptools
easy_install -U pip
pip install -r $WORKSPACE/docker/requirements.pip
pip install -e $WORKSPACE

python $WORKSPACE/setup.py develop

export CONFIG_FUNCTEST_YAML=$(pwd)/functest/ci/config_functest.yaml
# unit tests
# TODO: remove cover-erase
# To be deleted when all functest packages will be listed
nosetests --with-xunit \
         --with-coverage \
         --cover-erase \
         --cover-package=functest.core.TestCasesBase \
         --cover-package=functest.opnfv_tests.Controllers.ODL.OpenDaylightTesting \
         --cover-xml \
         --cover-html \
         functest/tests/unit
rc=$?

deactivate

# *******
# clean
# *******
# Clean useless logs
if [ -d "/home/opnfv/functest/results" ]
then
    sudo rm -rf /home/opnfv/functest/results
fi

exit $rc
