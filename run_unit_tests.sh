#!/bin/bash
set -o errexit
set -o pipefail

nosetests --with-xunit \
         --with-coverage \
         --cover-tests \
         --cover-package=functest \
         --cover-xml \
         --cover-html \
         --log-config=$(pwd)/functest/tests/unit/test_logging.ini \
         functest/tests/unit
rc=$?

exit $rc
