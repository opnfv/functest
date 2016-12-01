#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

from datetime import datetime
import os
import time
import uuid

from functest.core.testcase_base import TestcaseBase
from functest.core.testcase import TestCase
from functest.utils import functest_utils
from functest.utils.constants import CONST

from snaps.openstack import create_flavor
from snaps.openstack.create_image import ImageSettings
from snaps.openstack.create_flavor import FlavorSettings, OpenStackFlavor
from snaps.openstack.create_network import NetworkSettings, SubnetSettings
from snaps.openstack.tests import openstack_tests
from snaps.openstack.utils import deploy_utils, nova_utils


class VPingBase(TestCase):
    """
    Base class for vPing tests that check connectivity between two VMs shared
    internal network.
    This class is responsible for creating the image, internal network.
    """
    def __init__(self, case_name=''):
        super(VPingBase, self).__init__(case_name)

        self.logger = None
        self.functest_repo = CONST.dir_repo_functest
        self.guid = ''
        if CONST.vping_unique_names:
            self.guid = '-' + str(uuid.uuid4())

        self.os_creds = openstack_tests.get_credentials(
            os_env_file=CONST.openstack_creds)

        self.repo = CONST.dir_vping

        self.image_creator = None
        self.image_creators = list()
        self.network_creator = None
        self.flavor_creator = None
        self.router_creator = None
        self.sg_creator = None
        self.kp_creator = None
        self.vm1_creator = None
        self.vm2_creator = None

        self.self_cleanup = CONST.vping_cleanup_objects

        # Image constants
        self.image_name = CONST.vping_image_name + self.guid
        self.image_url = CONST.openstack_image_url
        self.image_format = CONST.openstack_image_disk_format
        self.image_user = CONST.openstack_image_user

        # VM constants
        self.vm1_name = CONST.vping_vm_name_1 + self.guid
        self.vm2_name = CONST.vping_vm_name_2 + self.guid
        self.vm_boot_timeout = CONST.vping_vm_boot_timeout
        self.vm_delete_timeout = CONST.vping_vm_delete_timeout
        self.vm_ssh_connect_timeout = CONST.vping_vm_ssh_connect_timeout
        self.ping_timeout = CONST.vping_ping_timeout
        self.flavor_name = 'vping-flavor' + self.guid

        # NEUTRON Private Network parameters
        self.private_net_name = CONST.vping_private_net_name + self.guid
        self.private_subnet_name = CONST.vping_private_subnet_name + self.guid
        self.private_subnet_cidr = CONST.vping_private_subnet_cidr

        scenario = functest_utils.get_scenario()

        self.flavor_metadata = create_flavor.MEM_PAGE_SIZE_ANY
        if 'ovs' in scenario or 'fdio' in scenario:
            self.flavor_metadata = create_flavor.MEM_PAGE_SIZE_LARGE

        self.image_custom_config = None
        # Move this configuration option
        if hasattr(CONST, 'snaps_health_check'):
            self.image_custom_config = CONST.snaps_health_check

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

        # TODO - Create SNAPS-OO test helper method for creating images.
        image_base_name = self.image_name + '-' + str(self.guid)
        image_extra_properties = dict()
        disk_image_url = self.image_url

        if self.image_custom_config:
            if 'disk_url' in self.image_custom_config \
                    and self.image_custom_config['disk_url']:
                disk_image_url = self.image_custom_config['disk_url']
            if 'extra_properties' in self.image_custom_config \
                    and  self.image_custom_config['extra_properties']:
                image_extra_properties =\
                    self.image_custom_config['extra_properties']
            if 'kernel_url' in self.image_custom_config \
                    and self.image_custom_config['kernel_url']:
                kernel_image_settings = ImageSettings(
                    name=image_base_name + '-kernel',
                    url=self.image_custom_config['kernel_url'])
                self.image_creators.append(deploy_utils.create_image(
                    self.os_creds, kernel_image_settings))
                kernel_image = self.image_creators[-1].get_image()
                image_extra_properties['kernel_id'] = kernel_image.id
            if 'ramdisk_url' in self.image_custom_config \
                    and self.image_custom_config['ramdisk_url']:
                ramdisk_image_settings = ImageSettings(
                    name=image_base_name + '-ramdisk',
                    url=self.image_custom_config['ramdisk_url'])
                self.image_creators.append(
                    deploy_utils.create_image(self.os_creds,
                                              ramdisk_image_settings))
                ramdisk_image = self.image_creators[-1].get_image()
                image_extra_properties['ramdisk_id'] = ramdisk_image.id

        os_image_settings = ImageSettings(
            name=image_base_name + '-disk',
            url=disk_image_url, img_format=self.image_format,
            image_user=self.image_user,
            extra_properties=image_extra_properties)
        self.logger.info("Creating image with name: '%s'" % self.image_name)
        self.image_creator = deploy_utils.create_image(
            self.os_creds, os_image_settings)
        self.image_creators.append(self.image_creator)

        self.logger.info(
            "Creating network with name: '%s'" % self.private_net_name)
        self.network_creator = deploy_utils.create_network(
            self.os_creds,
            NetworkSettings(name=self.private_net_name,
                            subnet_settings=[SubnetSettings(
                                name=self.private_subnet_name,
                                cidr=self.private_subnet_cidr)]))

        self.logger.info(
            "Creating flavor with name: '%s'" % self.flavor_name)
        self.flavor_creator = OpenStackFlavor(
            self.os_creds,
            FlavorSettings(name=self.flavor_name, ram=512, disk=1, vcpus=1,
                           metadata=self.flavor_metadata))
        self.flavor_creator.create()

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
            exit_code = self._do_vping(self.vm2_creator, test_ip)
        else:
            raise Exception('VMs never became active')

        if exit_code == TestcaseBase.EX_RUN_ERROR:
            return exit_code

        self.stop_time = time.time()
        self.__parse_result(exit_code, self.start_time, self.stop_time)
        return TestcaseBase.EX_OK

    def _cleanup(self):
        """
        Cleanup all OpenStack objects. Should be called on completion
        :return:
        """
        if self.self_cleanup:
            if self.vm2_creator:
                self.logger.info(
                    "Deleting VM 2 instance with name: '%s'"
                    % self.vm2_creator.instance_settings.name)
                self.vm2_creator.clean()
            if self.vm1_creator:
                self.logger.info(
                    "Deleting VM 1 instance with name: '%s'"
                    % self.vm1_creator.instance_settings.name)
                self.vm1_creator.clean()
            if self.router_creator:
                self.logger.info(
                    "Deleting router instance with name: '%s'"
                    % self.router_creator.router_settings.name)
                self.router_creator.clean()
            if self.kp_creator:
                self.logger.info(
                    "Deleting keypair with name: '%s'"
                    % self.kp_creator.keypair_settings.name)
                self.kp_creator.clean()
            if self.sg_creator:
                self.logger.info(
                    "Deleting security group with name: '%s'"
                    % self.sg_creator.sec_grp_settings.name)
                self.sg_creator.clean()
            if self.network_creator:
                self.logger.info(
                    "Deleting network with name: '%s'"
                    % self.network_creator.network_settings.name)
                self.network_creator.clean()
            for image_creator in self.image_creators:
                self.logger.info(
                    "Deleting image with name: '%s'"
                    % image_creator.image_settings.name)
                image_creator.clean()
            if self.flavor_creator:
                self.logger.info(
                    "Deleting flavor with name: '%s'"
                    % self.flavor_name)
                self.flavor_creator.clean()

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

    def __parse_result(self, code, start_time, stop_time):
        """
        Populates self.details and self.criteria for reporting
        :param code: the exit code to parse
        :param start_time: the time the test was started
        :param stop_time: the time the test ended
        """
        test_status = "FAIL"
        duration = round(stop_time - start_time, 1)

        if code == 0:
            self.logger.info("vPing OK")
            self.logger.info("vPing duration:'%s'" % duration)
            test_status = "PASS"
        elif code == -2:
            self.logger.info("Userdata is not supported in nova boot. "
                             "Aborting test...")
        else:
            self.logger.error("vPing FAILED")

        self.details = {'timestart': start_time,
                        'duration': duration,
                        'status': test_status}
        self.criteria = test_status


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
        except Exception:
            return VPingBase.EX_RUN_ERROR
