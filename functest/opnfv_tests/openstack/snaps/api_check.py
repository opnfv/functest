# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import unittest

from snaps import test_suite_builder

from functest.opnfv_tests.openstack.snaps.snaps_test_runner import \
    SnapsTestRunner
from functest.utils.constants import CONST


class ApiCheck(SnapsTestRunner):
    """
    This test executes the Python Tests included with the SNAPS libraries
    that exercise many of the OpenStack APIs within Keystone, Glance, Neutron,
    and Nova
    """
    def __init__(self, case_name="api_check"):
        super(ApiCheck, self).__init__(case_name)

        self.suite = unittest.TestSuite()

        test_suite_builder.add_openstack_api_tests(
            suite=self.suite,
            os_creds=self.os_creds,
            ext_net_name=self.ext_net_name,
            use_keystone=self.use_keystone)
