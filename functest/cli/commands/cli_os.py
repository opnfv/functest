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
import six
from six.moves.urllib.parse import urlparse

from functest.ci import check_deployment
from functest.utils.constants import CONST
import functest.utils.openstack_clean as os_clean
import functest.utils.openstack_snapshot as os_snapshot


class OpenStack(object):

    def __init__(self):
        self.os_auth_url = CONST.__getattribute__('OS_AUTH_URL')
        self.endpoint_ip = None
        self.endpoint_port = None
        self.openstack_creds = CONST.__getattribute__('openstack_creds')
        self.snapshot_file = CONST.__getattribute__('openstack_snapshot_file')
        if self.os_auth_url:
            self.endpoint_ip = urlparse(self.os_auth_url).hostname
            self.endpoint_port = urlparse(self.os_auth_url).port

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
        dic_credentials = {}
        for key, value in os.environ.items():
            if key.startswith('OS_'):
                dic_credentials.update({key: value})
        return dic_credentials

    def check(self):
        self.ping_endpoint()
        deployment = check_deployment.CheckDeployment()
        deployment.check_all()

    def snapshot_create(self):
        self.ping_endpoint()
        if os.path.isfile(self.snapshot_file):
            answer = six.moves.input(
                "It seems there is already an OpenStack "
                "snapshot. Do you want to overwrite it with "
                "the current OpenStack status? [y|n]\n")
            while True:
                if answer.lower() in ["y", "yes"]:
                    break
                elif answer.lower() in ["n", "no"]:
                    return
                else:
                    answer = six.moves.input(
                        "Invalid answer. Please type [y|n]\n")

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


class CliOpenStack(OpenStack):

    def __init__(self):
        super(CliOpenStack, self).__init__()

    @staticmethod
    def show_credentials():
        dic_credentials = OpenStack.show_credentials()
        for key, value in dic_credentials.items():
                if key.startswith('OS_'):
                    click.echo("{}={}".format(key, value))
