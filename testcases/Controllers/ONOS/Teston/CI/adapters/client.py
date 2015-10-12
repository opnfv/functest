"""
Description:
    This file is used to run testcase
    lanqinglong@huawei.com
"""
from environment import environment

class client( environment ):

    def __init__( self ):
        environment.__init__( self )
        self.loginfo = environment()

    def RunScript( self, testname ):
        """
        Run ONOS Test Script
        Parameters:
        testname: ONOS Testcase Name
        masterusername: The server username of running ONOS
        masterpassword: The server password of running ONOS
        """
        self.ChangeTestCasePara( testname, self.masterusername, self.masterpassword )
        runtest = "OnosSystemTest/TestON/bin/cli.py run " + testname
        os.system(runtest)
        print "Done!"

    def onosbasic(self):
        #This is the compass run machine user&pass,you need to modify

        print "Test Begin....."
        self.OnosConnectionSet()
        masterhandle = self.SSHlogin(self.localhost, self.masterusername,
                                    self.masterpassword)
        self.OnosEnvSetup( masterhandle )
        self.SSHRelease( masterhandle )