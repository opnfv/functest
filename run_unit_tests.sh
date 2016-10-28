#!/bin/bash
set -o errexit
set -o pipefail

echo "Running unit tests..."

if [ -z $WORKSPACE ]
then
    WORKSPACE="$HOME"
fi

# Create log dir if needed (TODO clean that...)
if [ ! -d "/home/opnfv/functest/results" ]
then
    sudo mkdir -p /home/opnfv/functest/results
fi

if [ ! -d "/home/opnfv/functest/results/odl" ]
then
    sudo mkdir -p /home/opnfv/functest/results/odl
fi

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
sudo rm -rf /home/opnfv/functest/results

exit $rc
