#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Ease deploying tenant networks

It offers a simple way to create all tenant network resources required by a
testcase (including all Functest ones):

  - TenantNetwork1 selects the user and the project set as env vars
  - TenantNetwork2 creates a user and project to isolate the same resources

This classes could be reused by more complexed scenarios (Single VM)
"""

import logging
import os
import time
import uuid

import os_client_config
import shade
from tempest.lib.common.utils import data_utils
from xtesting.core import testcase

from functest.utils import config
from functest.utils import env
from functest.utils import functest_utils


class NewProject():
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
        self.role_name = None
        self.default_member = env.get('NEW_USER_ROLE')

    def create(self):
        """Create projects/users"""
        assert self.orig_cloud
        assert self.case_name
        self.password = data_utils.rand_password().replace('%', '!')
        self.__logger.debug("password: %s", self.password)
        self.domain = self.orig_cloud.get_domain(
            name_or_id=self.orig_cloud.auth.get(
                "project_domain_name", "Default"))
        self.project = self.orig_cloud.create_project(
            name=f'{self.case_name[:18]}-project_{self.guid}',
            description=f"Created by OPNFV Functest: {self.case_name}",
            domain_id=self.domain.id)
        self.__logger.debug("project: %s", self.project)
        self.user = self.orig_cloud.create_user(
            name=f'{self.case_name}-user_{self.guid}',
            password=self.password,
            domain_id=self.domain.id)
        self.__logger.debug("user: %s", self.user)
        try:
            if self.orig_cloud.get_role(self.default_member):
                self.role_name = self.default_member
            elif self.orig_cloud.get_role(self.default_member.lower()):
                self.role_name = self.default_member.lower()
            else:
                raise Exception(f"Cannot detect {self.default_member}")
        except Exception:  # pylint: disable=broad-except
            self.__logger.info("Creating default role %s", self.default_member)
            role = self.orig_cloud.create_role(self.default_member)
            self.role_name = role.name
            self.__logger.debug("role: %s", role)
        self.orig_cloud.grant_role(
            self.role_name, user=self.user.id, project=self.project.id,
            domain=self.domain.id)
        osconfig = os_client_config.config.OpenStackConfig()
        osconfig.cloud_config[
            'clouds']['envvars']['project_name'] = self.project.name
        osconfig.cloud_config[
            'clouds']['envvars']['project_id'] = self.project.id
        osconfig.cloud_config['clouds']['envvars']['username'] = self.user.name
        osconfig.cloud_config['clouds']['envvars']['password'] = self.password
        self.__logger.debug("cloud_config %s", osconfig.cloud_config)
        self.cloud = shade.OpenStackCloud(
            cloud_config=osconfig.get_one_cloud())
        self.__logger.debug("new cloud %s", self.cloud.auth)

    def get_environ(self):
        "Get new environ"
        environ = dict(
            os.environ,
            OS_USERNAME=self.user.name,
            OS_PROJECT_NAME=self.project.name,
            OS_PROJECT_ID=self.project.id,
            OS_PASSWORD=self.password)
        try:
            del environ['OS_TENANT_NAME']
            del environ['OS_TENANT_ID']
        except Exception:  # pylint: disable=broad-except
            pass
        return environ

    def clean(self):
        """Remove projects/users"""
        try:
            assert self.orig_cloud
            if self.user:
                self.orig_cloud.delete_user(self.user.id)
            if self.project:
                self.orig_cloud.delete_project(self.project.id)
            secgroups = self.orig_cloud.list_security_groups(
                filters={'name': 'default',
                         'project_id': self.project.id})
            if secgroups:
                sec_id = secgroups[0].id
                self.orig_cloud.delete_security_group(sec_id)
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot clean all resources")


class TenantNetwork1(testcase.TestCase):
    # pylint: disable=too-many-instance-attributes
    """Create a tenant network (scenario1)

    It creates and configures all tenant network resources required by
    advanced testcases (subnet, network and router).

    It ensures that all testcases inheriting from TenantNetwork1 could work
    without network specific configurations (or at least read the same config
    data).
    """

    __logger = logging.getLogger(__name__)
    cidr = '192.168.120.0/24'
    shared_network = False

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tenantnetwork1'
        super().__init__(**kwargs)
        self.dir_results = os.path.join(getattr(config.CONF, 'dir_results'))
        self.res_dir = os.path.join(self.dir_results, self.case_name)
        self.output_log_name = 'functest.log'
        self.output_debug_log_name = 'functest.debug.log'
        self.ext_net = None
        try:
            cloud_config = os_client_config.get_config()
            self.cloud = self.orig_cloud = shade.OpenStackCloud(
                cloud_config=cloud_config)
        except Exception:  # pylint: disable=broad-except
            self.cloud = self.orig_cloud = None
            self.__logger.exception("Cannot connect to Cloud")
        if env.get('NO_TENANT_NETWORK').lower() != 'true':
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
        Return the configured external network name or
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

    @staticmethod
    def get_default_role(cloud, member="Member"):
        """Get the default role

        It also tests the role in lowercase to avoid possible conflicts.
        """
        role = cloud.get_role(member)
        if not role:
            role = cloud.get_role(member.lower())
        return role

    @staticmethod
    def get_public_auth_url(cloud):
        """Get Keystone public endpoint"""
        keystone_id = functest_utils.search_services(cloud, 'keystone')[0].id
        endpoint = cloud.search_endpoints(
            filters={'interface': 'public',
                     'service_id': keystone_id})[0].url
        return endpoint

    def create_network_resources(self):
        """Create all tenant network resources

        It creates a router which gateway is the external network detected.
        The new subnet is attached to that router.

        Raises: expection on error
        """
        assert self.cloud
        if env.get('NO_TENANT_NETWORK').lower() != 'true':
            assert self.ext_net
        provider = {}
        if hasattr(config.CONF, f'{self.case_name}_network_type'):
            provider["network_type"] = getattr(
                config.CONF, f'{self.case_name}_network_type')
        if hasattr(config.CONF, f'{self.case_name}_physical_network'):
            provider["physical_network"] = getattr(
                config.CONF, f'{self.case_name}_physical_network')
        if hasattr(config.CONF, f'{self.case_name}_segmentation_id'):
            provider["segmentation_id"] = getattr(
                config.CONF, f'{self.case_name}_segmentation_id')
        domain = self.orig_cloud.get_domain(
            name_or_id=self.orig_cloud.auth.get(
                "project_domain_name", "Default"))
        project = self.orig_cloud.get_project(
            self.cloud.auth['project_name'],
            domain_id=domain.id)
        self.network = self.orig_cloud.create_network(
            f'{self.case_name}-net_{self.guid}',
            provider=provider, project_id=project.id,
            shared=self.shared_network)
        self.__logger.debug("network: %s", self.network)

        self.subnet = self.cloud.create_subnet(
            self.network.id,
            subnet_name=f'{self.case_name}-subnet_{self.guid}',
            cidr=getattr(
                config.CONF, f'{self.case_name}_private_subnet_cidr',
                self.cidr),
            enable_dhcp=True,
            dns_nameservers=[env.get('NAMESERVER')])
        self.__logger.debug("subnet: %s", self.subnet)

        self.router = self.cloud.create_router(
            name=f'{self.case_name}-router_{self.guid}',
            ext_gateway_net_id=self.ext_net.id if self.ext_net else None)
        self.__logger.debug("router: %s", self.router)
        self.cloud.add_router_interface(self.router, subnet_id=self.subnet.id)

    def run(self, **kwargs):
        status = testcase.TestCase.EX_RUN_ERROR
        try:
            assert self.cloud
            self.start_time = time.time()
            if env.get('NO_TENANT_NETWORK').lower() != 'true':
                self.create_network_resources()
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
            if self.router:
                if self.subnet:
                    self.cloud.remove_router_interface(
                        self.router, self.subnet.id)
                self.cloud.delete_router(self.router.id)
            if self.subnet:
                self.cloud.delete_subnet(self.subnet.id)
            if self.network:
                self.cloud.delete_network(self.network.id)
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("cannot clean all resources")


class TenantNetwork2(TenantNetwork1):
    """Create a tenant network (scenario2)

    It creates new user/project before creating and configuring all tenant
    network resources required by a testcase (subnet, network and router).

    It ensures that all testcases inheriting from TenantNetwork2 could work
    without network specific configurations (or at least read the same config
    data).
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tenantnetwork2'
        super().__init__(**kwargs)
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
            super().clean()
            assert self.project
            self.project.clean()
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot clean all resources")
