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

from xtesting.core import testcase

from functest.core import singlevm
from functest.utils import config


class VPingUserdata(singlevm.VmReady2):
    """
    Class to execute the vPing test using userdata and the VM's console
    """

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "vping_userdata"
        super(VPingUserdata, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.vm1 = None
        self.vm2 = None

    def run(self, **kwargs):
        """
        Sets up the OpenStack VM instance objects then executes the ping and
        validates.
        :return: the exit code from the super.execute() method
        """
        try:
            assert self.cloud
            assert super(VPingUserdata, self).run(
                **kwargs) == testcase.TestCase.EX_OK
            self.result = 0
            self.vm1 = self.boot_vm()
            self.vm2 = self.boot_vm(
                '{}-vm2_{}'.format(self.case_name, self.guid),
                userdata=self._get_userdata())
            self.vm2 = self.cloud.wait_for_server(self.vm2, auto_ip=False)

            result = self._do_vping()
            self.stop_time = time.time()
            if result != testcase.TestCase.EX_OK:
                return testcase.TestCase.EX_RUN_ERROR
            self.result = 100
            return testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            self.logger.exception('Unexpected error running vping_userdata')
            return testcase.TestCase.EX_RUN_ERROR

    def _do_vping(self):
        """
        Override from super
        """
        if not (self.vm1.private_v4 or self.vm1.addresses[
                self.network.name][0].addr):
            self.logger.error("vm1: IP addr missing")
            return testcase.TestCase.EX_TESTCASE_FAILED

        self.logger.info("Waiting for ping...")
        exit_code = testcase.TestCase.EX_TESTCASE_FAILED
        sec = 0
        tries = 0

        while True:
            time.sleep(1)
            p_console = self.cloud.get_server_console(self.vm2.id)
            self.logger.debug("console: \n%s", p_console)
            if "vPing OK" in p_console:
                self.logger.info("vPing detected!")
                exit_code = testcase.TestCase.EX_OK
                break
            elif "failed to read iid from metadata" in p_console or tries > 5:
                self.logger.info("Failed to read iid from metadata")
                break
            elif sec == getattr(config.CONF, 'vping_ping_timeout'):
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
                        "Pinging %s. Waiting for response...",
                        self.vm1.private_v4 or self.vm1.addresses[
                            self.network.name][0].addr)
            sec += 1

        return exit_code

    def _get_userdata(self):
        """
        Returns the post VM creation script to be added into the VM's userdata
        :param test_ip: the IP value to substitute into the script
        :return: the bash script contents
        """
        if self.vm1.private_v4 or self.vm1.addresses[
                self.network.name][0].addr:
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
                    "done\n" % str(
                        self.vm1.private_v4 or self.vm1.addresses[
                            self.network.name][0].addr))
        return None

    def clean(self):
        assert self.cloud
        if self.vm1:
            self.cloud.delete_server(
                self.vm1, wait=True,
                timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        if self.vm2:
            self.cloud.delete_server(
                self.vm2, wait=True,
                timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        super(VPingUserdata, self).clean()
