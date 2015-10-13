"""
Description:
    This file is used to run testcase
    lanqinglong@huawei.com
"""
from environment import environment
import os
import time
import pexpect
import re

class client( environment ):

    def __init__( self ):
        environment.__init__( self )
        self.loginfo = environment()

    def RunScript( self, handle, testname, timeout=300 ):
        """
        Run ONOS Test Script
        Parameters:
        testname: ONOS Testcase Name
        masterusername: The server username of running ONOS
        masterpassword: The server password of running ONOS
        """
        self.ChangeTestCasePara( testname, self.masterusername, self.masterpassword )
        runhandle = handle
        runtest = self.home + "/OnosSystemTest/TestON/bin/cli.py run " + testname
        runhandle.sendline(runtest)
        circletime = 0
        lastshowscreeninfo = ''
        while True:
            Result = runhandle.expect(["PEXPECT]#", pexpect.EOF, pexpect.TIMEOUT])
            curshowscreeninfo = runhandle.before
            if (len(lastshowscreeninfo) != len(curshowscreeninfo)):
                print str(curshowscreeninfo)[len(lastshowscreeninfo)::]
                lastshowscreeninfo = curshowscreeninfo
            if Result == 0:
                print "Done!"
                return
            time.sleep(1)
            circletime += 1
            if circletime > timeout:
                break
        self.loginfo.log( "Timeout when running the test, please check!" )

    def onosstart( self ):
        #This is the compass run machine user&pass,you need to modify

        print "Test Begin....."
        self.OnosConnectionSet()
        masterhandle = self.SSHlogin(self.localhost, self.masterusername,
                                    self.masterpassword)
        self.OnosEnvSetup( masterhandle )
        return masterhandle

    def onosclean( self, handle ):
        self.SSHRelease( handle )
