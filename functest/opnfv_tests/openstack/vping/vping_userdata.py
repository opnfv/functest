#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import sys
import time

import argparse

import functest.utils.functest_logger as ft_logger
import vping_base


class VPingUserdata(vping_base.VPingBase):

    def __init__(self, case_name='vping_userdata'):
        super(VPingUserdata, self).__init__(case_name)
        self.logger = ft_logger.Logger(self.case_name).getLogger()

    def boot_vm_preparation(self, config, vmname, test_ip):
        config['config_drive'] = True
        if vmname == self.vm2_name:
            u = ("#!/bin/sh\n\n"
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
            config['userdata'] = u

    def do_vping(self, vm, test_ip):
        self.logger.info("Waiting for ping...")
        EXIT_CODE = -1
        sec = 0
        tries = 0

        while True:
            time.sleep(1)
            p_console = vm.get_console_output()
            if "vPing OK" in p_console:
                self.logger.info("vPing detected!")
                EXIT_CODE = 0
                break
            elif "failed to read iid from metadata" in p_console or tries > 5:
                EXIT_CODE = -2
                break
            elif sec == self.ping_timeout:
                self.logger.info("Timeout reached.")
                break
            elif sec % 10 == 0:
                if "request failed" in p_console:
                    self.logger.debug("It seems userdata is not supported "
                                      "in nova boot. Waiting a bit...")
                    tries += 1
                else:
                    self.logger.debug("Pinging %s. Waiting for response..."
                                      % test_ip)
            sec += 1

        return EXIT_CODE


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-r", "--report",
                             help="Create json result file",
                             action="store_true")
    args = vars(args_parser.parse_args())

    sys.exit(vping_base.VPingMain(VPingUserdata).main(**args))
