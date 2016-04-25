"""
Description:
    This file is used to run testcase
    lanqinglong@huawei.com

#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
"""
from environment import environment
import time
import pexpect
import requests
import json


class client(environment):

    def __init__(self):
        environment.__init__(self)
        self.loginfo = environment()
        self.testcase = ''

    def RunScript(self, handle, testname, timeout=300):
        """
        Run ONOS Test Script
        Parameters:
        testname: ONOS Testcase Name
        masterusername: The server username of running ONOS
        masterpassword: The server password of running ONOS
        """
        self.testcase = testname
        self.ChangeTestCasePara(testname, self.masterusername,
                                self.masterpassword)
        runhandle = handle
        runtest = (self.home + "/OnosSystemTest/TestON/bin/cli.py run " +
                   testname)
        runhandle.sendline(runtest)
        circletime = 0
        lastshowscreeninfo = ''
        while True:
            Result = runhandle.expect(["PEXPECT]#", pexpect.EOF,
                                       pexpect.TIMEOUT])
            curshowscreeninfo = runhandle.before
            if(len(lastshowscreeninfo) != len(curshowscreeninfo)):
                self.loginfo.log(str(curshowscreeninfo)
                                 [len(lastshowscreeninfo)::])
                lastshowscreeninfo = curshowscreeninfo
            if Result == 0:
                print "Done!"
                return
            time.sleep(1)
            circletime += 1
            if circletime > timeout:
                break
        self.loginfo.log("Timeout when running the test, please check!")

    def onosstart(self):
        # This is the compass run machine user&pass,you need to modify

        print "Test Begin....."
        self.OnosConnectionSet()
        masterhandle = self.SSHlogin(self.localhost, self.masterusername,
                                     self.masterpassword)
        self.OnosEnvSetup(masterhandle)
        return masterhandle

    def onosclean(self, handle):
        self.SSHRelease(handle)
        self.loginfo.log('Release onos handle Successful')

    def push_results_to_db(self, payload, pushornot=1):
        if pushornot != 1:
            return 1
        url = self.Result_DB + "/results"
        params = {"project_name": "functest", "case_name": "ONOS-" +
                  self.testcase, "pod_name": 'huawei-build-2',
                  "details": payload}

        headers = {'Content-Type': 'application/json'}
        try:
            r = requests.post(url, data=json.dumps(params), headers=headers)
            self.loginfo.log(r)
        except:
            self.loginfo.log('Error pushing results into Database')
