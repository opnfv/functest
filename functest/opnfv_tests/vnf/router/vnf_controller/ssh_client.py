#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""ssh client module for vrouter testing"""

import logging
import time
import yaml

import paramiko

from functest.opnfv_tests.vnf.router.utilvnf import Utilvnf

RECEIVE_ROOP_WAIT = 1

DEFAULT_CONNECT_TIMEOUT = 10
DEFAULT_CONNECT_RETRY_COUNT = 10
DEFAULT_SEND_TIMEOUT = 10


class SshClient():  # pylint: disable=too-many-instance-attributes
    """ssh client class for vrouter testing"""

    logger = logging.getLogger(__name__)

    def __init__(self, ip_address, user, password=None, key_filename=None):
        self.ip_address = ip_address
        self.user = user
        self.password = password
        self.key_filename = key_filename
        self.connected = False
        self.shell = None

        self.logger.setLevel(logging.INFO)

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.util = Utilvnf()
        with open(self.util.test_env_config_yaml, encoding='utf-8') as file_fd:
            test_env_config_yaml = yaml.safe_load(file_fd)
        file_fd.close()

        self.ssh_revieve_buff = test_env_config_yaml.get("general").get(
            "ssh_receive_buffer")

    def connect(self, time_out=DEFAULT_CONNECT_TIMEOUT,
                retrycount=DEFAULT_CONNECT_RETRY_COUNT):
        # pylint: disable=missing-docstring
        while retrycount > 0:
            try:
                self.logger.info("SSH connect to %s.", self.ip_address)
                self.ssh.connect(self.ip_address,
                                 username=self.user,
                                 password=self.password,
                                 key_filename=self.key_filename,
                                 timeout=time_out,
                                 look_for_keys=False,
                                 allow_agent=False)

                self.logger.info("SSH connection established to %s.",
                                 self.ip_address)

                self.shell = self.ssh.invoke_shell()

                while not self.shell.recv_ready():
                    time.sleep(RECEIVE_ROOP_WAIT)

                self.shell.recv(self.ssh_revieve_buff)
                break
            except Exception:  # pylint: disable=broad-except
                self.logger.info("SSH timeout for %s...", self.ip_address)
                time.sleep(time_out)
                retrycount -= 1

        if retrycount == 0:
            self.logger.warning(
                "Cannot establish connection to IP '%s'", self.ip_address)
            self.connected = False
            return self.connected

        self.connected = True
        return self.connected

    def send(self, cmd, prompt, timeout=DEFAULT_SEND_TIMEOUT):
        # pylint: disable=missing-docstring
        if self.connected is True:
            self.shell.settimeout(timeout)
            self.logger.debug("Commandset : '%s'", cmd)

            try:
                self.shell.send(cmd + '\n')
            except Exception:  # pylint: disable=broad-except
                self.logger.error("ssh send timeout : Command : '%s'", cmd)
                return None

            res_buff = ''
            while not res_buff.endswith(prompt):
                time.sleep(RECEIVE_ROOP_WAIT)
                try:
                    res = self.shell.recv(self.ssh_revieve_buff)
                except Exception:  # pylint: disable=broad-except
                    self.logger.error("ssh receive timeout : Command : '%s'",
                                      cmd)
                    break

                res_buff += res.decode("utf-8")

            self.logger.debug("Response : '%s'", res_buff)
            return res_buff
        self.logger.error("Cannot connected to IP '%s'.", self.ip_address)
        return None

    def close(self):
        # pylint: disable=missing-docstring
        if self.connected is True:
            self.ssh.close()

    @staticmethod
    def error_check(response, err_strs=None):
        # pylint: disable=missing-docstring
        if err_strs is None:
            err_strs = ["error", "warn", "unknown command", "already exist"]
        for err in err_strs:
            if err in response:
                return False

        return True
