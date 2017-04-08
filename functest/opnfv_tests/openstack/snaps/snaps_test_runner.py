# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

from functest.utils import functest_logger as ft_logger
from functest.core.pytest_suite_runner import PyTestSuiteRunner
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.utils import functest_utils

from snaps.openstack import create_flavor


class SnapsTestRunner(PyTestSuiteRunner):
    """
    This test executes the SNAPS Python Test case SimpleHealthCheck which
    creates a VM with a single port with an IPv4 address that is assigned by
    DHCP. This test then validates the expected IP with the actual
    """
    def __init__(self, **kwargs):
        super(SnapsTestRunner, self).__init__(**kwargs)

        self.ext_net_name = snaps_utils.get_ext_net_name()
        self.logger = ft_logger.Logger(self.project_name).getLogger()
        scenario = functest_utils.get_scenario()

        self.flavor_metadata = create_flavor.MEM_PAGE_SIZE_ANY
        if 'ovs' in scenario or 'fdio' in scenario:
            self.flavor_metadata = create_flavor.MEM_PAGE_SIZE_LARGE

        self.logger.info("Using flavor metatdata '%s'" % self.flavor_metadata)
