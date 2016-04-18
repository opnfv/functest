#!/usr/bin/python
#
# Copyright (c) 2016 Red Hat
# Luke Hinds (lhinds@redhat.com)
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# 0.1: OpenSCAP paramiko connection functions

import os
import paramiko

__version__ = 0.1
__author__ = 'Luke Hinds (lhinds@redhat.com)'
__url__ = 'http:/https://wiki.opnfv.org/display/security'


class connectionManager:
    def __init__(self, hostname, user, password, *args):
        self.hostname = hostname
        self.user = user
        self.password = password
        self.args = args

    def remotescript(self):
        localpath = self.args[0]
        remotepath = self.args[1]
        com = self.args[2]

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.hostname, 22, self.user, self.password)

        sftp = client.open_sftp()
        sftp.put(localpath, remotepath)

        output = ""
        stdin, stdout, stderr = client.exec_command(com)
        stdout = stdout.readlines()
        sftp.remove(remotepath)
        client.close()

        # Spool it back (can be improved at later point)
        for line in stdout:
            output = output + line
        if output != "":
            return output

    def remotecmd(self):
        com = self.args[0]
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.hostname, 22, self.user, self.password)
        output = ""
        stdin, stdout, stderr = client.exec_command(com)
        stdout = stdout.readlines()
        client.close()

        # Spool it back (can be improved at later point)
        for line in stdout:
            output = output + line
        if output != "":
            return output
        else:
            print "There was no output for this command"

    def run_tool(self):
        dist = self.args[0]
        report = self.args[1]
        com = self.args[2]
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.hostname, 22, self.user, self.password)

        output = ""
        stdin, stdout, stderr = client.exec_command(com)
        stdout = stdout.readlines()
        client.close()

        # Spool it back (can be improved at later point)
        for line in stdout:
            output = output + line
        if output != "":
            return output

    def download_reports(self):
        dl_folder = self.args[0]
        reportfile = self.args[1]
        reportname = self.args[2]
        resultsname = self.args[3]
        transport = paramiko.Transport((self.hostname, 22))
        transport.connect(username=self.user, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Download the reportfile (html) and the results (xml)
        print 'Downloading \"{0}\"...'.format(reportname)
        sftp.get(reportfile, ('{0}/{1}'.format(dl_folder, reportname)))
        print 'Downloading \"{0}\"...'.format(resultsname)
        sftp.get(reportfile, ('{0}/{1}'.format(dl_folder, resultsname)))
        sftp.close()
        transport.close()
