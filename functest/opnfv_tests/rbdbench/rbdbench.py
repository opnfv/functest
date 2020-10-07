#!/usr/bin/env python3
'''
code to run rbdbench
'''
import logging
import time
import paramiko
import pkg_resources
import yaml
from xtesting.core import testcase

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)


class StorageValidation(testcase.TestCase):
    # pylint: disable=too-few-public-methods
    '''
    Main class to run rbdbench tool
    '''

    __logger = logging.getLogger('xtesting.ci.run_tests')

    def run(self, **kwargs):
        # pylint: disable-msg=too-many-locals
        '''
        this will execute the rbdbench commands
        '''
        commands = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/rbdbench/commands.yaml')
        conf_cli = yaml.safe_load(open(commands, 'r'))
        rbd_command = conf_cli.split(",")
        client = paramiko.SSHClient()
        cred = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/rbdbench/cred.yaml')
        data = yaml.safe_load(open(cred, 'r'))
        string = data.split(",")
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect("%s" % string[0], username="%s" % string[1],
                           password="%s" % string[2])
            self.__logger.info("Connected to Storage Client")
        except Exception:  # pylint: disable=broad-except
            self.__logger.error("[!] Cannot connect to the SSH Server")
            return testcase.TestCase.EX_RUN_ERROR
        for command in rbd_command:
            _stdin, stdout, _stderr = client.exec_command(command)
            # pylint: disable = unused-variable
            opt = stdout.readlines()
            opt = "".join(opt)
            self.__logger.info("%s", opt)
            var = time.strftime("%d%m%y%H%M%S")
            temp = open("output_%s.txt" % var, "a")
            temp.write(opt)
            temp.close()
            self.result = 100
            return testcase.TestCase.EX_OK
        cred.close()
        commands.close()
