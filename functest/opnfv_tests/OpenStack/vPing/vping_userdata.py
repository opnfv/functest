import time

import functest.utils.functest_logger as ft_logger
from vping_base import VPingBase


class VPingUserData(VPingBase):

    def __init__(self):
        super(self, VPingUserData).__init__()
        self.case_name = 'vping_userdata'
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

        return EXIT_CODE, time.time()
