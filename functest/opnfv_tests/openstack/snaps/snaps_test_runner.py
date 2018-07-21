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

import os_client_config
import shade
from xtesting.core import unit

from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.utils import config
from functest.utils import functest_utils


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
        if hasattr(config.CONF, 'snaps_network_config'):
            self.netconf_override = getattr(
                config.CONF, 'snaps_network_config')

        self.use_fip = (
            getattr(config.CONF, 'snaps_use_floating_ips') == 'True')
        self.use_keystone = (
            getattr(config.CONF, 'snaps_use_keystone') == 'True')

        self.flavor_metadata = getattr(config.CONF, 'snaps_flavor_extra_specs',
                                       None)
        self.logger.info("Using flavor metadata '%s'", self.flavor_metadata)

        self.image_metadata = None
        if hasattr(config.CONF, 'snaps_images'):
            self.image_metadata = getattr(config.CONF, 'snaps_images')

    def check_requirements(self):
        """Skip if OpenStack Rocky or newer."""
        try:
            cloud_config = os_client_config.get_config()
            cloud = shade.OpenStackCloud(cloud_config=cloud_config)
            if functest_utils.get_nova_version(cloud) > (2, 60):
                self.is_skipped = True
        except Exception:  # pylint: disable=broad-except
            pass
