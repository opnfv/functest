#!/bin/bash
set -o errexit
set -o pipefail

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
         --log-config=$(pwd)/functest/tests/unit/test_logging.ini \
         functest/tests/unit
rc=$?

deactivate

exit $rc
