# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import unittest

from functest.opnfv_tests.openstack.snaps.snaps_test_runner import \
    SnapsTestRunner
from functest.utils.constants import CONST

from snaps.openstack.tests.os_source_file_test import OSIntegrationTestCase
from snaps.openstack.tests.create_instance_tests import SimpleHealthCheck


class HealthCheck(SnapsTestRunner):
    """
    This test executes the SNAPS Python Test case SimpleHealthCheck which
    creates a VM with a single port with an IPv4 address that is assigned by
    DHCP. This test then validates the expected IP with the actual
    """
    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "snaps_health_check"
        super(HealthCheck, self).__init__(**kwargs)

        self.suite = unittest.TestSuite()

        image_custom_config = None
        if hasattr(CONST, 'snaps_health_check'):
            image_custom_config = CONST.__getattribute__('snaps_health_check')
        self.suite.addTest(
            OSIntegrationTestCase.parameterize(
                SimpleHealthCheck, os_creds=self.os_creds,
                ext_net_name=self.ext_net_name,
                use_keystone=self.use_keystone,
                flavor_metadata=self.flavor_metadata,
                image_metadata=image_custom_config))
