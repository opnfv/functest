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

# Create log dir if needed
# TODO clean that...
# log shall be disabled during unit tests
# fix to be done in Logger
if [ ! -d "/home/opnfv/functest/results" ]
then
    echo "Create dummy log file...."
    sudo mkdir -p /home/opnfv/functest/results/odl
    sudo touch /home/opnfv/functest/results/functest.log
    sudo touch /home/opnfv/functest/results/odl/stdout.txt
    sudo chmod -Rf a+rw /home/opnfv
fi

# Either Workspace is set (CI)
# then useless log files must belong to jenkins:jenkins
# or it is local tests and we do not care
if [ -z $WORKSPACE ]
then
    WORKSPACE="."
else
    sudo chown -Rf jenkins:jenkins /home/opnfv
    # as we import the module from the home repo
    # and in jenkins the name is different
    # functest-verify-master != functest
    # make some ugly adjustments...
    cd $WORKSPACE
    export PYTHONPATH="${PYTHONPATH}:$WORKSPACE"
    cd ..

    if [ ! -d "./functest" ]
    then
    ln -s functest-verify-master functest
    fi
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

# unit tests
nosetests --with-xunit \
         --with-coverage \
         --cover-erase \
         --cover-package=functest.core.TestCasesBase \
         --cover-package=functest.testcases.Controllers.ODL.OpenDaylightTesting \
         --cover-xml \
         --cover-html \
         unit_tests
rc=$?

deactivate

# *******
# clean
# *******
# First as we had to start the test from ..
# Push the results upstream for jenkins
if [ $WORKSPACE != "." ]
then
    mv coverage.xml nosetests.xml $WORKSPACE
fi

# Clean useless logs
if [ -d "/home/opnfv/functest/results" ]
then
    sudo rm -rf /home/opnfv/functest/results
fi

exit $rc
