# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import functest.utils.functest_utils as ft_utils
from functest.core.pytest_suite_runner import PyTestSuiteRunner
from functest.opnfv_tests.openstack.snaps import snaps_utils
from snaps import test_suite_builder
import unittest
import os


class SnapsSmoke(PyTestSuiteRunner):
    """
    This test executes the Python Tests included with the SNAPS libraries
    that exercise many of the OpenStack APIs within Keystone, Glance, Neutron,
    and Nova
    """
    def __init__(self):
        super(SnapsSmoke, self).__init__()

        self.suite = unittest.TestSuite()
        self.case_name = "snaps_smoke"
        creds_file = ft_utils.get_functest_config('general.openstack.creds')
        use_key = ft_utils.get_functest_config('snaps.use_keystone')
        use_fip = ft_utils.get_functest_config('snaps.use_floating_ips')
        ext_net_name = snaps_utils.get_ext_net_name()

        # Tests requiring floating IPs leverage files contained within the
        # SNAPS repository and are found relative to that path
        if use_fip:
            snaps_dir = ft_utils.get_functest_config(
                'general.dir.dir_repo_snaps') + '/snaps'
            os.chdir(snaps_dir)

        test_suite_builder.add_openstack_integration_tests(
            self.suite, creds_file, ext_net_name, use_keystone=use_key,
            use_floating_ips=use_fip)
