#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Ease deploying tenant networks

It offers a simple way to create all tenant network ressources required by a
testcase (including all Functest ones):
  - TenantNetwork1 selects the user and the project set as env vars
  - TenantNetwork2 creates a user and project to isolate the same ressources

This classes could be reused by more complexed scenarios (Single VM)
"""

import logging
import os
import time
import uuid

import os_client_config
import shade
from xtesting.core import testcase

from functest.utils import config
from functest.utils import env


class NewProject(object):
    """Ease creating new projects/users"""
    # pylint: disable=too-many-instance-attributes

    __logger = logging.getLogger(__name__)

    def __init__(self, cloud, case_name, guid):
        self.cloud = None
        self.orig_cloud = cloud
        self.case_name = case_name
        self.guid = guid
        self.project = None
        self.user = None
        self.password = None
        self.domain = None

    def create(self):
        """Create projects/users"""
        assert self.orig_cloud
        assert self.case_name
        self.password = str(uuid.uuid4())
        self.domain = self.orig_cloud.get_domain(
            name_or_id=self.orig_cloud.auth.get(
                "project_domain_name", "Default"))
        self.project = self.orig_cloud.create_project(
            name='{}-project_{}'.format(self.case_name, self.guid),
            description="Created by OPNFV Functest: {}".format(
                self.case_name),
            domain_id=self.domain.id)
        self.__logger.debug("project: %s", self.project)
        self.user = self.orig_cloud.create_user(
            name='{}-user_{}'.format(self.case_name, self.guid),
            password=self.password,
            domain_id=self.domain.id)
        self.__logger.debug("user: %s", self.user)
        self.orig_cloud.grant_role(
            "Member", user=self.user.id, project=self.project.id,
            domain=self.domain.id)
        osconfig = os_client_config.config.OpenStackConfig()
        osconfig.cloud_config[
            'clouds']['envvars']['project_name'] = self.project.name
        osconfig.cloud_config['clouds']['envvars']['username'] = self.user.name
        osconfig.cloud_config['clouds']['envvars']['password'] = self.password
        self.__logger.debug("cloud_config %s", osconfig.cloud_config)
        self.cloud = shade.OpenStackCloud(
            cloud_config=osconfig.get_one_cloud())
        self.__logger.debug("new cloud %s", self.cloud.auth)

    def clean(self):
        """Remove projects/users"""
        try:
            assert self.orig_cloud
            assert self.user.id
            assert self.project.id
            self.orig_cloud.delete_user(self.user.id)
            self.orig_cloud.delete_project(self.project.id)
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot clean all ressources")


class TenantNetwork1(testcase.TestCase):
    # pylint: disable=too-many-instance-attributes
    """Create a tenant network (scenario1)

    It creates and configures all tenant network ressources required by
    advanced testcases (subnet, network and router).

    It ensures that all testcases inheriting from TenantNetwork1 could work
    without network specific configurations (or at least read the same config
    data).
    """

    __logger = logging.getLogger(__name__)
    cidr = '192.168.0.0/24'
    shared_network = False

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tenantnetwork1'
        super(TenantNetwork1, self).__init__(**kwargs)
        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), self.case_name)
        try:
            self.cloud = shade.OperatorCloud(
                cloud_config=os_client_config.get_config())
        except Exception:  # pylint: disable=broad-except
            self.cloud = None
            self.ext_net = None
            self.__logger.exception("Cannot connect to Cloud")
        try:
            self.ext_net = self.get_external_network(self.cloud)
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot get the external network")
        self.guid = str(uuid.uuid4())
        self.network = None
        self.subnet = None
        self.router = None

    @staticmethod
    def get_external_network(cloud):
        """
        Returns the configured external network name or
        the first retrieved external network name
        """
        assert cloud
        if env.get("EXTERNAL_NETWORK"):
            network = cloud.get_network(
                env.get("EXTERNAL_NETWORK"), {"router:external": True})
            if network:
                return network
        networks = cloud.list_networks({"router:external": True})
        if networks:
            return networks[0]
        return None

    def _create_network_ressources(self):
        assert self.cloud
        assert self.ext_net
        provider = {}
        if hasattr(config.CONF, '{}_network_type'.format(self.case_name)):
            provider["network_type"] = getattr(
                config.CONF, '{}_network_type'.format(self.case_name))
        if hasattr(config.CONF, '{}_physical_network'.format(self.case_name)):
            provider["physical_network"] = getattr(
                config.CONF, '{}_physical_network'.format(self.case_name))
        if hasattr(config.CONF, '{}_segmentation_id'.format(self.case_name)):
            provider["segmentation_id"] = getattr(
                config.CONF, '{}_segmentation_id'.format(self.case_name))
        self.network = self.cloud.create_network(
            '{}-net_{}'.format(self.case_name, self.guid),
            provider=provider,
            shared=self.shared_network)
        self.__logger.debug("network: %s", self.network)

        self.subnet = self.cloud.create_subnet(
            self.network.id,
            subnet_name='{}-subnet_{}'.format(self.case_name, self.guid),
            cidr=getattr(
                config.CONF, '{}_private_subnet_cidr'.format(self.case_name),
                self.cidr),
            enable_dhcp=True,
            dns_nameservers=[env.get('NAMESERVER')])
        self.__logger.debug("subnet: %s", self.subnet)

        self.router = self.cloud.create_router(
            name='{}-router_{}'.format(self.case_name, self.guid),
            ext_gateway_net_id=self.ext_net.id)
        self.__logger.debug("router: %s", self.router)
        self.cloud.add_router_interface(self.router, subnet_id=self.subnet.id)

    def run(self, **kwargs):
        status = testcase.TestCase.EX_RUN_ERROR
        try:
            assert self.cloud
            self.start_time = time.time()
            self._create_network_ressources()
            self.result = 100
            status = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception('Cannot run %s', self.case_name)
        finally:
            self.stop_time = time.time()
        return status

    def clean(self):
        try:
            assert self.cloud
            self.cloud.remove_router_interface(self.router, self.subnet.id)
            self.cloud.delete_router(self.router.id)
            self.cloud.delete_subnet(self.subnet.id)
            self.cloud.delete_network(self.network.id)
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("cannot clean all ressources")


class TenantNetwork2(TenantNetwork1):
    """Create a tenant network (scenario2)

    It creates new user/project before creating and configuring all tenant
    network ressources required by a testcase (subnet, network and router).

    It ensures that all testcases inheriting from TenantNetwork2 could work
    without network specific configurations (or at least read the same config
    data).
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tenantnetwork2'
        super(TenantNetwork2, self).__init__(**kwargs)
        try:
            assert self.cloud
            self.project = NewProject(
                self.cloud, self.case_name, self.guid)
            self.project.create()
            self.cloud = self.project.cloud
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot create user or project")
            self.cloud = None
            self.project = None

    def clean(self):
        try:
            super(TenantNetwork2, self).clean()
            assert self.project
            self.project.clean()
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot clean all ressources")
