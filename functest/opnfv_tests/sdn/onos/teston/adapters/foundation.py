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

import functest.utils.functest_constants as ft_constants
import functest.utils.functest_utils as ft_utils


class Foundation(object):

    def __init__(self):

        # currentpath = os.getcwd()
        currentpath = '%s/sdn/onos/teston/ci' % ft_constants.FUNCTEST_TEST_DIR
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
        self.Result_DB = str(ft_utils.get_db_url())
        self.masterusername = str(ft_constants.ONOSBENCH_USERNAME)
        self.masterpassword = str(ft_constants.ONOSBENCH_PASSWORD)
        self.agentusername = str(ft_constants.ONOSCLI_USERNAME)
        self.agentpassword = str(ft_constants.ONOSCLI_PASSWORD)
        self.runtimeout = ft_constants.ONOS_RUNTIMEOUT
        self.OCT = str(ft_constants.ONOS_OCT)
        self.OC1 = str(ft_constants.ONOS_OC1)
        self.OC2 = str(ft_constants.ONOS_OC2)
        self.OC3 = str(ft_constants.ONOS_OC3)
        self.OCN = str(ft_constants.ONOS_OCN)
        self.OCN2 = str(ft_constants.ONOS_OCN2)
        self.installer_master = str(ft_constants.ONOS_INSTALLER_MASTER)
        self.installer_master_username = \
            str(ft_constants.ONOS_INSTALLER_MASTER_USERNAME)
        self.installer_master_password = \
            ft_constants.ONOS_INSTALLER_MASTER_PASSWORD
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
