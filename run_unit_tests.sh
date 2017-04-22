#!/bin/bash
set -o errexit
set -o pipefail

#install releng
rm -rf releng-unittests
git clone --depth 1 https://gerrit.opnfv.org/gerrit/releng releng-unittests
pip install releng-unittests/modules/
rm -fr releng-unittests

export CONFIG_FUNCTEST_YAML=$(pwd)/functest/ci/config_functest.yaml
# unit tests
# TODO: remove cover-erase
# To be deleted when all functest packages will be listed
nosetests --with-xunit \
         --with-coverage \
         --cover-erase \
         --cover-tests \
         --cover-package=functest.ci \
         --cover-package=functest.cli \
         --cover-package=functest.core \
         --cover-package=functest.opnfv_tests.sdn.odl.odl \
         --cover-package=functest.opnfv_tests.vnf.ims \
         --cover-package=functest.utils \
         --cover-package=functest.opnfv_tests.features \
         --cover-package=functest.opnfv_tests.openstack \
         --cover-xml \
         --cover-html \
         --log-config=$(pwd)/functest/tests/unit/test_logging.ini \
         functest/tests/unit
rc=$?

exit $rc
