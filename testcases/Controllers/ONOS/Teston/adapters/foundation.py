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

import functest.utils.config_functest as CONF
import functest.utils.functest_utils as ft_utils


class foundation:

    def __init__(self):

        # currentpath = os.getcwd()
        REPO_PATH = ft_utils.FUNCTEST_REPO + '/'
        currentpath = REPO_PATH + 'testcases/Controllers/ONOS/Teston/CI'
        self.cipath = currentpath
        self.logdir = os.path.join(currentpath, 'log')
        self.workhome = currentpath[0: currentpath.rfind('testcases') - 1]
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
        self.Result_DB = str(
            CONF.get_functest_config('results.test_db_url'))
        self.masterusername = str(
            CONF.get_functest_config('ONOS.general.onosbench_username'))
        self.masterpassword = str(
            CONF.get_functest_config('ONOS.general.onosbench_password'))
        self.agentusername = str(
            CONF.get_functest_config('ONOS.general.onoscli_username'))
        self.agentpassword = str(
            CONF.get_functest_config('ONOS.general.onoscli_password'))
        self.runtimeout = \
            CONF.get_functest_config('ONOS.general.runtimeout')
        self.OCT = str(CONF.get_functest_config('ONOS.environment.OCT'))
        self.OC1 = str(CONF.get_functest_config('ONOS.environment.OC1'))
        self.OC2 = str(CONF.get_functest_config('ONOS.environment.OC2'))
        self.OC3 = str(CONF.get_functest_config('ONOS.environment.OC3'))
        self.OCN = str(CONF.get_functest_config('ONOS.environment.OCN'))
        self.OCN2 = str(CONF.get_functest_config('ONOS.environment.OCN2'))
        self.installer_master = str(
            CONF.get_functest_config('ONOS.environment.installer_master'))
        self.installer_master_username = str(CONF.get_functest_config(
            'ONOS.environment.installer_master_username'))
        self.installer_master_password = str(CONF.get_functest_config(
            'ONOS.environment.installer_master_password'))
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
