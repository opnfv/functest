#!/bin/bash
set -o errexit
set -o pipefail

echo "Running unit tests..."

if [ -z $WORKSPACE ]
then
    WORKSPACE="$HOME"
fi

# start vitual env
virtualenv $WORKSPACE/functest_venv
source $WORKSPACE/functest_venv/bin/activate

# install python packages
easy_install -U setuptools
easy_install -U pip
pip install -r docker/requirements.pip
pip install -e .

python ./setup.py develop

echo " ************** "
which nosetests
echo " ************** "
echo $PWD
echo " ************** "
echo " ************** "
echo $PYTHONPATH
echo " ************** "
which python
echo " ************** "



# unit tests
nosetests --with-xunit \
         --with-coverage \
         --cover-package=functest.core.TestCasesBase \
         --cover-package=functest.testcases.Controllers.ODL.OpenDaylightTesting \
         --cover-xml \
         unit_tests
rc=$?

deactivate

exit $rc
