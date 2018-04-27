#!/usr/bin/env python
from snaps.provisioning.ansible_utils import ssh_client
from cinderclient.shell import logger
from sys import stderr

# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""cinder volume testcase."""

import time

from scp import SCPClient
import pkg_resources

from snaps.config.keypair import KeypairConfig
from snaps.config.network import PortConfig
from snaps.config.security_group import (
    Direction, Protocol, SecurityGroupConfig, SecurityGroupRuleConfig)
from snaps.config.vm_inst import FloatingIpConfig, VmInstanceConfig
from snaps.config.volume import VolumeConfig
from snaps.openstack.create_volume import OpenStackVolume
from snaps.openstack.create_instance import OpenStackVmInstance
import snaps.openstack.create_instance
from snaps.openstack.utils import deploy_utils
from xtesting.core import testcase
from xtesting.energy import energy
from functest.opnfv_tests.openstack.cinder_test import cinder_base
from functest.utils import config

class VolumeCheck(cinder_base.VolumeBase):
    """
    Class to execute volume data persistence on 2 different instances
    """

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "volume_check"
        super(VolumeCheck, self).__init__(**kwargs)
        
        self.kp_name = getattr(config.CONF, 'cinder_test_keypair_name') + self.guid
        self.kp_priv_file = getattr(config.CONF, 'cinder_test_keypair_priv_file')
        self.kp_pub_file = getattr(config.CONF, 'cinder_test_keypair_pub_file')
        self.sg_name = getattr(config.CONF, 'cinder_test_sg_name') + self.guid
        self.sg_desc = getattr(config.CONF, 'cinder_test_sg_desc')
        self.sg_creator = None
        
    def run(self, **kwargs):
        """
        Set up the OpenStack volume
        Set up the OpenStack instance objects 
        Create the filesystem and add data to the new volume through userdata
        Validate userdata opperations
        .
        :return: the exit code from the super.execute() method
        """
        try:
            super(VolumeCheck, self).run()
            
            log = "Creating keypair with name: '%s'" % self.kp_name
            self.logger.info(log)
            kp_creator = deploy_utils.create_keypair(
                self.os_creds,
                KeypairConfig(
                    name=self.kp_name, private_filepath=self.kp_priv_file,
                    public_filepath=self.kp_pub_file))
            self.creators.append(kp_creator)
            self.kp_creator = kp_creator
            #Creating security group
            sg_creator = self.__create_security_group()
            self.creators.append(sg_creator)
            self.sg_creator = sg_creator
            
            # Creating Instance 1
            port1_settings = PortConfig(
                name=self.vm1_name + '-volumeTestPort',
                network_name=self.network_creator.network_settings.name)
            instance1_settings = VmInstanceConfig(
                name=self.vm1_name,
                flavor=self.flavor_name,
                vm_boot_timeout=self.vm_boot_timeout,
                vm_delete_timeout=self.vm_delete_timeout,
                ssh_connect_timeout=self.vm_ssh_connect_timeout,
                port_settings=[port1_settings],
                security_group_names=[sg_creator.sec_grp_settings.name],
                volume_names = self.volume_name.split(),
                floating_ip_settings=[FloatingIpConfig(
                    name=self.vm1_name + '-FIPName',
                    port_name=port1_settings.name,
                    router_name=self.router_creator.router_settings.name)])

            self.logger.info(
                "Creating VM 1 instance with name: '%s'",
                instance1_settings.name)
            self.logger.info(log)
            self.vm1_creator = deploy_utils.create_vm_instance(
                self.os_creds,
                instance1_settings,
                self.image_creator.image_settings,
                keypair_creator=self.kp_creator)
            self.creators.append(self.vm1_creator)   
               
            return self._execute()
        except Exception as exc: # pylint: disable=broad-except
            self.logger.error('Unexpected error running test on first instance- ' + exc.message)
            return testcase.TestCase.EX_RUN_ERROR
            
    def run_second_instance(self, **kwargs):
        
        try:
            #create instance 2
            
            self.logger.info("Called run_second_instance")
            kp_creator = deploy_utils.create_keypair(
                self.os_creds,
                KeypairConfig(
                    name=self.kp_name, private_filepath=self.kp_priv_file,
                    public_filepath=self.kp_pub_file))
            self.creators.append(kp_creator)
            port2_settings = PortConfig(
                name=self.vm2_name + '-volumeTestPort',
                network_name=self.network_creator.network_settings.name)
            instance2_settings = VmInstanceConfig(
                name=self.vm2_name, flavor=self.flavor_name,
                vm_boot_timeout=self.vm_boot_timeout,
                vm_delete_timeout=self.vm_delete_timeout,
                ssh_connect_timeout=self.vm_ssh_connect_timeout,
                port_settings=[port2_settings],
                security_group_names=[self.sg_creator.sec_grp_settings.name],
                volume_names = self.volume_name.split(),
                floating_ip_settings=[FloatingIpConfig(
                    name=self.vm2_name + '-FIPName',
                    port_name=port2_settings.name,
                    router_name=self.router_creator.router_settings.name)])
    
            log = ("Creating VM 2 instance with name: '%s'"
                % instance2_settings.name)
            self.logger.info(log)
            self.vm2_creator = deploy_utils.create_vm_instance(
                self.os_creds,
                instance2_settings,
                self.image_creator.image_settings,
                keypair_creator=kp_creator)
            self.creators.append(self.vm2_creator)
            
            return self._execute()
        except Exception as exc:  # pylint: disable=broad-except
            self.logger.error('Unexpected error running test on second instance - ' + exc.message)
            return testcase.TestCase.EX_RUN_ERROR
    
    def vm_clean(self, vm_creator):
        self.logger.info("Removing VM instance")
        try:
            self.vm1_creator.clean()
            sec = 0
            flag = False
            while True:
                time.sleep(1)
                if self.vm1_creator.vm_deleted(block=False):
                   self.logger.info("Virtual instance deleted!")
                   self.creators.remove(vm_creator)
                   flag = True
                   return True
                elif sec == self.vm_delete_timeout:
                   self.logger.info("Timeout reached")
                   flag = True
                   return False
                if flag:
                   break
                log = "Deleting virtual instance... %s" % self.vm1_name
                self.logger.info(log)
                sec += 1 
        except Exception:
            return testcase.TestCase.EX_RUN_ERROR
    
    def _cinder_test(self, vm_creator, opperation):
        if vm_creator.vm_ssh_active(block = True):
            ssh = vm_creator.ssh_client()
            if opperation == 'write':
                logger.info("Starting write data")
                if self._transfer_write_data_script(ssh):
                    if self._write_volume_data(ssh):
                        if self.vm_clean(vm_creator):
                            time.sleep(10)
                            self.run_second_instance()
                else:
                    return testcase.TestCase.EX_RUN_ERROR
            elif opperation == 'check':
                logger.info("Starting check data")
                if self._transfer_check_data_script(ssh):
                    return self._check_volume_data(ssh)
                else:
                    return testcase.TestCase.EX_RUN_ERROR
            else:
                return testcase.TestCase.EX_RUN_ERROR
    
    
    def _transfer_write_data_script(self, ssh):
        """
        Transfert script to VM.

        Uses SCP to copy the script via the SSH client
        :param ssh: the SSH client
        :return:
        """
        self.logger.info("Trying to transfer the script")
        scp = SCPClient(ssh.get_transport())
        write_data_script = pkg_resources.resource_filename(
            'functest.opnfv_tests.openstack.cinder_test', 'write_volume_data.sh')
        try:
            scp.put(write_data_script, "~/")
        except Exception:  # pylint: disable=broad-except
            self.logger.error("Cannot SCP the file '%s'", write_data_script)
            return False

        cmd = 'chmod 755 ~/write_volume_data.sh'
        # pylint: disable=unused-variable
        (stdin, stdout, stderr) = ssh.exec_command(cmd)
        for line in stdout.readlines():
            print line

        return True
    
    def _transfer_check_data_script(self, ssh):
        """
        Transfert script to VM.

        Uses SCP to copy the script via the SSH client
        :param ssh: the SSH client
        :return:
        """
        self.logger.info("Trying to transfer the script")
        scp = SCPClient(ssh.get_transport())
        check_volume_script = pkg_resources.resource_filename(
            'functest.opnfv_tests.openstack.cinder_test', 'check_volume_data.sh')
        try:
            scp.put(check_volume_script, "~/")
        except Exception:  # pylint: disable=broad-except
            self.logger.error("Cannot SCP the file '%s'", check_volume_script)
            return False

        cmd = 'chmod 755 ~/check_volume_data.sh'
        # pylint: disable=unused-variable
        (stdin, stdout, stderr) = ssh.exec_command(cmd)
        for line in stdout.readlines():
            print line

        return True
    
    def _write_volume_data(self, ssh):
        """
        Write data on the new attached volume.

        :param ssh: the SSH client used to issue the command
        :return: exit_code (int)
        """
        
        self.logger.info("Waiting to write data...")

        sec = 0
        cmd = '~/write_volume_data.sh'
        
        time.sleep(1)
        
        while True:
            time.sleep(1)
            (stidin , stdout, stderr) = ssh.exec_command(cmd)
            output = stdout.readlines()
            error= stderr.readlines()
            self.logger.info(output)
            self.logger.info(error)
            for line in output:
                if "New data added to the volume" in line:
                    self.logger.info("New data added to the volume!")
                    return True
                elif sec == self.write_data_timeout:
                    self.logger.info("Timeout reached.")
                    return False
            log = "Writing data to new volume. Waiting for response..."
            self.logger.debug(log)
            sec += 1
        
    
    def _check_volume_data(self, ssh):
        """
        Check data on attached volume.

        :param ssh: the SSH client used to issue the command
        :return: exit_code (int)
        """
        self.logger.info("Waiting for test result...")

        sec = 0
        cmd = '~/check_volume_data.sh '

        while True:
            time.sleep(1)
            (stidin , stdout, stderr) = ssh.exec_command(cmd)
            output = stdout.readlines()
            error= stderr.readlines()
            self.logger.info(output)
            self.logger.info(error)
            for line in output:
                if "Found existing data on volume" in line:
                    self.logger.info("Found existing data on volume")
                    return True
                elif sec == self.write_data_timeout:
                    self.logger.info("Timeout reached.")
                    return False
            
            log = "Check existing data on the volume. Waiting for response..."
            self.logger.debug(log)
            sec += 1
        return exit_code

    def __create_security_group(self):
        """
        Configure OpenStack security groups.

        Configures and deploys an OpenStack security group object
        :return: the creator object
        """
        sg_rules = list()
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name=self.sg_name, direction=Direction.ingress,
                protocol=Protocol.icmp))
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name=self.sg_name, direction=Direction.ingress,
                protocol=Protocol.tcp, port_range_min=22, port_range_max=22))
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name=self.sg_name, direction=Direction.egress,
                protocol=Protocol.tcp, port_range_min=22, port_range_max=22))

        log = "Security group with name: '%s'" % self.sg_name
        self.logger.info(log)
        return deploy_utils.create_security_group(self.os_creds,
                                                  SecurityGroupConfig(
                                                      name=self.sg_name,
                                                      description=self.sg_desc,
                                                      rule_settings=sg_rules))
    

