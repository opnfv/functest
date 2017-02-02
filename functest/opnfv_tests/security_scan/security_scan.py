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
# 0.1: This script installs OpenSCAP on the remote host, and scans the
# nominated node. Post scan a report is downloaded and if '--clean' is passed
# all trace of the scan is removed from the remote system.


import datetime
import os
import sys
from ConfigParser import SafeConfigParser

import argparse
from keystoneclient import session
from keystoneclient.auth.identity import v2
from novaclient import client

import connect
import functest.utils.functest_constants as ft_constants

__version__ = 0.1
__author__ = 'Luke Hinds (lhinds@redhat.com)'
__url__ = 'https://wiki.opnfv.org/display/functest/Functest+Security'

# Global vars
INSTALLER_IP = ft_constants.CI_INSTALLER_IP
oscapbin = 'sudo /bin/oscap'
functest_dir = '%s/security_scan/' % ft_constants.FUNCTEST_TEST_DIR


class SecurityScanParser():

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='OPNFV OpenSCAP'
                                                          ' Scanner')
        self.parser.add_argument('--config', action='store', dest='cfgfile',
                                 help='Config file', required=True)

    def parse_args(self, argv=[]):
        return vars(self.parser.parse_args(argv))


class GlobalVariables:
    tmpdir = ""


def run_tests(host, nodetype, cfgparse, localkey):
    user = cfgparse.get(nodetype, 'user')
    port = cfgparse.get(nodetype, 'port')
    connect.logger.info("Host: {0} Selected Profile: {1}".format(host,
                                                                 nodetype))
    connect.logger.info("Checking internet for package installation...")
    if internet_check(host, nodetype, cfgparse, localkey):
        connect.logger.info("Internet Connection OK.")
        connect.logger.info("Creating temp file structure..")
        createfiles(host, port, user, localkey)
        connect.logger.debug("Installing OpenSCAP...")
        install_pkg(host, port, user, localkey)
        connect.logger.debug("Running scan...")
        run_scanner(host, port, user, localkey, nodetype, cfgparse)
        clean = cfgparse.get(nodetype, 'clean')
        connect.logger.info("Post installation tasks....")
        post_tasks(host, port, user, localkey, nodetype, cfgparse)
        if clean:
            connect.logger.info("Cleaning down environment....")
            connect.logger.debug("Removing OpenSCAP....")
            removepkg(host, port, user, localkey, nodetype)
            connect.logger.info("Deleting tmp file and reports (remote)...")
            cleandir(host, port, user, localkey, nodetype)
    else:
        connect.logger.error("Internet timeout. Moving on to next node..")
        pass


def nova_iterate(nova, cfgparse, localkey):
    # Find compute nodes, active with network on ctlplane
    for server in nova.servers.list():
        if server.status == 'ACTIVE' and 'compute' in server.name:
            networks = server.networks
            nodetype = 'compute'
            for host in networks['ctlplane']:
                run_tests(host, nodetype, cfgparse, localkey)
        # Find controller nodes, active with network on ctlplane
        elif server.status == 'ACTIVE' and 'controller' in server.name:
            networks = server.networks
            nodetype = 'controller'
            for host in networks['ctlplane']:
                run_tests(host, nodetype, cfgparse, localkey)


def internet_check(host, nodetype, cfgparse, localkey):
    import connect
    user = cfgparse.get(nodetype, 'user')
    port = cfgparse.get(nodetype, 'port')
    localpath = functest_dir + 'scripts/internet_check.py'
    remotepath = '/tmp/internet_check.py'
    com = 'python /tmp/internet_check.py'
    testconnect = connect.ConnectionManager(host, port, user, localkey,
                                            localpath, remotepath, com)
    connectionresult = testconnect.remotescript()
    if connectionresult.rstrip() == 'True':
        return True
    else:
        return False


def createfiles(host, port, user, localkey):
    import connect
    localpath = functest_dir + 'scripts/createfiles.py'
    remotepath = '/tmp/createfiles.py'
    com = 'python /tmp/createfiles.py'
    connect = connect.ConnectionManager(host, port, user, localkey,
                                        localpath, remotepath, com)
    GlobalVariables.tmpdir = connect.remotescript()


def install_pkg(host, port, user, localkey):
    import connect
    com = 'sudo yum -y install openscap-scanner scap-security-guide'
    connect = connect.ConnectionManager(host, port, user, localkey, com)
    connect.remotecmd()


def run_scanner(host, port, user, localkey, nodetype, cfgparse):
    import connect
    scantype = cfgparse.get(nodetype, 'scantype')
    profile = cfgparse.get(nodetype, 'profile')
    results = cfgparse.get(nodetype, 'results')
    report = cfgparse.get(nodetype, 'report')
    secpolicy = cfgparse.get(nodetype, 'secpolicy')
    # Here is where we contruct the actual scan command
    if scantype == 'xccdf':
        cpe = cfgparse.get(nodetype, 'cpe')
        com = '{0} xccdf eval --profile {1} --results {2}/{3}' \
              ' --report {2}/{4}' \
              ' --cpe {5} {6}'.format(oscapbin,
                                      profile,
                                      GlobalVariables.tmpdir.rstrip(),
                                      results,
                                      report,
                                      cpe,
                                      secpolicy)
        connect = connect.ConnectionManager(host, port, user, localkey, com)
        connect.remotecmd()
    elif scantype == 'oval':
        com = '{0} oval eval --results {1}/{2} '
        '--report {1}/{3} {4}'.format(oscapbin,
                                      GlobalVariables.tmpdir.rstrip(),
                                      results, report, secpolicy)
        connect = connect.ConnectionManager(host, port, user, localkey, com)
        connect.remotecmd()
    else:
        com = '{0} oval-collect '.format(oscapbin)
        connect = connect.ConnectionManager(host, port, user, localkey, com)
        connect.remotecmd()


def post_tasks(host, port, user, localkey, nodetype, cfgparse):
    import connect
    # Create the download folder for functest dashboard and download reports
    reports_dir = cfgparse.get(nodetype, 'reports_dir')
    dl_folder = os.path.join(reports_dir, host + "_" +
                             datetime.datetime.
                             now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.makedirs(dl_folder, 0755)
    report = cfgparse.get(nodetype, 'report')
    results = cfgparse.get(nodetype, 'results')
    reportfile = '{0}/{1}'.format(GlobalVariables.tmpdir.rstrip(), report)
    connect = connect.ConnectionManager(host, port, user, localkey, dl_folder,
                                        reportfile, report, results)
    connect.download_reports()


def removepkg(host, port, user, localkey, nodetype):
    import connect
    com = 'sudo yum -y remove openscap-scanner scap-security-guide'
    connect = connect.ConnectionManager(host, port, user, localkey, com)
    connect.remotecmd()


def cleandir(host, port, user, localkey, nodetype):
    import connect
    com = 'sudo rm -r {0}'.format(GlobalVariables.tmpdir.rstrip())
    connect = connect.ConnectionManager(host, port, user, localkey, com)
    connect.remotecmd()


if __name__ == '__main__':
    # Apex Spefic var needed to query Undercloud
    if ft_constants.OS_AUTH_URL is None:
        connect.logger.error(" Enviroment variable OS_AUTH_URL is not set")
        sys.exit(0)
    else:
        OS_AUTH_URL = ft_constants.OS_AUTH_URL

    parser = SecurityScanParser()
    args = parser.parse_args(sys.argv[1:])

    # Config Parser
    cfgparse = SafeConfigParser()
    cfgparse.read(args.cfgfile)

    #  Grab Undercloud key
    remotekey = cfgparse.get('undercloud', 'remotekey')
    localkey = cfgparse.get('undercloud', 'localkey')
    setup = connect.SetUp(remotekey, localkey)
    setup.getockey()

    # Configure Nova Credentials
    com = 'sudo /usr/bin/hiera admin_password'
    setup = connect.SetUp(com)
    keypass = setup.keystonepass()
    auth = v2.Password(auth_url=OS_AUTH_URL,
                       username='admin',
                       password=str(keypass).rstrip(),
                       tenant_name='admin')
    sess = session.Session(auth=auth)
    nova = client.Client(2, session=sess)

    nova_iterate(nova, cfgparse, localkey)
