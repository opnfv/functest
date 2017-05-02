#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import os
import pprint
import time
from datetime import datetime

import functest.core.testcase as testcase
import functest.utils.openstack_utils as os_utils
from functest.utils.constants import CONST


class VPingBase(testcase.TestCase):
    def __init__(self, **kwargs):
        super(VPingBase, self).__init__(**kwargs)
        self.logger = None
        self.functest_repo = CONST.dir_repo_functest
        self.repo = CONST.dir_vping
        self.vm1_name = CONST.vping_vm_name_1
        self.vm2_name = CONST.vping_vm_name_2
        self.vm_boot_timeout = 180
        self.vm_delete_timeout = 100
        self.ping_timeout = CONST.vping_ping_timeout

        self.image_name = CONST.vping_image_name
        self.image_filename = CONST.openstack_image_file_name
        self.image_format = CONST.openstack_image_disk_format
        self.image_username = CONST.openstack_image_username
        self.image_password = CONST.openstack_image_password
        self.image_path = os.path.join(CONST.dir_functest_images,
                                       self.image_filename)

        self.flavor_name = CONST.vping_vm_flavor

        # NEUTRON Private Network parameters
        self.private_net_name = CONST.vping_private_net_name
        self.private_subnet_name = CONST.vping_private_subnet_name
        self.private_subnet_cidr = CONST.vping_private_subnet_cidr
        self.router_name = CONST.vping_router_name
        self.sg_name = CONST.vping_sg_name
        self.sg_desc = CONST.vping_sg_desc
        self.neutron_client = os_utils.get_neutron_client()
        self.glance_client = os_utils.get_glance_client()
        self.nova_client = os_utils.get_nova_client()

    def run(self, **kwargs):
        if not self.check_repo_exist():
            return testcase.TestCase.EX_RUN_ERROR

        image_id = self.create_image()
        if not image_id:
            return testcase.TestCase.EX_RUN_ERROR

        flavor = self.get_flavor()
        if not flavor:
            return testcase.TestCase.EX_RUN_ERROR

        network_id = self.create_network_full()
        if not network_id:
            return testcase.TestCase.EX_RUN_ERROR

        sg_id = self.create_security_group()
        if not sg_id:
            return testcase.TestCase.EX_RUN_ERROR

        self.delete_exist_vms()

        self.start_time = time.time()
        self.logger.info("vPing Start Time:'%s'" % (
            datetime.fromtimestamp(self.start_time).strftime(
                '%Y-%m-%d %H:%M:%S')))

        vm1 = self.boot_vm(self.vm1_name,
                           image_id,
                           flavor,
                           network_id,
                           None,
                           sg_id)
        if not vm1:
            return testcase.TestCase.EX_RUN_ERROR

        test_ip = self.get_test_ip(vm1)
        vm2 = self.boot_vm(self.vm2_name,
                           image_id,
                           flavor,
                           network_id,
                           test_ip,
                           sg_id)
        if not vm2:
            return testcase.TestCase.EX_RUN_ERROR

        EXIT_CODE = self.do_vping(vm2, test_ip)
        if EXIT_CODE == testcase.TestCase.EX_RUN_ERROR:
            return EXIT_CODE

        self.stop_time = time.time()
        self.parse_result(EXIT_CODE,
                          self.start_time,
                          self.stop_time)
        return testcase.TestCase.EX_OK

    def boot_vm_preparation(self, config, vmname, test_ip):
        pass

    def do_vping(self, vm, test_ip):
        raise NotImplementedError('vping execution is not implemented')

    def check_repo_exist(self):
        if not os.path.exists(self.functest_repo):
            self.logger.error("Functest repository not found '%s'"
                              % self.functest_repo)
            return False
        return True

    def create_image(self):
        _, image_id = os_utils.get_or_create_image(self.image_name,
                                                   self.image_path,
                                                   self.image_format)
        if not image_id:
            return None

        return image_id

    def get_flavor(self):
        try:
            flavor = self.nova_client.flavors.find(name=self.flavor_name)
            self.logger.info("Using existing Flavor '%s'..."
                             % self.flavor_name)
            return flavor
        except:
            self.logger.error("Flavor '%s' not found." % self.flavor_name)
            self.logger.info("Available flavors are: ")
            self.pMsg(self.nova_client.flavor.list())
            return None

    def create_network_full(self):
        network_dic = os_utils.create_network_full(self.neutron_client,
                                                   self.private_net_name,
                                                   self.private_subnet_name,
                                                   self.router_name,
                                                   self.private_subnet_cidr)

        if not network_dic:
            self.logger.error(
                "There has been a problem when creating the neutron network")
            return None
        network_id = network_dic["net_id"]
        return network_id

    def create_security_group(self):
        sg_id = os_utils.get_security_group_id(self.neutron_client,
                                               self.sg_name)
        if sg_id != '':
            self.logger.info("Using existing security group '%s'..."
                             % self.sg_name)
        else:
            self.logger.info("Creating security group  '%s'..."
                             % self.sg_name)
            SECGROUP = os_utils.create_security_group(self.neutron_client,
                                                      self.sg_name,
                                                      self.sg_desc)
            if not SECGROUP:
                self.logger.error("Failed to create the security group...")
                return None

            sg_id = SECGROUP['id']

            self.logger.debug("Security group '%s' with ID=%s created "
                              "successfully." % (SECGROUP['name'], sg_id))

            self.logger.debug("Adding ICMP rules in security group '%s'..."
                              % self.sg_name)
            if not os_utils.create_secgroup_rule(self.neutron_client, sg_id,
                                                 'ingress', 'icmp'):
                self.logger.error("Failed to create security group rule...")
                return None

            self.logger.debug("Adding SSH rules in security group '%s'..."
                              % self.sg_name)
            if not os_utils.create_secgroup_rule(self.neutron_client, sg_id,
                                                 'ingress', 'tcp',
                                                 '22', '22'):
                self.logger.error("Failed to create security group rule...")
                return None

            if not os_utils.create_secgroup_rule(
                    self.neutron_client, sg_id, 'egress', 'tcp', '22', '22'):
                self.logger.error("Failed to create security group rule...")
                return None
        return sg_id

    def delete_exist_vms(self):
        servers = self.nova_client.servers.list()
        for server in servers:
            if server.name == self.vm1_name or server.name == self.vm2_name:
                self.logger.info("Deleting instance %s..." % server.name)
                server.delete()

    def boot_vm(self, vmname, image_id, flavor, network_id, test_ip, sg_id):
        config = dict()
        config['name'] = vmname
        config['flavor'] = flavor
        config['image'] = image_id
        config['nics'] = [{"net-id": network_id}]
        self.boot_vm_preparation(config, vmname, test_ip)
        self.logger.info("Creating instance '%s'..." % vmname)
        self.logger.debug("Configuration: %s" % config)
        vm = self.nova_client.servers.create(**config)

        # wait until VM status is active
        if not self.waitVmActive(self.nova_client, vm):
            vm_status = os_utils.get_instance_status(self.nova_client, vm)
            self.logger.error("Instance '%s' cannot be booted. Status is '%s'"
                              % (vmname, vm_status))
            return None
        else:
            self.logger.info("Instance '%s' is ACTIVE." % vmname)

        self.add_secgroup(vmname, vm.id, sg_id)

        return vm

    def waitVmActive(self, nova, vm):
        # sleep and wait for VM status change
        sleep_time = 3
        count = self.vm_boot_timeout / sleep_time
        while True:
            status = os_utils.get_instance_status(nova, vm)
            self.logger.debug("Status: %s" % status)
            if status == "ACTIVE":
                return True
            if status == "ERROR" or status == "error":
                return False
            if count == 0:
                self.logger.debug("Booting a VM timed out...")
                return False
            count -= 1
            time.sleep(sleep_time)
        return False

    def add_secgroup(self, vmname, vm_id, sg_id):
        self.logger.info("Adding '%s' to security group '%s'..." %
                         (vmname, self.sg_name))
        os_utils.add_secgroup_to_instance(self.nova_client, vm_id, sg_id)

    def get_test_ip(self, vm):
        test_ip = vm.networks.get(self.private_net_name)[0]
        self.logger.debug("Instance '%s' got %s" % (vm.name, test_ip))
        return test_ip

    def parse_result(self, code, start_time, stop_time):
        test_status = "FAIL"
        if code == 0:
            self.logger.info("vPing OK")
            duration = round(stop_time - start_time, 1)
            self.logger.info("vPing duration:'%s'" % duration)
            test_status = "PASS"
        elif code == -2:
            duration = 0
            self.logger.info("Userdata is not supported in nova boot. "
                             "Aborting test...")
        else:
            duration = 0
            self.logger.error("vPing FAILED")

        self.details = {'timestart': start_time,
                        'duration': duration,
                        'status': test_status}
        self.result = test_status

    @staticmethod
    def pMsg(msg):
        """pretty printing"""
        pprint.PrettyPrinter(indent=4).pprint(msg)


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
        except Exception:
            return VPingBase.EX_RUN_ERROR
