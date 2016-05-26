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

import argparse
import connect
import datetime
import os

from ConfigParser import SafeConfigParser
from keystoneclient.auth.identity import v2
from keystoneclient import session
from novaclient import client

__version__ = 0.1
__author__ = 'Luke Hinds (lhinds@redhat.com)'
__url__ = 'https://wiki.opnfv.org/display/functest/Functest+Security'

# Global vars
INSTALLER_IP = os.getenv('INSTALLER_IP')
oscapbin = 'sudo /bin/oscap'

# Configure Nova Credentials
com = 'sudo hiera admin_password'
connect = connect.novaManager(com)
keypass = connect.keystonepass()
auth = v2.Password(auth_url='http://{0}:5000/v2.0'.format(INSTALLER_IP),
                   username='admin',
                   password=str(keypass).rstrip(),
                   tenant_name='admin')
sess = session.Session(auth=auth)
nova = client.Client(2, session=sess)


# args
parser = argparse.ArgumentParser(description='OPNFV OpenSCAP Scanner')
parser.add_argument('--config', action='store', dest='cfgfile',
                    help='Config file', required=True)
args = parser.parse_args()

# functest logger
logger = ft_logger.Logger("security_scan").getLogger()

# Config Parser
cfgparse = SafeConfigParser()
cfgparse.read(args.cfgfile)


def run_tests(host, nodetype):
    port = cfgparse.get(nodetype, 'port')
    user = cfgparse.get(nodetype, 'user')
    user_key = cfgparse.get(nodetype, 'user_key')
    print ("Host: {0} Selected Profile: {1}.\n").format(host, nodetype)
    logger.info("Host: {0} Selected Profile: {1}").format(host, nodetype)
    print 'Creating temp file structure...\n'
    logger.info("Creating temp file structure..")
    createfiles(host, port, user, user_key)
    print 'Installing OpenSCAP...\n'
    logger.info("Installing OpenSCAP...")
    install_pkg(host, port, user, user_key)
    print 'Running scan...\n'
    logger.info("Running scan...")
    run_scanner(host, port, user, user_key, nodetype)
    clean = cfgparse.get(nodetype, 'clean')
    print 'Post installation tasks...\n'
    logger.info("Post installation tasks....")
    post_tasks(host, port, user, user_key, nodetype)
    if clean:
        print 'Cleaning down environment...\n'
        logger.info("Cleaning down environment....")
        print 'Removing OpenSCAP...\n'
        logger.info("Removing OpenSCAP....")
        removepkg(host, port, user, user_key, nodetype)
        print 'Deleting tmp file and reports (remote)..\n'
        logger.info("Deleting tmp file and reports (remote)...")
        cleandir(host, port, user, user_key, nodetype)


def nova_iterate():
    # Find compute nodes, active with network on ctlplane
    for server in nova.servers.list():
        if server.status == 'ACTIVE' and 'compute' in server.name:
            networks = server.networks
            nodetype = 'compute'
            for host in networks['ctlplane']:
                run_tests(host, nodetype)
        # Find controller nodes, active with network on ctlplane
        elif server.status == 'ACTIVE' and 'controller' in server.name:
            networks = server.networks
            nodetype = 'controller'
            for host in networks['ctlplane']:
                run_tests(host, nodetype)


def createfiles(host, port, user, user_key):
    import connect
    global tmpdir
    localpath = os.getcwd() + '/scripts/createfiles.py'
    remotepath = '/tmp/createfiles.py'
    com = 'python /tmp/createfiles.py'
    connect = connect.connectionManager(host, port, user, user_key,
                                        localpath, remotepath, com)
    tmpdir = connect.remotescript()


def install_pkg(host, port, user, user_key):
    import connect
    com = 'sudo yum -y install openscap-scanner scap-security-guide'
    connect = connect.connectionManager(host, port, user, user_key, com)
    # install_pkg = connect.remotecmd()  # install_pkg is never used
    connect.remotecmd()


def run_scanner(host, port, user, user_key, nodetype):
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
              ' --report {2}/{4} --cpe {5} {6}'.format(oscapbin,
                                                       profile,
                                                       tmpdir.rstrip(),
                                                       results,
                                                       report,
                                                       cpe,
                                                       secpolicy)
        connect = connect.connectionManager(host, port, user, user_key, com)
        # run_tool = connect.remotecmd()
        connect.remotecmd()
    elif scantype == 'oval':
        com = '{0} oval eval --results {1}/{2} '
        '--report {1}/{3} {4}'.format(oscapbin, tmpdir.rstrip(),
                                      results, report, secpolicy)
        connect = connect.connectionManager(host, port, user, user_key, com)
        # run_tool = connect.remotecmd()
        connect.remotecmd()
    else:
        com = '{0} oval-collect '.format(oscap)
        connect = connect.connectionManager(host, port, user, user_key, com)
        # run_tool = connect.remotecmd()
        connect.remotecmd()


def post_tasks(host, port, user, user_key, nodetype):
    import connect
    # Create the download folder for functest dashboard and download reports
    reports_dir = cfgparse.get(nodetype, 'reports_dir')
    dl_folder = os.path.join(reports_dir, host + "_" +
                             datetime.datetime.
                             now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.makesdir(dl_folder, 0755)
    report = cfgparse.get(nodetype, 'report')
    results = cfgparse.get(nodetype, 'results')
    reportfile = '{0}/{1}'.format(tmpdir.rstrip(), report)
    connect = connect.connectionManager(host, port, user, user_key, dl_folder,
                                        reportfile, report, results)
    # run_tool = connect.download_reports()
    connect.download_reports()


def removepkg(host, port, user, user_key, nodetype):
    import connect
    com = 'sudo yum -y remove openscap-scanner scap-security-guide'
    connect = connect.connectionManager(host, port, user, user_key, com)
    # yumremove = connect.remotecmd()
    connect.remotecmd()


def cleandir(host, port, user, user_key, nodetype):
    import connect
    com = 'sudo rm -r {0}'.format(tmpdir.rstrip())
    connect = connect.connectionManager(host, port, user, user_key, com)
    # deldir = connect.remotecmd()
    connect.remotecmd()


if __name__ == '__main__':
    nova_iterate()
