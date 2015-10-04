"""
Description:
    This file is used to setup the running environment
    Include Download code,setup environment variable
            Set onos running config
            Set user name/password
            Onos-push-keys and so on
    lanqinglong@huawei.com
"""

import os
import time
import pexpect
import re
import sys
import pxssh
from foundation import foundation

class environment:

    def __init__( self ):
        self.loginfo = foundation( )
        self.masterhandle = ''

    def DownLoadCode( self, handle, codeurl ):
        """
        Download Code use 'git clone'
        parameters:
        handle:  current working handle
        codeurl: clone code url
        """
        print "Now loading test codes! Please wait in patient..."
        originalfolder = os.getcwd()
        gitclone = handle
        gitclone.sendline( "git clone " + codeurl )
        index = 0
        while index != 1 or index != 4:
            index = gitclone.expect ( ['already exists', 'resolving deltas: 100%', \
                                    'Receiving objects', 'Already up-to-date', \
                                    pexpect.EOF] )

            filefolder = originalfolder + '/' + codeurl.split('/')[-1].split('.')[0]
            if index == 0 :
                os.chdir( filefolder )
                os.system( 'git pull' )
                os.chdir( originalfolder )
                self.loginfo.log( 'Download code success!' )
                break
            elif index == 1 :
                self.loginfo.log( 'Download code success!' )
                break
            elif index == 2 :
                increment += 1
                if increment == 20:
                    print '\n'
                print '.'
            else :
                self.loginfo.log( 'Download code failed!' )
                self.loginfo.log( 'Information before' + gitclone.before )
                break
            time.sleep(5)
        gitclone.prompt( )

    def InstallDefaultSoftware( self, handle ):
        """
        Install default software
        parameters:
        handle(input): current working handle
        """
        print "Now Cleaning test environment"
        handle.sendline("sudo apt-get install -y mininet")
        handle.prompt( )
        handle.sendline("sudo pip install configobj")
        handle.prompt( )
        handle.sendline("sudo apt-get install -y sshpass")
        handle.prompt( )
        handle.sendline("OnosSystemTest/TestON/bin/cleanup.sh")
        handle.prompt( )
        time.sleep(5)
        self.loginfo.log( 'Clean environment success!' )

    def OnosPushKeys(self, handle, cmd, password):
        """
        Using onos-push-keys to make ssh device without password
        parameters:
        handle(input): working handle
        cmd(input): onos-push-keys xxx(xxx is device)
        password(input): login in password
        """
        print "Now Pushing Onos Keys:"+cmd
        Pushkeys = handle
        Pushkeys.sendline( cmd )
        Result = 0
        while Result != 2:
            Result = Pushkeys.expect( ["yes", "password", "#|$", pexpect.EOF, \
                                       pexpect.TIMEOUT])
            if ( Result == 0 ):
                Pushkeys.sendline( "yes" )
            if ( Result == 1 ):
                Pushkeys.sendline( password )
            if ( Result == 2 ):
                self.loginfo.log( "ONOS Push keys Success!" )
            if ( Result == 3 ):
                self.loginfo.log( "ONOS Push keys Error!" )
        Pushkeys.prompt( )
        print "Done!"

    def SetOnosEnvVar( self, handle, masterpass, agentpass):
        """
        Setup onos pushkeys to all devices(3+2)
        parameters:
        handle(input): current working handle
        masterpass: scripts running server's password
        agentpass: onos cluster&compute node password
        """
        print "Now Setting test environment"
        self.OnosPushKeys( handle, "onos-push-keys " + self.OCT, masterpass)
        self.OnosPushKeys( handle, "onos-push-keys " + self.OC1, agentpass)
        self.OnosPushKeys( handle, "onos-push-keys " + self.OC2, agentpass)
        self.OnosPushKeys( handle, "onos-push-keys " + self.OC3, agentpass)
        self.OnosPushKeys( handle, "onos-push-keys " + self.OCN, agentpass)
        self.OnosPushKeys( handle, "onos-push-keys " + self.OCN2, agentpass)

    def ChangeOnosName( self, user, password):
        """
        Change onos name in envDefault file
        Because some command depend on this
        parameters:
        user: onos&compute node user
        password: onos&compute node password
        """
        print "Now Changing ONOS name&password"
        if masterusername is 'root':
            filepath = '/root/'
        else :
            filepath = '/home/' +masterusername + '/'
        line = open(filepath + "onos/tools/build/envDefaults", 'r').readlines()
        lenall = len(line)-1
        for i in range(lenall):
           if "ONOS_USER=" in line[i]:
               line[i]=line[i].replace("sdn",user)
           if "ONOS_GROUP" in line[i]:
               line[i]=line[i].replace("sdn",user)
           if "ONOS_PWD" in line[i]:
               line[i]=line[i].replace("rocks",password)
        NewFile = open("onos/tools/build/envDefaults",'w')
        NewFile.writelines(line)
        NewFile.close
        print "Done!"

    def ChangeTestCasePara(testcase,user,password):
        """
        When running test script, there's something need \
        to change in every test folder's *.param & *.topo files
        user: onos&compute node user
        password: onos&compute node password
        """
        print "Now Changing " + testcase +  " name&password"
        if masterusername is 'root':
            filepath = '/root/'
        else :
            filepath = '/home/' + masterusername + '/'
        filepath = filepath +"OnosSystemTest/TestON/tests/" + testcase + "/" + \
                   testcase + ".topo"
        line = open(filepath,'r').readlines()
        lenall = len(line)-1
        for i in range(lenall-2):
           if ("localhost" in line[i]) or ("OCT" in line[i]):
               line[i+1]=re.sub(">\w+",">"+user,line[i+1])
               line[i+2]=re.sub(">\w+",">"+password,line[i+2])
           if "OC1" in line [i] \
              or "OC2" in line [i] \
              or "OC3" in line [i] \
              or "OCN" in line [i] \
              or "OCN2" in line[i]:
               line[i+1]=re.sub(">\w+",">root",line[i+1])
               line[i+2]=re.sub(">\w+",">root",line[i+2])
        NewFile = open(filepath,'w')
        NewFile.writelines(line)
        NewFile.close

    def SSHlogin ( self, ipaddr, username, password ) :
        """
        SSH login provide a connection to destination.
        parameters:
        ipaddr:   ip address
        username: login user name
        password: login password
        return: handle
        """
        login = pxssh.pxssh( )
        login.login ( ipaddr, username, password, original_prompt='[$#>]')
        #send command ls -l
        login.sendline ('ls -l')
        #match prompt
        login.prompt()
        print ("SSH login " + ipaddr + " success!")
        return login

    def SSHRelease( self, handle ):
        #Release ssh
        handle.logout()

    def OnosEnvSetup( self, handle ):
        """
        Onos Environment Setup function
        """
        self.DownLoadCode( handle, 'https://github.com/sunyulin/OnosSystemTest.git' )
        self.DownLoadCode( handle, 'https://gerrit.onosproject.org/onos' )
        self.ChangeOnosName(self.agentusername,self.agentpassword)
        self.InstallDefaultSoftware( handle )
        self.SetOnosEnvVar(handle, self.masterpassword,self.agentpassword)