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

    def __init__(self, **kwargs):
        testcase.TestCase.__init__(self, **kwargs)
        self.rbd_command = ''
        self.string = ''

    def openfile(self):
        '''
        This function contains credentials and commands
        '''
        commands = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/rbdbench/commands.yaml')
        conf_cli = yaml.safe_load(open(commands, 'r'))
        self.rbd_command = conf_cli.split(",")
        cred = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/rbdbench/cred.yaml')
        data = yaml.safe_load(open(cred, 'r'))
        self.string = data.split(",")
        self.__logger.info("Commands have been read")

    def execute(self):
        '''
        This function will execute rbd commands
        '''

        client = paramiko.SSHClient()

        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect("%s" % self.string[0],
                           username="%s" % self.string[1],
                           password="%s" % self.string[2])
            self.__logger.info("Connected to Storage Client")
        except Exception:  # pylint: disable=broad-except
            self.__logger.error("[!] Cannot connect to the SSH Server")
            return testcase.TestCase.EX_RUN_ERROR
        for command in self.rbd_command:
            _stdin, stdout, _stderr = client.exec_command(command)
            opt = stdout.readlines()
            err = _stderr.readlines()
            if err:
                self.result = 0
                res = testcase.TestCase.EX_RUN_ERROR
            else:
                opt = "".join(opt)
                self.__logger.info("%s", opt)
                var = time.strftime("%d%m%y%H%M%S")
                temp = open("output_%s.txt" % var, "a")
                temp.write(opt)
                temp.close()
                self.result = 100
                res = testcase.TestCase.EX_OK
            return res

    def run(self, **kwargs):

        self.start_time = time.time()
        self.openfile()
        self.execute()
        self.stop_time = time.time()
