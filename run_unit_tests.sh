#!/bin/bash
set -o errexit
set -o pipefail

# Either Workspace is set (CI)
if [ -z $WORKSPACE ]
then
    WORKSPACE=`pwd`
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

#install releng
rm -rf releng-unittests
git clone --depth 1 https://gerrit.opnfv.org/gerrit/releng releng-unittests
pip install releng-unittests/modules/
rm -fr releng-unittests

export CONFIG_FUNCTEST_YAML=$(pwd)/functest/ci/config_functest.yaml
nosetests --with-xunit \
         --with-coverage \
         --cover-tests \
         --cover-package=functest \
         --cover-xml \
         --cover-html \
         --log-config=$(pwd)/functest/tests/unit/test_logging.ini \
         functest/tests/unit
rc=$?

deactivate

exit $rc
