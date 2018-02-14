#!/usr/bin/env python

# Copyright (c) 2017 Cable Television Laboratories, Inc. and others.
#
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""configuration params to run snaps tests"""

import logging

from functest.core import unit
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.utils.constants import CONST
from functest.utils import env

from snaps.openstack import create_flavor


class SnapsTestRunner(unit.Suite):
    # pylint: disable=too-many-instance-attributes
    """
    This test executes the SNAPS Python Tests
    """

    def __init__(self, **kwargs):
        super(SnapsTestRunner, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.os_creds = kwargs.get('os_creds') or snaps_utils.get_credentials()

        if 'ext_net_name' in kwargs:
            self.ext_net_name = kwargs['ext_net_name']
        else:
            self.ext_net_name = snaps_utils.get_ext_net_name(self.os_creds)

        self.netconf_override = None
        if hasattr(CONST, 'snaps_network_config'):
            self.netconf_override = CONST.__getattribute__(
                'snaps_network_config')

        self.use_fip = (
            CONST.__getattribute__('snaps_use_floating_ips') == 'True')
        self.use_keystone = (
            CONST.__getattribute__('snaps_use_keystone') == 'True')
        scenario = env.get('DEPLOY_SCENARIO')

        self.flavor_metadata = None
        if 'ovs' in scenario or 'fdio' in scenario:
            self.flavor_metadata = create_flavor.MEM_PAGE_SIZE_LARGE

        self.logger.info("Using flavor metadata '%s'", self.flavor_metadata)

        self.image_metadata = None
        if hasattr(CONST, 'snaps_images'):
            self.image_metadata = CONST.__getattribute__('snaps_images')
