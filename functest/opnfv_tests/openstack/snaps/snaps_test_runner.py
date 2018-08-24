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
import uuid

import os_client_config
import shade
from xtesting.core import unit

from functest.core import tenantnetwork
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

        try:
            cloud_config = os_client_config.get_config()
            self.orig_cloud = shade.OpenStackCloud(cloud_config=cloud_config)
            guid = str(uuid.uuid4())
            self.project = tenantnetwork.NewProject(
                self.orig_cloud, self.case_name, guid)
            self.project.create()
        except Exception:  # pylint: disable=broad-except
            raise Exception("Cannot create user or project")

        if self.orig_cloud.get_role("admin"):
            role_name = "admin"
        elif self.orig_cloud.get_role("Admin"):
            role_name = "Admin"
        else:
            raise Exception("Cannot detect neither admin nor Admin")
        self.orig_cloud.grant_role(
            role_name, user=self.project.user.id,
            project=self.project.project.id,
            domain=self.project.domain.id)
        self.role = None
        if not self.orig_cloud.get_role("heat_stack_owner"):
            self.role = self.orig_cloud.create_role("heat_stack_owner")
        self.orig_cloud.grant_role(
            "heat_stack_owner", user=self.project.user.id,
            project=self.project.project.id,
            domain=self.project.domain.id)
        creds_overrides = dict(
            username=self.project.user.name,
            project_name=self.project.project.name,
            project_id=self.project.project.id,
            password=self.project.password)
        self.os_creds = kwargs.get('os_creds') or \
            snaps_utils.get_credentials(overrides=creds_overrides)
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

    def clean(self):
        """Cleanup of OpenStack resources. Should be called on completion."""
        try:
            super(SnapsTestRunner, self).clean()
            assert self.orig_cloud
            assert self.project
            if self.role:
                self.orig_cloud.delete_role(self.role.id)
            self.project.clean()
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot clean all resources")

    def check_requirements(self):
        """Skip if OpenStack Rocky or newer."""
        try:
            cloud_config = os_client_config.get_config()
            cloud = shade.OpenStackCloud(cloud_config=cloud_config)
            if functest_utils.get_nova_version(cloud) > (2, 60):
                self.is_skipped = True
        except Exception:  # pylint: disable=broad-except
            pass
