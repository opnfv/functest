#!/usr/bin/env python

# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""vping_userdata testcase."""

import logging
import time

from snaps.config.network import PortConfig
from snaps.config.vm_inst import VmInstanceConfig
from snaps.openstack.utils import deploy_utils
from xtesting.core import testcase

from functest.opnfv_tests.openstack.vping import vping_base


class VPingUserdata(vping_base.VPingBase):
    """
    Class to execute the vPing test using userdata and the VM's console
    """

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "vping_userdata"
        super(VPingUserdata, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)

    def run(self, **kwargs):
        """
        Sets up the OpenStack VM instance objects then executes the ping and
        validates.
        :return: the exit code from the super.execute() method
        """
        super(VPingUserdata, self).run()

        # Creating Instance 1
        port1_settings = PortConfig(
            name=self.vm1_name + '-vPingPort',
            network_name=self.network_creator.network_settings.name)
        instance1_settings = VmInstanceConfig(
            name=self.vm1_name,
            flavor=self.flavor_name,
            vm_boot_timeout=self.vm_boot_timeout,
            port_settings=[port1_settings])

        self.logger.info(
            "Creating VM 1 instance with name: '%s'",
            instance1_settings.name)
        self.vm1_creator = deploy_utils.create_vm_instance(
            self.os_creds, instance1_settings,
            self.image_creator.image_settings)
        self.creators.append(self.vm1_creator)

        userdata = _get_userdata(
            self.vm1_creator.get_port_ip(port1_settings.name))
        if userdata:
            # Creating Instance 2
            port2_settings = PortConfig(
                name=self.vm2_name + '-vPingPort',
                network_name=self.network_creator.network_settings.name)
            instance2_settings = VmInstanceConfig(
                name=self.vm2_name,
                flavor=self.flavor_name,
                vm_boot_timeout=self.vm_boot_timeout,
                port_settings=[port2_settings],
                userdata=userdata)

            self.logger.info(
                "Creating VM 2 instance with name: '%s'",
                instance2_settings.name)
            self.vm2_creator = deploy_utils.create_vm_instance(
                self.os_creds, instance2_settings,
                self.image_creator.image_settings)
            self.creators.append(self.vm2_creator)
        else:
            raise Exception('Userdata is None')

        return self._execute()

    def _do_vping(self, vm_creator, test_ip):
        """
        Override from super
        """
        self.logger.info("Waiting for ping...")
        exit_code = testcase.TestCase.EX_TESTCASE_FAILED
        sec = 0
        tries = 0

        while True:
            time.sleep(1)
            p_console = vm_creator.get_console_output()
            if "vPing OK" in p_console:
                self.logger.info("vPing detected!")
                exit_code = testcase.TestCase.EX_OK
                break
            elif "failed to read iid from metadata" in p_console or tries > 5:
                self.logger.info("Failed to read iid from metadata")
                break
            elif sec == self.ping_timeout:
                self.logger.info("Timeout reached.")
                break
            elif sec % 10 == 0:
                if "request failed" in p_console:
                    self.logger.debug(
                        "It seems userdata is not supported in nova boot. " +
                        "Waiting a bit...")
                    tries += 1
                else:
                    self.logger.debug(
                        "Pinging %s. Waiting for response...", test_ip)
            sec += 1

        return exit_code


def _get_userdata(test_ip):
    """
    Returns the post VM creation script to be added into the VM's userdata
    :param test_ip: the IP value to substitute into the script
    :return: the bash script contents
    """
    if test_ip:
        return ("#!/bin/sh\n\n"
                "while true; do\n"
                " ping -c 1 %s 2>&1 >/dev/null\n"
                " RES=$?\n"
                " if [ \"Z$RES\" = \"Z0\" ] ; then\n"
                "  echo 'vPing OK'\n"
                "  break\n"
                " else\n"
                "  echo 'vPing KO'\n"
                " fi\n"
                " sleep 1\n"
                "done\n" % str(test_ip))
    return None
