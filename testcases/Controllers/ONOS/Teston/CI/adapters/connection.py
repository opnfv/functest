"""
Description:
    This file is used to make connections
    Include ssh & exchange public-key to each other so that
    it can run without password

    lanqinglong@huawei.com
"""
import os
import os.path
import time
import pexpect
import re
import sys
from foundation import foundation

class connection:

    def __init__( self ):
        self.loginfo = foundation()

    def AddKnownHost( self, ipaddr, username, password ):
        """
        Add an user to known host,so that onos can login in with onos $ipaddr.
        parameters:
        ipaddr:   ip address
        username: login user name
        password: login password
        """
        print( "Now Adding an user to known hosts " + ipaddr )
        login = pexpect.spawn( "ssh -l %s -p 8101 %s"%( username, ipaddr ) )
        index = 0
        while index != 2:
            index = login.expect( ['assword:', 'yes/no', pexpect.EOF, \
                                   pexpect.TIMEOUT] )
            if index == 0:
                login.sendline( password )
                login.sendline( "logout" )
                index = login.expect( ["closed", pexpect.EOF] )
                if index == 0:
                    self.loginfo.log( "Add SSH Known Host Success!" )
                else:
                    self.loginfo.log( "Add SSH Known Host Failed! Please Check!" )
                #login.interact()

            if index == 1:
                login.sendline('yes')

    def Gensshkey( self ):
        """
        Generate ssh keys, used for some server have no sshkey.
        """
        print "Now Generating SSH keys..."
        os.system("rm -rf ~/.ssh/*")
        keysub = pexpect.spawn("ssh-keygen -t rsa")
        Result = 0
        while Result != 2:
            Result = keysub.expect( ["Overwrite", "Enter", pexpect.EOF, \
                                     pexpect.TIMEOUT])
            if Result == 0:
                keysub.sendline("y")
            if Result == 1:
                keysub.sendline("\n")
            if Result == 3:
                self.loginfo.log("Generate SSH key failed.")

        self.loginfo.log( "Generate SSH key success." )

    def GetRootAuth( self, password ):
        """
        Get root user
        parameters:
        password: root login password
        """
        print( "Now changing to user root" )
        login = pexpect.spawn( "su - root" )
        index = 0
        while index != 2:
            index = login.expect( ['assword:', "failure", \
                                   pexpect.EOF, pexpect.TIMEOUT] )
            if index == 0:
                login.sendline( password )
            if index == 1:
                self.loginfo.log("Change user to root failed.")

        login.interact()

    def ReleaseRootAuth( self ):
        """
        Exit root user.
        """
        print( "Now Release user root" )
        login = pexpect.spawn( "exit" )
        index = login.expect( ['logout', \
                                pexpect.EOF, pexpect.TIMEOUT] )
        if index == 0:
            self.loginfo.log("Release root user success.")
        if index == 1:
            self.loginfo.log("Release root user failed.")

        login.interact()

    def AddEnvIntoBashrc( self, envalue ):
        """
        Add Env var into /etc/profile.
        parameters:
        envalue: environment value to add
        """
        print "Now Adding bash environment"
        fileopen = open( "/etc/profile", 'r' )
        findContext = 1
        while findContext:
            findContext = fileopen.readline( )
            result = findContext.find( envalue )
            if result != -1:
                break
        fileopen.close
        if result == -1:
            envAdd = open( "/etc/profile", 'a+' )
            envAdd.writelines( "\n" + envalue )
            envAdd.close( )
        self.loginfo.log( "Add env to bashrc success!" )

    def OnosConnectionSet (self):
        """
        Intergrate for ONOS connection setup
        """
        self.Gensshkey()
        self.AddKnownHost( self.OC1, "karaf", "karaf" )
        self.AddKnownHost( self.OC2, "karaf", "karaf" )
        self.AddKnownHost( self.OC3, "karaf", "karaf" )
        currentpath = os.getcwd()
        filepath = os.path.join( currentpath, "onos/tools/dev/bash_profile" )
        self.AddEnvIntoBashrc("source " + filepath + "\n")
        self.AddEnvIntoBashrc("export OCT=" + self.OCT)
        self.AddEnvIntoBashrc("export OC1=" + self.OC1)
        self.AddEnvIntoBashrc("export OC2=" + self.OC2)
        self.AddEnvIntoBashrc("export OC3=" + self.OC3)
        self.AddEnvIntoBashrc("export OCN=" + self.OCN)
        self.AddEnvIntoBashrc("export OCN2=" + self.OCN2)
        self.AddEnvIntoBashrc("export localhost=" + self.localhost)
