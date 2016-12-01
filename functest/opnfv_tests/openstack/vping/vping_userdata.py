#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import argparse
import sys
import time

from snaps.openstack.utils import deploy_utils
from snaps.openstack.create_instance import VmInstanceSettings
from snaps.openstack.create_network import PortSettings

from functest.core.testcase_base import TestcaseBase
import functest.utils.functest_logger as ft_logger
import vping_base


class VPingUserdata(vping_base.VPingBase):
    """
    Class to execute the vPing test using userdata and the VM's console
    """

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "vping_userdata"
        super(VPingUserdata, self).__init__(**kwargs)
        self.logger = ft_logger.Logger(self.case_name).getLogger()

    def run(self):
        """
        Sets up the OpenStack VM instance objects then executes the ping and
        validates.
        :return: the exit code from the super.execute() method
        """
        try:
            super(VPingUserdata, self).run()

            # Creating Instance 1
            port1_settings = PortSettings(
                name=self.vm1_name + '-vPingPort',
                network_name=self.network_creator.network_settings.name)
            instance1_settings = VmInstanceSettings(
                name=self.vm1_name,
                flavor=self.flavor_name,
                vm_boot_timeout=self.vm_boot_timeout,
                port_settings=[port1_settings])

            self.logger.info(
                "Creating VM 1 instance with name: '%s'"
                % instance1_settings.name)
            self.vm1_creator = deploy_utils.create_vm_instance(
                self.os_creds, instance1_settings,
                self.image_creator.image_settings)

            userdata = _get_userdata(
                self.vm1_creator.get_port_ip(port1_settings.name))
            if userdata:
                # Creating Instance 2
                port2_settings = PortSettings(
                    name=self.vm2_name + '-vPingPort',
                    network_name=self.network_creator.network_settings.name)
                instance2_settings = VmInstanceSettings(
                    name=self.vm2_name,
                    flavor=self.flavor_name,
                    vm_boot_timeout=self.vm_boot_timeout,
                    port_settings=[port2_settings],
                    userdata=userdata)

                self.logger.info(
                    "Creating VM 2 instance with name: '%s'"
                    % instance2_settings.name)
                self.vm2_creator = deploy_utils.create_vm_instance(
                    self.os_creds, instance2_settings,
                    self.image_creator.image_settings)
            else:
                raise Exception('Userdata is None')

            return self._execute()
        except Exception as e:
            self.logger.error('Unexpected error - ' + e.message)
            return TestcaseBase.EX_RUN_ERROR
        finally:
            self._cleanup()

    def _do_vping(self, vm_creator, test_ip):
        """
        Override from super
        """
        self.logger.info("Waiting for ping...")
        exit_code = -1
        sec = 0
        tries = 0

        while True:
            time.sleep(1)
            p_console = vm_creator.get_vm_inst().get_console_output()
            if "vPing OK" in p_console:
                self.logger.info("vPing detected!")
                exit_code = 0
                break
            elif "failed to read iid from metadata" in p_console or tries > 5:
                exit_code = -2
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
                        "Pinging %s. Waiting for response..." % test_ip)
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
                "done\n" % test_ip)
    return None


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-r", "--report",
                             help="Create json result file",
                             action="store_true")
    args = vars(args_parser.parse_args())

    sys.exit(vping_base.VPingMain(VPingUserdata).main(**args))
