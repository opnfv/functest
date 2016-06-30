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
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_clean as os_clean
import functest.utils.openstack_snapshot as os_snapshot
import yaml


with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)

REPOS_DIR = os.getenv('repos_dir')
FUNCTEST_REPO = ("%s/functest/" % REPOS_DIR)
FUNCTEST_CONF_DIR = functest_yaml.get("general").get(
    "directories").get("dir_functest_conf")
RC_FILE = os.getenv('creds')
OS_SNAPSHOT_FILE = ft_utils.get_parameter_from_yaml(
    "general.openstack.snapshot_file")


class CliOpenStack:

    def __init__(self):
        self.os_auth_url = os.getenv('OS_AUTH_URL')
        self.endpoint_ip = None
        self.endpoint_port = None
        if self.os_auth_url is not None:
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

    def show_credentials(self):
        cmd = "env|grep OS_"
        ft_utils.execute_command(cmd, exit_on_error=False, verbose=False)
        click.echo("")

    def fetch_credentials(self):
        if os.path.isfile(RC_FILE):
            answer = raw_input("It seems the RC file is already present. "
                               "Do you want to overwrite it? [y|n]\n")
            while True:
                if answer.lower() in ["y", "yes"]:
                    break
                elif answer.lower() in ["n", "no"]:
                    return
                else:
                    answer = raw_input("Invalid answer. Please type [y|n]\n")

        CI_INSTALLER_TYPE = os.getenv('INSTALLER_TYPE')
        if CI_INSTALLER_TYPE is None:
            click.echo("The environment variable 'INSTALLER_TYPE' is not"
                       "defined. Please export it")
        CI_INSTALLER_IP = os.getenv('INSTALLER_IP')
        if CI_INSTALLER_IP is None:
            click.echo("The environment variable 'INSTALLER_IP' is not"
                       "defined. Please export it")
        cmd = ("/home/opnfv/repos/releng/utils/fetch_os_creds.sh "
               "-d %s -i %s -a %s"
               % (RC_FILE, CI_INSTALLER_TYPE, CI_INSTALLER_IP))
        click.echo("Fetching credentials from installer node '%s' with IP=%s.."
                   % (CI_INSTALLER_TYPE, CI_INSTALLER_IP))
        ft_utils.execute_command(cmd, verbose=False)

    def check(self):
        self.ping_endpoint()
        cmd = FUNCTEST_REPO + "ci/check_os.sh"
        ft_utils.execute_command(cmd, verbose=False)

    def snapshot_create(self):
        self.ping_endpoint()
        if os.path.isfile(OS_SNAPSHOT_FILE):
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
        if not os.path.isfile(OS_SNAPSHOT_FILE):
            click.echo("There is no OpenStack snapshot created. To create "
                       "one run the command 'functest env os-create-snapshot'")
            return
        with open(OS_SNAPSHOT_FILE, 'r') as yaml_file:
            click.echo("\n%s"
                       % yaml_file.read())

    def clean(self):
        self.ping_endpoint()
        if not os.path.isfile(OS_SNAPSHOT_FILE):
            click.echo("Not possible to clean OpenStack without a snapshot. "
                       "This could cause problems. "
                       "Run first the command 'os-create-shapshot'.")
            return
        os_clean.main()
