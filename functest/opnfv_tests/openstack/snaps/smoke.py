# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import os
import unittest

from snaps import test_suite_builder

from functest.opnfv_tests.openstack.snaps.snaps_test_runner import \
    SnapsTestRunner
from functest.utils.constants import CONST


class SnapsSmoke(SnapsTestRunner):
    """
    This test executes the Python Tests included with the SNAPS libraries
    that exercise many of the OpenStack APIs within Keystone, Glance, Neutron,
    and Nova
    """
    def __init__(self, case_name="snaps_smoke"):
        super(SnapsSmoke, self).__init__(case_name)

        self.suite = unittest.TestSuite()
        use_fip = CONST.snaps_use_floating_ips

        # The snaps smoke test uses the same config as the
        # snaps_health_check suite, so reuse it here
        image_custom_config = None
        if hasattr(CONST, 'snaps_health_check'):
            image_custom_config = CONST.snaps_health_check

        # Tests requiring floating IPs leverage files contained within the
        # SNAPS repository and are found relative to that path
        if self.use_fip:
            snaps_dir = CONST.dir_repo_snaps + '/snaps'
            os.chdir(snaps_dir)

        test_suite_builder.add_openstack_integration_tests(
            suite=self.suite,
            os_creds=self.os_creds,
            ext_net_name=self.ext_net_name,
            use_keystone=self.use_keystone,
            flavor_metadata=self.flavor_metadata,
            image_metadata=image_custom_config,
            use_floating_ips=self.use_fip)
