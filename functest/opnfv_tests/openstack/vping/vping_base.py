#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import os
import time
from datetime import datetime
import logging
import uuid

import functest.utils.functest_utils as ft_utils
import functest.utils.functest_constants as ft_constants
from functest.core import TestCasesBase

from snaps.openstack.utils import deploy_utils, nova_utils
from snaps.openstack.tests import openstack_tests
from snaps.openstack.create_image import ImageSettings
from snaps.openstack.create_network import NetworkSettings, SubnetSettings

logging.basicConfig(level=logging.INFO)


class VPingBase(TestCasesBase.TestCasesBase):
    """
    Base class for vPing tests that check connectivity between two VMs shared
    internal network.
    This class is responsible for creating the image, internal network.
    """

    def __init__(self):
        def get_conf(parameter):
            return ft_utils.get_functest_config(parameter)

        super(VPingBase, self).__init__()

        self.logger = None
        self.functest_repo = ft_constants.FUNCTEST_REPO_DIR
        self.guid = ''
        if get_conf('vping.unique_names'):
            self.guid = '-' + str(uuid.uuid4())

        self.os_creds = openstack_tests.get_credentials(
            os_env_file=get_conf('general.openstack.creds'))

        self.repo = get_conf('general.directories.dir_vping')

        self.image_creator = None
        self.network_creator = None
        self.router_creator = None
        self.sg_creator = None
        self.kp_creator = None
        self.vm1_creator = None
        self.vm2_creator = None

        self.self_cleanup = get_conf('vping.cleanup_objects')

        # Image constants
        self.image_name = get_conf('vping.image_name') + self.guid
        self.image_url = get_conf('general.openstack.image_url')
        self.image_format = get_conf('general.openstack.image_disk_format')
        self.image_user = get_conf('general.openstack.image_user')

        # VM constants
        self.vm1_name = get_conf('vping.vm_name_1') + self.guid
        self.vm2_name = get_conf('vping.vm_name_2') + self.guid
        self.vm_boot_timeout = get_conf('vping.vm_boot_timeout')
        self.vm_delete_timeout = get_conf('vping.vm_delete_timeout')
        self.vm_ssh_connect_timeout = get_conf('vping.vm_ssh_connect_timeout')
        self.ping_timeout = get_conf('vping.ping_timeout')
        self.flavor_name = get_conf('vping.vm_flavor')

        # NEUTRON Private Network parameters
        self.private_net_name = get_conf(
            'vping.vping_private_net_name') + self.guid
        self.private_subnet_name = get_conf(
            'vping.vping_private_subnet_name') + self.guid
        self.private_subnet_cidr = get_conf('vping.vping_private_subnet_cidr')

    def run(self):
        """
        Begins the test execution which should originate from the subclass
        """
        self.logger.info('Begin virtual environment setup')

        self.start_time = time.time()
        self.logger.info("vPing Start Time:'%s'" % (
            datetime.fromtimestamp(self.start_time).strftime(
                '%Y-%m-%d %H:%M:%S')))

        self.__delete_exist_vms()

        if not os.path.exists(self.functest_repo):
            raise Exception(
                "Functest repository not found '%s'" % self.functest_repo)

        self.logger.info("Creating image with name: '%s'" % self.image_name)
        self.image_creator = deploy_utils.create_image(
            self.os_creds,
            ImageSettings(name=self.image_name, url=self.image_url,
                          img_format=self.image_format,
                          image_user=self.image_user))
        self.logger.info(
            "Creating network with name: '%s'" % self.private_net_name)
        self.network_creator = deploy_utils.create_network(
            self.os_creds,
            NetworkSettings(self.os_creds, name=self.private_net_name,
                            subnet_settings=[SubnetSettings(
                                self.os_creds, name=self.private_subnet_name,
                                cidr=self.private_subnet_cidr)]))

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

        if exit_code == TestCasesBase.TestCasesBase.EX_RUN_ERROR:
            return exit_code

        self.stop_time = time.time()
        self.__parse_result(exit_code, self.start_time, self.stop_time)
        return TestCasesBase.TestCasesBase.EX_OK

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
            if self.image_creator:
                self.logger.info(
                    "Deleting image with name: '%s'"
                    % self.image_creator.image_settings.name)
                self.image_creator.clean()

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
                return self.vping.push_to_db()
        except:
            return VPingBase.EX_RUN_ERROR
