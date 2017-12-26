# Copyright (c) 2017 Cable Television Laboratories, Inc. and others.
#
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import logging

from functest.core import unit
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.utils.constants import CONST

from snaps.openstack import create_flavor
from snaps.openstack.tests import openstack_tests


class SnapsTestRunner(unit.Suite):
    """
    This test executes the SNAPS Python Tests
    """
    def __init__(self, **kwargs):
        super(SnapsTestRunner, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)

        if 'os_creds' in kwargs:
            self.os_creds = kwargs['os_creds']
        else:
            creds_override = None
            if hasattr(CONST, 'snaps_os_creds_override'):
                creds_override = CONST.__getattribute__(
                    'snaps_os_creds_override')
            self.os_creds = openstack_tests.get_credentials(
                os_env_file=CONST.__getattribute__('openstack_creds'),
                proxy_settings_str=None, ssh_proxy_cmd=None,
                overrides=creds_override)

        if 'ext_net_name' in kwargs:
            self.ext_net_name = kwargs['ext_net_name']
        else:
            self.ext_net_name = snaps_utils.get_ext_net_name(self.os_creds)

        self.network_config = None
        if hasattr(CONST, 'snaps_network_config'):
            self.network_config = CONST.__getattribute__(
                'snaps_network_config')

        self.use_fip = (
            CONST.__getattribute__('snaps_use_floating_ips') == 'True')
        self.use_keystone = (
            CONST.__getattribute__('snaps_use_keystone') == 'True')
        scenario = CONST.__getattribute__('DEPLOY_SCENARIO')

        self.flavor_metadata = None
        if 'ovs' in scenario or 'fdio' in scenario:
            self.flavor_metadata = create_flavor.MEM_PAGE_SIZE_LARGE

        self.logger.info("Using flavor metadata '%s'", self.flavor_metadata)

        self.image_metadata = None
        if hasattr(CONST, 'snaps_images'):
            self.image_metadata = CONST.__getattribute__('snaps_images')
