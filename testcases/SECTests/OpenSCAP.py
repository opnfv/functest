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

import os
import datetime
import argparse

__version__ = 0.1
__author__ = 'Luke Hinds (lhinds@redhat.com)'
__url__ = 'https://wiki.opnfv.org/display/functest/Functest+Security'

'''
Example Run:
    python ./OpenSCAP.py --host 192.168.0.24 --port 22 --user root --password
    p6ssw0rd oval --secpolicy
    /usr/share/xml/scap/ssg/content/ssg-rhel7-oval.xml --report report.html
    --results results.xml

'''

# Variables needed..
pwd = os.getcwd()
oscap = '/bin/oscap'
currenttime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Set up the main parser
parser = argparse.ArgumentParser(description='OpenSCAP Python Scanner')

# Main args
# Todo  add required = True
parser.add_argument('--user',
                    action='store',
                    dest='user',
                    help='user')
parser.add_argument('--password',
                    action='store',
                    dest='password',
                    help='Password')
parser.add_argument('--host',
                    action='store',
                    dest='host',
                    help='host',
                    required=True)
parser.add_argument('--port',
                    action='store',
                    dest='port"',
                    help='port',
                    required=True)
parser.add_argument('--dist',
                    action='store',
                    dest='dist',
                    help='Distribution')
parser.add_argument('--clean',
                    action='store_true',
                    dest='clean',
                    help='Clean all files from host')

# And the subparser
subparsers = parser.add_subparsers(
    title='subcommands',
    description='valid subcommands',
    help='additional help')


parser_xccdf = subparsers.add_parser('xccdf')
parser_xccdf.set_defaults(which='xccdf')

parser_oval = subparsers.add_parser('oval')
parser_oval.set_defaults(which='oval')

parser_oval_collect = subparsers.add_parser('oval-collect')
parser_oval_collect.set_defaults(which='oval-collect')

parser_xccdf.add_argument(
    '--profile',
    action='store',
    dest='profile',
    help='xccdf profile')

parser_oval.add_argument(
    '--results',
    action='store',
    dest='results',
    help='Report name (inc extension (.html)')

parser_oval.add_argument(
    '--report',
    action='store',
    dest='report',
    help='Report name (inc extension (.html)')

parser_oval.add_argument(
    '--secpolicy',
    action='store',
    dest='secpolicy',
    help='Security Policy')

parserout = parser.parse_args()
args = vars(parser.parse_args())


def createfiles():
    import connect
    global tmpdir
    localpath = os.getcwd() + '/scripts/createfiles.py'
    remotepath = '/tmp/createfiles.py'
    com = 'python /tmp/createfiles.py'
    connect = connect.connectionManager(parserout.host,
                                        parserout.user,
                                        parserout.password,
                                        localpath,
                                        remotepath,
                                        com)
    tmpdir = connect.remotescript()


def install_pkg():
    import connect
    com = 'yum -y install openscap-scanner scap-security-guide'
    connect = connect.connectionManager(parserout.host,
                                        parserout.user,
                                        parserout.password,
                                        com)
    install_pkg = connect.remotecmd()
    print install_pkg


def run_scanner():
    import connect

    if args['which'] == 'xccdf':
        print 'xccdf'
        com = '{0} xccdf eval'.format(oscap)
        connect = connect.connectionManager(parserout.host,
                                            parserout.user,
                                            parserout.password,
                                            com)
    elif args['which'] == 'oval':
        com = ('{0} oval eval --results {1}/{2}' +
               ' --report {1}/{3} {4}'.format(oscap,
                                              tmpdir.rstrip(),
                                              parserout.results,
                                              parserout.report,
                                              parserout.secpolicy))
        connect = connect.connectionManager(parserout.host,
                                            parserout.user,
                                            parserout.password,
                                            com)
        run_tool = connect.remotecmd()
    else:
        com = '{0} oval-collect '.format(oscap)
        connect = connect.connectionManager(parserout.host,
                                            parserout.user,
                                            parserout.password,
                                            com)
        run_tool = connect.remotecmd()
        print run_tool


def post_tasks():
    import connect
    dl_folder = os.path.join(os.getcwd(), parserout.host +
                             datetime.datetime.now().
                             strftime('%Y-%m-%d_%H-%M-%S'))
    os.mkdir(dl_folder, 0755)
    reportfile = '{0}/{1}'.format(tmpdir.rstrip(), parserout.report)
    connect = connect.connectionManager(parserout.host,
                                        parserout.user,
                                        parserout.password,
                                        dl_folder,
                                        reportfile,
                                        parserout.report,
                                        parserout.results)
    run_tool = connect.download_reports()
    print run_tool


def removepkg():
    import connect
    com = 'yum -y remove openscap-scanner scap-security-guide'
    connect = connect.connectionManager(parserout.host,
                                        parserout.user,
                                        parserout.password,
                                        com)
    yumremove = connect.remotecmd()
    print yumremove


def cleandir():
    import connect
    com = 'rm -r {0}'.format(tmpdir.rstrip())
    connect = connect.connectionManager(parserout.host,
                                        parserout.user,
                                        parserout.password,
                                        com)
    deldir = connect.remotecmd()
    print deldir


if __name__ == '__main__':
    print 'Creating temp file structure...\n'
    createfiles()
    print 'Install OpenSCAP scanner...\n'
    install_pkg()
    print 'Running scan...\n'
    run_scanner()
    print 'Post installation tasks...\n'
    post_tasks()
    if parserout.clean:
        print 'Cleaning down environment...\n'
        print 'Removing OpenSCAP...\n'
        removepkg()
        print 'Deleting tmp file and reports (remote)...\n'
        cleandir()
