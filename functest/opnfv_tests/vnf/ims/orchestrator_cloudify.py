#!/usr/bin/python
# coding: utf8
#######################################################################
#
#   Copyright (c) 2015 Orange
#   valentin.boucher@orange.com
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
########################################################################

import logging
import os
import shutil
import subprocess32 as subprocess
import yaml

from git import Repo


class Orchestrator(object):

    def __init__(self, testcase_dir, inputs={}):
        self.testcase_dir = testcase_dir
        self.blueprint_dir = testcase_dir + 'cloudify-manager-blueprint/'
        self.input_file = 'inputs.yaml'
        self.manager_blueprint = False
        self.config = inputs
        self.logger = logging.getLogger(__name__)
        self.manager_up = False

    def set_credentials(self, username, password, tenant_name, auth_url):
        self.config['keystone_username'] = username
        self.config['keystone_password'] = password
        self.config['keystone_url'] = auth_url
        self.config['keystone_tenant_name'] = tenant_name

    def set_flavor_id(self, flavor_id):
        self.config['flavor_id'] = flavor_id

    def set_image_id(self, image_id):
        self.config['image_id'] = image_id

    def set_external_network_name(self, external_network_name):
        self.config['external_network_name'] = external_network_name

    def set_ssh_user(self, ssh_user):
        self.config['ssh_user'] = ssh_user

    def set_nova_url(self, nova_url):
        self.config['nova_url'] = nova_url

    def set_neutron_url(self, neutron_url):
        self.config['neutron_url'] = neutron_url

    def set_nameservers(self, nameservers):
        if 0 < len(nameservers):
            self.config['dns_subnet_1'] = nameservers[0]

    def download_manager_blueprint(self, manager_blueprint_url,
                                   manager_blueprint_branch):
        if self.manager_blueprint:
            self.logger.info(
                "cloudify manager server blueprint is "
                "already downloaded !")
        else:
            self.logger.info(
                "Downloading the cloudify manager server blueprint")
            download_result = self._download_blueprints(
                manager_blueprint_url,
                manager_blueprint_branch,
                self.blueprint_dir)

            if not download_result:
                self.logger.error("Failed to download manager blueprint")
                exit(-1)
            else:
                self.manager_blueprint = True

    def manager_up(self):
        return self.manager_up

    def deploy_manager(self):
        if self.manager_blueprint:
            self.logger.info("Writing the inputs file")
            with open(self.blueprint_dir + "inputs.yaml", "w") as f:
                f.write(yaml.dump(self.config, default_style='"'))
            f.close()

            # Ensure no ssh key file already exists
            key_files = ["/.ssh/cloudify-manager-kp.pem",
                         "/.ssh/cloudify-agent-kp.pem"]
            home = os.path.expanduser("~")

            for key_file in key_files:
                if os.path.isfile(home + key_file):
                    os.remove(home + key_file)

            self.logger.info("Launching the cloudify-manager deployment")
            script = "set -e; "
            script += ("source " + self.testcase_dir +
                       "venv_cloudify/bin/activate; ")
            script += "cd " + self.testcase_dir + "; "
            script += "cfy init -r; "
            script += "cd cloudify-manager-blueprint; "
            script += ("cfy local create-requirements -o requirements.txt " +
                       "-p openstack-manager-blueprint.yaml; ")
            script += "pip install -r requirements.txt; "
            script += ("cfy bootstrap --install-plugins " +
                       "-p openstack-manager-blueprint.yaml -i inputs.yaml; ")
            cmd = "/bin/bash -c '" + script + "'"
            error = execute_command(cmd, self.logger)
            if error:
                self.logger.error("Failed to deploy cloudify-manager")
                return error

            self.logger.info("Cloudify-manager server is UP !")

            self.manager_up = True

    def undeploy_manager(self):
        self.logger.info("Launching the cloudify-manager undeployment")

        self.manager_up = False

        script = "source " + self.testcase_dir + "venv_cloudify/bin/activate; "
        script += "cd " + self.testcase_dir + "; "
        script += "cfy teardown -f --ignore-deployments; "
        cmd = "/bin/bash -c '" + script + "'"
        execute_command(cmd, self.logger)

        self.logger.info(
            "Cloudify-manager server has been successfully removed!")

    def download_upload_and_deploy_blueprint(self, blueprint, config,
                                             bp_name, dep_name):
        self.logger.info("Downloading the {0} blueprint".format(
            blueprint['file_name']))
        destination_folder = os.path.join(self.testcase_dir,
                                          blueprint['destination_folder'])
        download_result = self._download_blueprints(blueprint['url'],
                                                    blueprint['branch'],
                                                    destination_folder)

        if not download_result:
            self.logger.error(
                "Failed to download blueprint {0}".
                format(blueprint['file_name']))
            exit(-1)

        self.logger.info("Writing the inputs file")

        with open(self.testcase_dir + blueprint['destination_folder'] +
                  "/inputs.yaml", "w") as f:
            f.write(yaml.dump(config, default_style='"'))
        f.close()

        self.logger.info("Launching the {0} deployment".format(bp_name))
        script = "source " + self.testcase_dir + "venv_cloudify/bin/activate; "
        script += ("cd " + self.testcase_dir +
                   blueprint['destination_folder'] + "; ")
        script += ("cfy blueprints upload -b " +
                   bp_name + " -p openstack-blueprint.yaml; ")
        script += ("cfy deployments create -b " + bp_name +
                   " -d " + dep_name + " --inputs inputs.yaml; ")
        script += ("cfy executions start -w install -d " +
                   dep_name + " --timeout 1800; ")

        cmd = "/bin/bash -c '" + script + "'"
        error = execute_command(cmd, self.logger, 2000)
        if error:
            self.logger.error("Failed to deploy blueprint")
            return error
        self.logger.info("The deployment of {0} is ended".format(dep_name))

    def undeploy_deployment(self, dep_name):
        self.logger.info("Launching the {0} undeployment".format(dep_name))
        script = "source " + self.testcase_dir + "venv_cloudify/bin/activate; "
        script += "cd " + self.testcase_dir + "; "
        script += ("cfy executions start -w uninstall -d " + dep_name +
                   " --timeout 1800 ; ")
        script += "cfy deployments delete -d " + dep_name + "; "

        cmd = "/bin/bash -c '" + script + "'"
        try:
            execute_command(cmd, self.logger)
        except:
            self.logger.error("Clearwater undeployment failed")

    def _download_blueprints(self, blueprint_url, branch, dest_path):
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        try:
            Repo.clone_from(blueprint_url, dest_path, branch=branch)
            return True
        except:
            return False


def execute_command(cmd, logger, timeout=1800):
    """
    Execute Linux command
    """
    if logger:
        logger.debug('Executing command : {}'.format(cmd))
    timeout_exception = False
    output_file = "output.txt"
    f = open(output_file, 'w+')
    try:
        p = subprocess.call(cmd, shell=True, stdout=f,
                            stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired:
        timeout_exception = True
        if logger:
            logger.error("TIMEOUT when executing command %s" % cmd)
        pass

    f.close()
    f = open(output_file, 'r')
    result = f.read()
    if result != "" and logger:
        logger.debug(result)
    if p == 0:
        return False
    else:
        if logger and not timeout_exception:
            logger.error("Error when executing command %s" % cmd)
        f = open(output_file, 'r')
        lines = f.readlines()
        return lines[-5:]
