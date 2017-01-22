#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#


import os

import click

from functest.utils.constants import CONST
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_clean as os_clean
import functest.utils.openstack_snapshot as os_snapshot


class CliOpenStack(object):

    def __init__(self):
        self.os_auth_url = CONST.OS_AUTH_URL
        self.endpoint_ip = None
        self.endpoint_port = None
        self.openstack_creds = CONST.openstack_creds
        self.snapshot_file = CONST.openstack_snapshot_file
        if self.os_auth_url:
            self.endpoint_ip = self.os_auth_url.rsplit("/")[2].rsplit(":")[0]
            self.endpoint_port = self.os_auth_url.rsplit("/")[2].rsplit(":")[1]

    def ping_endpoint(self):
        if self.os_auth_url is None:
            click.echo("Source the OpenStack credentials first '. $creds'")
            exit(0)
        response = os.system("ping -c 1 " + self.endpoint_ip + ">/dev/null")
        if response == 0:
            return 0
        else:
            click.echo("Cannot talk to the endpoint %s\n" % self.endpoint_ip)
            exit(0)

    @staticmethod
    def show_credentials():
        for key, value in os.environ.items():
            if key.startswith('OS_'):
                click.echo("{}={}".format(key, value))

    def fetch_credentials(self):
        if os.path.isfile(self.openstack_creds):
            answer = raw_input("It seems the RC file is already present. "
                               "Do you want to overwrite it? [y|n]\n")
            while True:
                if answer.lower() in ["y", "yes"]:
                    break
                elif answer.lower() in ["n", "no"]:
                    return
                else:
                    answer = raw_input("Invalid answer. Please type [y|n]\n")

        installer_type = CONST.INSTALLER_TYPE
        if installer_type is None:
            click.echo("The environment variable 'INSTALLER_TYPE' is not"
                       "defined. Please export it")
        installer_ip = CONST.INSTALLER_IP
        if installer_ip is None:
            click.echo("The environment variable 'INSTALLER_IP' is not"
                       "defined. Please export it")
        cmd = ("%s/releng/utils/fetch_os_creds.sh -d %s -i %s -a %s"
               % (CONST.dir_repos,
                  self.openstack_creds,
                  installer_type,
                  installer_ip))
        click.echo("Fetching credentials from installer node '%s' with IP=%s.."
                   % (installer_type, installer_ip))
        ft_utils.execute_command(cmd, verbose=False)

    def check(self):
        self.ping_endpoint()
        cmd = CONST.dir_repo_functest + "/functest/ci/check_os.sh"
        ft_utils.execute_command(cmd, verbose=False)

    def snapshot_create(self):
        self.ping_endpoint()
        if os.path.isfile(self.snapshot_file):
            answer = raw_input("It seems there is already an OpenStack "
                               "snapshot. Do you want to overwrite it with "
                               "the current OpenStack status? [y|n]\n")
            while True:
                if answer.lower() in ["y", "yes"]:
                    break
                elif answer.lower() in ["n", "no"]:
                    return
                else:
                    answer = raw_input("Invalid answer. Please type [y|n]\n")

        click.echo("Generating Openstack snapshot...")
        os_snapshot.main()

    def snapshot_show(self):
        if not os.path.isfile(self.snapshot_file):
            click.echo("There is no OpenStack snapshot created. To create "
                       "one run the command "
                       "'functest openstack snapshot-create'")
            return
        with open(self.snapshot_file, 'r') as yaml_file:
            click.echo("\n%s"
                       % yaml_file.read())

    def clean(self):
        self.ping_endpoint()
        if not os.path.isfile(self.snapshot_file):
            click.echo("Not possible to clean OpenStack without a snapshot. "
                       "This could cause problems. "
                       "Run first the command "
                       "'functest openstack snapshot-create'")
            return
        os_clean.main()
