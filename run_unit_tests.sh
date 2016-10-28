#!/bin/bash
set -o errexit
set -o pipefail

# clean
if [ -d "/home/opnfv/functest/results" ]
then
    sudo rm -rf /home/opnfv/functest/results
fi

if [ -z $WORKSPACE ]
then
    WORKSPACE="$HOME"
fi

# Create log dir if needed (TODO clean that...)
if [ ! -d "/home/opnfv/functest/results" ]
then
    echo "Create dummy log file...."
    sudo mkdir -p /home/opnfv/functest/results
    sudo chmod -R 766 /home/opnfv
    sudo touch /home/opnfv/functest/results/functest.log
    sudo chmod 766 /home/opnfv/functest/results/functest.log
fi

if [ ! -d "/home/opnfv/functest/results/odl" ]
then
    sudo mkdir -p /home/opnfv/functest/results/odl
fi

echo " ************* "
ls -lah /home/opnfv/functest/results
echo " ************* "

# as we import the module from the home repo
# and in jenkins the name is different
# functest(verify-master != functest
# make some ugly adjustments...
cd $WORKSPACE
export PYTHONPATH="${PYTHONPATH}:$WORKSPACE"
cd ..

if [ ! -d "./functest" ]
then
ln -s functest-verify-master functest
fi

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
         --cover-package=functest.core.TestCasesBase \
         --cover-package=functest.testcases.Controllers.ODL.OpenDaylightTesting \
         --cover-xml \
         unit_tests
rc=$?

deactivate

# clean
if [ -d "/home/opnfv/functest/results" ]
then
    sudo rm -rf /home/opnfv/functest/results
fi

exit $rc
