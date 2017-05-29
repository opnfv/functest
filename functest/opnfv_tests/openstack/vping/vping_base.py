#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

from datetime import datetime
import logging
import os
import time
import uuid

from functest.core import testcase
from functest.utils import functest_utils
from functest.utils.constants import CONST

from snaps.openstack import create_flavor
from snaps.openstack.create_flavor import FlavorSettings, OpenStackFlavor
from snaps.openstack.create_network import NetworkSettings, SubnetSettings
from snaps.openstack.tests import openstack_tests
from snaps.openstack.utils import deploy_utils, nova_utils


class VPingBase(testcase.OSGCTestCase):

    """
    Base class for vPing tests that check connectivity between two VMs shared
    internal network.
    This class is responsible for creating the image, internal network.
    """

    def __init__(self, **kwargs):
        super(VPingBase, self).__init__(**kwargs)

        self.logger = logging.getLogger(self.__class__.__name__)

        self.functest_repo = CONST.__getattribute__('dir_repo_functest')
        self.guid = ''
        if CONST.__getattribute__('vping_unique_names'):
            self.guid = '-' + str(uuid.uuid4())

        self.os_creds = openstack_tests.get_credentials(
            os_env_file=CONST.__getattribute__('openstack_creds'))

        self.repo = CONST.__getattribute__('dir_vping')

        self.creators = list()
        self.image_creator = None
        self.network_creator = None
        self.vm1_creator = None
        self.vm2_creator = None

        self.self_cleanup = CONST.__getattribute__('vping_cleanup_objects')

        # Image constants
        self.image_name =\
            CONST.__getattribute__('vping_image_name') + self.guid

        # VM constants
        self.vm1_name = CONST.__getattribute__('vping_vm_name_1') + self.guid
        self.vm2_name = CONST.__getattribute__('vping_vm_name_2') + self.guid
        self.vm_boot_timeout = CONST.__getattribute__('vping_vm_boot_timeout')
        self.vm_delete_timeout =\
            CONST.__getattribute__('vping_vm_delete_timeout')
        self.vm_ssh_connect_timeout = CONST.vping_vm_ssh_connect_timeout
        self.ping_timeout = CONST.__getattribute__('vping_ping_timeout')
        self.flavor_name = 'vping-flavor' + self.guid

        # NEUTRON Private Network parameters
        self.private_net_name =\
            CONST.__getattribute__('vping_private_net_name') + self.guid
        self.private_subnet_name =\
            CONST.__getattribute__('vping_private_subnet_name') + self.guid
        self.private_subnet_cidr =\
            CONST.__getattribute__('vping_private_subnet_cidr')

        scenario = functest_utils.get_scenario()

        self.flavor_metadata = create_flavor.MEM_PAGE_SIZE_ANY
        if 'ovs' in scenario or 'fdio' in scenario:
            self.flavor_metadata = create_flavor.MEM_PAGE_SIZE_LARGE

        self.cirros_image_config = None

        # Move this configuration option up for all tests to leverage
        if hasattr(CONST, 'snaps_images_cirros'):
            self.cirros_image_config = CONST.__getattribute__(
                'snaps_images_cirros')

    def run(self):
        """
        Begins the test execution which should originate from the subclass
        """

        if not os.path.exists(self.functest_repo):
            raise Exception(
                "Functest repository not found '%s'" % self.functest_repo)

        self.logger.info('Begin virtual environment setup')

        self.start_time = time.time()
        self.logger.info("vPing Start Time:'%s'" % (
            datetime.fromtimestamp(self.start_time).strftime(
                '%Y-%m-%d %H:%M:%S')))

        self.__delete_exist_vms()

        image_base_name = self.image_name + '-' + str(self.guid)
        os_image_settings = openstack_tests.cirros_image_settings(
            image_base_name, image_metadata=self.cirros_image_config)
        self.logger.info("Creating image with name: '%s'" % self.image_name)

        self.image_creator = deploy_utils.create_image(
            self.os_creds, os_image_settings)
        self.creators.append(self.image_creator)

        self.logger.info(
            "Creating network with name: '%s'" % self.private_net_name)
        self.network_creator = deploy_utils.create_network(
            self.os_creds,
            NetworkSettings(name=self.private_net_name,
                            subnet_settings=[SubnetSettings(
                                name=self.private_subnet_name,
                                cidr=self.private_subnet_cidr)]))
        self.creators.append(self.network_creator)

        self.logger.info(
            "Creating flavor with name: '%s'" % self.flavor_name)
        flavor_creator = OpenStackFlavor(
            self.os_creds,
            FlavorSettings(name=self.flavor_name, ram=512, disk=1, vcpus=1,
                           metadata=self.flavor_metadata))
        flavor_creator.create()
        self.creators.append(flavor_creator)

    def _execute(self):
        """
        Method called by subclasses after environment has been setup
        :return: the exit code
        """
        self.logger.info('Begin test execution')

        test_ip = self.vm1_creator.get_port_ip(
            self.vm1_creator.instance_settings.port_settings[0].name)

        if self.vm1_creator.vm_active(
                block=True) and self.vm2_creator.vm_active(block=True):
            result = self._do_vping(self.vm2_creator, test_ip)
        else:
            raise Exception('VMs never became active')

        if result == testcase.TestCase.EX_RUN_ERROR:
            return testcase.TestCase.EX_RUN_ERROR

        self.stop_time = time.time()
        self.result = 100
        return testcase.TestCase.EX_OK

    def _cleanup(self):
        """
        Cleanup all OpenStack objects. Should be called on completion
        :return:
        """
        if self.self_cleanup:
            for creator in reversed(self.creators):
                try:
                    creator.clean()
                except Exception as e:
                    self.logger.error('Unexpected error cleaning - %s', e)

    def _do_vping(self, vm_creator, test_ip):
        """
        Method to be implemented by subclasses
        Begins the real test after the OpenStack environment has been setup
        :param vm_creator: the SNAPS VM instance creator object
        :param test_ip: the IP to which the VM needs to issue the ping
        :return: T/F
        """
        raise NotImplementedError('vping execution is not implemented')

    def __delete_exist_vms(self):
        """
        Cleans any existing VMs using the same name.
        """
        nova_client = nova_utils.nova_client(self.os_creds)
        servers = nova_client.servers.list()
        for server in servers:
            if server.name == self.vm1_name or server.name == self.vm2_name:
                self.logger.info("Deleting instance %s..." % server.name)
                server.delete()


class VPingMain(object):

    def __init__(self, vping_cls):
        self.vping = vping_cls()

    def main(self, **kwargs):
        try:
            result = self.vping.run(**kwargs)
            if result != VPingBase.EX_OK:
                return result
            if kwargs['report']:
                return self.vping.publish_report()
        except:
            return VPingBase.EX_RUN_ERROR
