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

import logging
import os
import time
import yaml
import re
import datetime


class foundation:

    def __init__(self):

        # currentpath = os.getcwd()
        REPO_PATH = os.environ['repos_dir'] + '/functest/'
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
        print loginfo
        logging.info(loginfo)

    def getdefaultpara(self):
        """
        Get Default Parameters value
        """
        with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
            functest_yaml = yaml.safe_load(f)

        self.Result_DB = str(functest_yaml.get("results").get("test_db_url"))
        self.masterusername = str(functest_yaml.get("ONOS").get("general").
                                  get('onosbench_username'))
        self.masterpassword = str(functest_yaml.get("ONOS").get("general").
                                  get("onosbench_password"))
        self.agentusername = str(functest_yaml.get("ONOS").get("general").
                                 get("onoscli_username"))
        self.agentpassword = str(functest_yaml.get("ONOS").get("general").
                                 get("onoscli_password"))
        self.runtimeout = functest_yaml.get("ONOS").get("general").get(
            "runtimeout")
        self.OCT = str(functest_yaml.get("ONOS").get("environment").get("OCT"))
        self.OC1 = str(functest_yaml.get("ONOS").get("environment").get("OC1"))
        self.OC2 = str(functest_yaml.get("ONOS").get("environment").get("OC2"))
        self.OC3 = str(functest_yaml.get("ONOS").get("environment").get("OC3"))
        self.OCN = str(functest_yaml.get("ONOS").get("environment").get("OCN"))
        self.OCN2 = str(functest_yaml.get("ONOS").
                        get("environment").get("OCN2"))
        self.installer_master = str(functest_yaml.get("ONOS").
                                    get("environment").get("installer_master"))
        self.installer_master_username = str(functest_yaml.get("ONOS").
                                             get("environment").
                                             get("installer_master_username"))
        self.installer_master_password = str(functest_yaml.get("ONOS").
                                             get("environment").
                                             get("installer_master_password"))
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
