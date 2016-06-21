"""
Description:
    This file is used to setup the running environment
    Include Download code,setup environment variable
            Set onos running config
            Set user name/password
            Onos-push-keys and so on
    lanqinglong@huawei.com

#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
"""

import os
import time
import pexpect
import re
import sys
import pxssh
from connection import connection


class environment(connection):

    def __init__(self):
        connection.__init__(self)
        self.loginfo = connection()
        self.masterhandle = ''
        self.home = ''

    def DownLoadCode(self, handle, codeurl):
        """
        Download Code use 'git clone'
        parameters:
        handle:  current working handle
        codeurl: clone code url
        """
        print "Now loading test codes! Please wait in patient..."
        originalfolder = sys.path[0]
        print originalfolder
        gitclone = handle
        gitclone.sendline("git clone " + codeurl)
        index = 0
        # increment = 0
        while index != 1 or index != 4:
            index = gitclone.expect(['already exists',
                                     'esolving deltas: 100%',
                                     'eceiving objects',
                                     'Already up-to-date',
                                     'npacking objects: 100%', pexpect.EOF])

            filefolder = self.home + '/' + codeurl.split('/')[-1].split('.')[0]
            if index == 0:
                os.chdir(filefolder)
                os.system('git pull')
                os.chdir(originalfolder)
                self.loginfo.log('Download code success!')
                break
            elif index == 1 or index == 4:
                self.loginfo.log('Download code success!')
                gitclone.sendline("mkdir onos")
                gitclone.prompt()
                gitclone.sendline("cp -rf " + filefolder + "/tools onos/")
                gitclone.prompt()
                break
            elif index == 2:
                os.write(1, gitclone.before)
                sys.stdout.flush()
            else:
                self.loginfo.log('Download code failed!')
                self.loginfo.log('Information before' + gitclone.before)
                break
        gitclone.prompt()

    def InstallDefaultSoftware(self, handle):
        """
        Install default software
        parameters:
        handle(input): current working handle
        """
        print "Now Cleaning test environment"
        handle.sendline("sudo apt-get install -y mininet")
        handle.prompt()
        handle.sendline("sudo pip install configobj")
        handle.prompt()
        handle.sendline("sudo apt-get install -y sshpass")
        handle.prompt()
        handle.sendline("OnosSystemTest/TestON/bin/cleanup.sh")
        handle.prompt()
        time.sleep(5)
        self.loginfo.log('Clean environment success!')

    def OnosPushKeys(self, handle, cmd, password):
        """
        Using onos-push-keys to make ssh device without password
        parameters:
        handle(input): working handle
        cmd(input): onos-push-keys xxx(xxx is device)
        password(input): login in password
        """
        print "Now Pushing Onos Keys:" + cmd
        Pushkeys = handle
        Pushkeys.sendline(cmd)
        Result = 0
        while Result != 2:
            Result = Pushkeys.expect(["(yes/no)", "assword:", "PEXPECT]#",
                                      pexpect.EOF, pexpect.TIMEOUT])
            if(Result == 0):
                Pushkeys.sendline("yes")
            if(Result == 1):
                Pushkeys.sendline(password)
            if(Result == 2):
                self.loginfo.log("ONOS Push keys Success!")
                break
            if(Result == 3):
                self.loginfo.log("ONOS Push keys Error!")
                break
            time.sleep(2)
        Pushkeys.prompt()
        print "Done!"

    def SetOnosEnvVar(self, handle, masterpass, agentpass):
        """
        Setup onos pushkeys to all devices(3+2)
        parameters:
        handle(input): current working handle
        masterpass: scripts running server's password
        agentpass: onos cluster&compute node password
        """
        print "Now Setting test environment"
        for host in self.hosts:
            print "try to connect " + str(host)
            result = self.CheckSshNoPasswd(host)
            if not result:
                print ("ssh login failed,try to copy master publickey" +
                       "to agent " + str(host))
                self.CopyPublicKey(host)
        self.OnosPushKeys(handle, "onos-push-keys " + self.OCT, masterpass)
        self.OnosPushKeys(handle, "onos-push-keys " + self.OC1, agentpass)
        self.OnosPushKeys(handle, "onos-push-keys " + self.OC2, agentpass)
        self.OnosPushKeys(handle, "onos-push-keys " + self.OC3, agentpass)
        self.OnosPushKeys(handle, "onos-push-keys " + self.OCN, agentpass)
        self.OnosPushKeys(handle, "onos-push-keys " + self.OCN2, agentpass)

    def CheckSshNoPasswd(self, host):
        """
        Check master can connect agent with no password
        """
        login = pexpect.spawn("ssh " + str(host))
        index = 4
        while index == 4:
            index = login.expect(['(yes/no)', '>|#|\$',
                                  pexpect.EOF, pexpect.TIMEOUT])
            if index == 0:
                login.sendline("yes")
                index = 4
            if index == 1:
                self.loginfo.log("ssh connect to " + str(host) +
                                 " success,no need to copy ssh public key")
                return True
        login.interact()
        return False

    def ChangeOnosName(self, user, password):
        """
        Change onos name in envDefault file
        Because some command depend on this
        parameters:
        user: onos&compute node user
        password: onos&compute node password
        """
        print "Now Changing ONOS name&password"
        filepath = self.home + '/onos/tools/build/envDefaults'
        line = open(filepath, 'r').readlines()
        lenall = len(line) - 1
        for i in range(lenall):
            if "ONOS_USER=" in line[i]:
                line[i] = line[i].replace("sdn", user)
            if "ONOS_GROUP" in line[i]:
                line[i] = line[i].replace("sdn", user)
            if "ONOS_PWD" in line[i]:
                line[i] = line[i].replace("rocks", password)
        NewFile = open(filepath, 'w')
        NewFile.writelines(line)
        NewFile.close
        print "Done!"

    def ChangeTestCasePara(self, testcase, user, password):
        """
        When running test script, there's something need \
        to change in every test folder's *.param & *.topo files
        user: onos&compute node user
        password: onos&compute node password
        """
        print "Now Changing " + testcase + " name&password"
        if self.masterusername == 'root':
            filepath = '/root/'
        else:
            filepath = '/home/' + self.masterusername + '/'
        filepath = (filepath + "OnosSystemTest/TestON/tests/" +
                    testcase + "/" + testcase + ".topo")
        line = open(filepath, 'r').readlines()
        lenall = len(line) - 1
        for i in range(lenall - 2):
            if("localhost" in line[i]) or ("OCT" in line[i]):
                line[i + 1] = re.sub(">\w+", ">" + user, line[i + 1])
                line[i + 2] = re.sub(">\w+", ">" + password, line[i + 2])
            if ("OC1" in line[i] or "OC2" in line[i] or "OC3" in line[i] or
                    "OCN" in line[i] or "OCN2" in line[i]):
                line[i + 1] = re.sub(">\w+", ">root", line[i + 1])
                line[i + 2] = re.sub(">\w+", ">root", line[i + 2])
        NewFile = open(filepath, 'w')
        NewFile.writelines(line)
        NewFile.close

    def SSHlogin(self, ipaddr, username, password):
        """
        SSH login provide a connection to destination.
        parameters:
        ipaddr:   ip address
        username: login user name
        password: login password
        return: handle
        """
        login = pxssh.pxssh()
        login.login(ipaddr, username, password, original_prompt='[$#>]')
        # send command ls -l
        login.sendline('ls -l')
        # match prompt
        login.prompt()
        print("SSH login " + ipaddr + " success!")
        return login

    def SSHRelease(self, handle):
        # Release ssh
        handle.logout()

    def CopyOnostoTestbin(self):
        sourcefile = self.cipath + '/dependencies/onos'
        destifile = self.home + '/onos/tools/test/bin/'
        os.system('pwd')
        runcommand = 'cp ' + sourcefile + ' ' + destifile
        os.system(runcommand)

    def CopyPublicKey(self, host):
        output = os.popen('cat /root/.ssh/id_rsa.pub')
        publickey = output.read().strip('\n')
        tmphandle = self.SSHlogin(self.installer_master,
                                  self.installer_master_username,
                                  self.installer_master_password)
        tmphandle.sendline("ssh " + host + " -T \'echo " +
                           str(publickey) + ">>/root/.ssh/authorized_keys\'")
        tmphandle.prompt()
        self.SSHRelease(tmphandle)
        print "Add OCT PublicKey to " + host + " success"

    def OnosEnvSetup(self, handle):
        """
        Onos Environment Setup function
        """
        self.Gensshkey(handle)
        self.home = self.GetEnvValue(handle, 'HOME')
        self.AddKnownHost(handle, self.OC1, "karaf", "karaf")
        self.AddKnownHost(handle, self.OC2, "karaf", "karaf")
        self.AddKnownHost(handle, self.OC3, "karaf", "karaf")
        self.DownLoadCode(handle,
                          'https://github.com/wuwenbin2/OnosSystemTest.git')
        # self.DownLoadCode(handle, 'https://gerrit.onosproject.org/onos')
        if self.masterusername == 'root':
            filepath = '/root/'
        else:
            filepath = '/home/' + self.masterusername + '/'
        self.OnosRootPathChange(filepath)
        self.CopyOnostoTestbin()
        self.ChangeOnosName(self.agentusername, self.agentpassword)
        self.InstallDefaultSoftware(handle)
        self.SetOnosEnvVar(handle, self.masterpassword, self.agentpassword)
