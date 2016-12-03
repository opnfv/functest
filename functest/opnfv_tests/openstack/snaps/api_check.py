# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import functest.utils.functest_utils as ft_utils
from functest.core.pytest_suite_runner import PyTestSuiteRunner
from snaps import test_suite_builder
import unittest


class ApiCheck(PyTestSuiteRunner):
    """
    This test executes the Python Tests included with the SNAPS libraries
    that exercise many of the OpenStack APIs within Keystone, Glance, Neutron,
    and Nova
    """
    def __init__(self):
        super(ApiCheck, self).__init__()

        self.suite = unittest.TestSuite()
        creds_file = ft_utils.get_functest_config('general.openstack.creds')
        ext_net = ft_utils.get_functest_config('snaps.external_network_name')
        use_key = ft_utils.get_functest_config('snaps.use_keystone')

        test_suite_builder.add_openstack_api_tests(self.suite, creds_file,
                                                   ext_net,
                                                   use_keystone=use_key)
