#!/bin/bash
set -o errexit
set -o pipefail

echo "Running unit tests..."
cd .

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
         --cover-package=functest.core.TestCasesBase \
         --cover-package=functest.testcases.Controllers.ODL.OpenDaylightTesting \
         --cover-xml \
         unit_tests

deactivate
rc=$?

exit $rc
