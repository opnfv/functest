"""
Description:
    This file include basis functions
    lanqinglong@huawei.com

#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
"""

import datetime
import logging
import os
import re
import time

from functest.utils.constants import CONST


class Foundation(object):

    def __init__(self):

        # currentpath = os.getcwd()
        currentpath = '%s/sdn/onos/teston/ci' % CONST.dir_functest_data
        self.cipath = currentpath
        self.logdir = os.path.join(currentpath, 'log')
        self.workhome = currentpath[0: currentpath.rfind('opnfv_tests') - 1]
        self.Result_DB = ''
        filename = time.strftime('%Y-%m-%d-%H-%M-%S') + '.log'
        self.logfilepath = os.path.join(self.logdir, filename)
        self.starttime = datetime.datetime.now()

    def log(self, loginfo):
        """
        Record log in log directory for deploying test environment
        parameters:
        loginfo(input): record info
        """
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s:%(message)s',
                            datefmt='%d %b %Y %H:%M:%S',
                            filename=self.logfilepath,
                            filemode='w')
        filelog = logging.FileHandler(self.logfilepath)
        logging.getLogger('Functest').addHandler(filelog)
        logging.info(loginfo)

    def getdefaultpara(self):
        """
        Get Default Parameters value
        """
        self.Result_DB = os.environ.get('TEST_DB_URL',
                                        CONST.results_test_db_url)
        self.masterusername = CONST.ONOS_onosbench_username
        self.masterpassword = CONST.ONOS_onosbench_password
        self.agentusername = CONST.ONOS_onoscli_username
        self.agentpassword = CONST.ONOS_onoscli_password
        self.runtimeout = CONST.ONOS_runtimeout
        self.OCT = CONST.ONOS_environment_OCT
        self.OC1 = CONST.ONOS_environment_OC1
        self.OC2 = CONST.ONOS_environment_OC2
        self.OC3 = CONST.ONOS_environment_OC3
        self.OCN = CONST.ONOS_environment_OCN
        self.OCN2 = CONST.ONOS_environment_OCN2
        self.installer_master = CONST.ONOS_environment_installer_master
        self.installer_master_username = (
            CONST.ONOS_environment_installer_master_username)
        self.installer_master_password = (
            CONST.ONOS_environment_installer_master_password)
        self.hosts = [self.OC1, self.OCN, self.OCN2]
        self.localhost = self.OCT

    def GetResult(self):
        cmd = "cat " + self.logfilepath + " | grep Fail"
        Resultbuffer = os.popen(cmd).read()
        duration = datetime.datetime.now() - self.starttime
        time.sleep(2)

        if re.search("[1-9]+", Resultbuffer):
            self.log("Testcase Fails\n" + Resultbuffer)
            Result = "POK"
        else:
            self.log("Testcases Pass")
            Result = "OK"
        payload = {'timestart': str(self.starttime),
                   'duration': str(duration), 'status': Result}

        return payload
