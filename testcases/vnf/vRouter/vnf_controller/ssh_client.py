#!/usr/bin/python
# coding: utf8
#######################################################################
#
# Copyright (c) 2016 Okinawa Open Laboratory
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
########################################################################

import logging
import os
import paramiko
import time
import yaml

import functest.utils.functest_logger as ft_logger

""" logging configuration """
logger = ft_logger.Logger("vRouter.ssh_client").getLogger()
logger.setLevel(logging.INFO)

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)
f.close()

SSH_RECEIVE_BUFFER = functest_yaml.get("vRouter").get("general").get(
    "ssh_receive_buffer")
RECEIVE_ROOP_WAIT = 1


class SSH_Client():

    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password
        self.connected = False

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, time_out=10, retrycount=10):
        while retrycount > 0:
            try:
                logger.info("SSH connect to %s." % self.ip)
                self.ssh.connect(self.ip,
                                 username=self.user,
                                 password=self.password,
                                 timeout=time_out,
                                 look_for_keys=False,
                                 allow_agent=False)

                logger.info("SSH connection established to %s." % self.ip)

                self.shell = self.ssh.invoke_shell()

                while not self.shell.recv_ready():
                    time.sleep(1)

                self.shell.recv(SSH_RECEIVE_BUFFER)
                break
            except:
                logger.info("SSH timeout for %s..." % self.ip)
                retrycount -= 1

        if retrycount == 0:
            logger.error("Cannot establish connection to IP '%s'. Aborting"
                         % self.ip)
            self.connected = False
            return self.connected

        self.connected = True
        return self.connected

    def send(self, cmd, prompt, timeout=10):
        if self.connected is True:
            self.shell.settimeout(timeout)
            logger.debug("Commandset : '%s'", cmd)

            try:
                self.shell.send(cmd + '\n')
            except:
                logger.error("ssh send timeout : Command : '%s'", cmd)
                return None

            res_buff = ''
            while not res_buff.endswith(prompt):
                time.sleep(RECEIVE_ROOP_WAIT)
                try:
                    res = self.shell.recv(SSH_RECEIVE_BUFFER)
                except:
                    logger.error("ssh receive timeout : Command : '%s'", cmd)
                    break

                res_buff += res

            logger.debug("Response : '%s'", res_buff)
            return res_buff
        else:
            logger.error("Cannot connected to IP '%s'." % self.ip)
            return None

    def close(self):
        if self.connected is True:
            self.ssh.close()

    def error_check(self, response, err_strs=["error",
                                              "warn",
                                              "unknown command",
                                              "already exist"]):
        for err in err_strs:
            if err in response:
                return False

        return True
