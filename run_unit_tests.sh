#!/bin/bash
set -o errexit
set -o pipefail

#install releng
rm -rf releng-unittests
git clone --depth 1 https://gerrit.opnfv.org/gerrit/releng releng-unittests
pip install releng-unittests/modules/
rm -rf releng-unittests

#install barometer
rm -rf barometer-unittests
git clone --depth 1 https://gerrit.opnfv.org/gerrit/barometer barometer-unittests
(cd barometer-unittests; python setup.py install)
rm -rf barometer-unittests

nosetests --with-xunit \
         --with-coverage \
         --cover-tests \
         --cover-package=functest \
         --cover-xml \
         --cover-html \
         --log-config=$(pwd)/functest/tests/unit/test_logging.ini \
         functest/tests/unit

exit $?
