# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import unittest

from snaps.openstack.tests.os_source_file_test import OSIntegrationTestCase
from snaps.openstack.tests.create_instance_tests import SimpleHealthCheck

from functest.core.pytest_suite_runner import PyTestSuiteRunner
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.utils.constants import CONST


class HealthCheck(PyTestSuiteRunner):
    """
    This test executes the SNAPS Python Test case SimpleHealthCheck which
    creates a VM with a single port with an IPv4 address that is assigned by
    DHCP. This test then validates the expected IP with the actual
    """
    def __init__(self):
        super(HealthCheck, self).__init__()

        self.suite = unittest.TestSuite()
        self.case_name = "snaps_health_check"
        ext_net_name = snaps_utils.get_ext_net_name()

        image_custom_config = CONST.snaps_simple_healthcheck or None

        self.suite.addTest(
            OSIntegrationTestCase.parameterize(
                SimpleHealthCheck, CONST.openstack_creds, ext_net_name,
                use_keystone=CONST.snaps_use_keystone,
                image_metadata=image_custom_config))
