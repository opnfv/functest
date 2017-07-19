#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import argparse
import enum
import json
import fileinput
import logging
import logging.config
import os
import pkg_resources
import re
import subprocess
import sys

import yaml

from functest.ci import check_deployment
from functest.utils import functest_utils as ft_utils
from functest.utils import openstack_utils as os_utils
from functest.utils.constants import CONST

from opnfv.utils import constants as opnfv_constants

""" logging configuration """
logger = logging.getLogger('functest.ci.prepare_env')


POD_ARCH = os.getenv("HOST_ARCH", None)
ARCH_FILTER = ['aarch64']
ACTIONS = ['start', 'check']
CONFIG_FUNCTEST_PATH = pkg_resources.resource_filename(
            'functest', 'ci/config_functest.yaml')
CONFIG_PATCH_PATH = pkg_resources.resource_filename(
            'functest', 'ci/config_patch.yaml')
CONFIG_AARCH64_PATCH_PATH = pkg_resources.resource_filename(
            'functest', 'ci/config_aarch64_patch.yaml')
RALLY_CONF_PATH = "/etc/rally/rally.conf"
RALLY_AARCH64_PATCH_PATH = pkg_resources.resource_filename(
            'functest', 'ci/rally_aarch64_patch.conf')


class Result(enum.Enum):
    EX_OK = os.EX_OK
    EX_ERROR = -1


class PrepareEnvParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("action", help="Possible actions are: "
                                 "'{d[0]}|{d[1]}' ".format(d=ACTIONS),
                                 choices=ACTIONS)

    def parse_args(self, argv=[]):
        return vars(self.parser.parse_args(argv))


def print_separator():
    logger.info("==============================================")


class Environment(object):

    def __init__(self):
        pass

    @staticmethod
    def check_env_variables():
        print_separator()
        logger.info("Checking environment variables...")

        if CONST.__getattribute__('INSTALLER_TYPE') is None:
            logger.warning("The env variable 'INSTALLER_TYPE' is not defined.")
            CONST.__setattr__('INSTALLER_TYPE', 'undefined')
        else:
            if (CONST.__getattribute__('INSTALLER_TYPE') not in
                    opnfv_constants.INSTALLERS):
                logger.warning("INSTALLER_TYPE=%s is not a valid OPNFV "
                               "installer. Available OPNFV Installers are : "
                               "%s. Setting INSTALLER_TYPE=undefined."
                               % (CONST.__getattribute__('INSTALLER_TYPE'),
                                  opnfv_constants.INSTALLERS))
                CONST.__setattr__('INSTALLER_TYPE', 'undefined')
            else:
                logger.info("    INSTALLER_TYPE=%s"
                            % CONST.__getattribute__('INSTALLER_TYPE'))

        if CONST.__getattribute__('INSTALLER_IP') is None:
            logger.warning(
                "The env variable 'INSTALLER_IP' is not defined. It is "
                "recommended to extract some information from the deployment")
        else:
            logger.info("    INSTALLER_IP=%s" %
                        CONST.__getattribute__('INSTALLER_IP'))

        if CONST.__getattribute__('DEPLOY_SCENARIO') is None:
            logger.warning("The env variable 'DEPLOY_SCENARIO' is not "
                           "defined. Setting CI_SCENARIO=undefined.")
            CONST.__setattr__('DEPLOY_SCENARIO', 'undefined')
        else:
            logger.info("    DEPLOY_SCENARIO=%s"
                        % CONST.__getattribute__('DEPLOY_SCENARIO'))
        if CONST.__getattribute__('CI_DEBUG'):
            logger.info("    CI_DEBUG=%s"
                        % CONST.__getattribute__('CI_DEBUG'))

        if CONST.__getattribute__('NODE_NAME'):
            logger.info("    NODE_NAME=%s"
                        % CONST.__getattribute__('NODE_NAME'))

        if CONST.__getattribute__('BUILD_TAG'):
            logger.info("    BUILD_TAG=%s"
                        % CONST.__getattribute__('BUILD_TAG'))

        if CONST.__getattribute__('IS_CI_RUN'):
            logger.info("    IS_CI_RUN=%s"
                        % CONST.__getattribute__('IS_CI_RUN'))

    @staticmethod
    def create_directories():
        print_separator()
        logger.info("Creating needed directories...")
        if not os.path.exists(CONST.__getattribute__('dir_functest_conf')):
            os.makedirs(CONST.__getattribute__('dir_functest_conf'))
            logger.info("    %s created." %
                        CONST.__getattribute__('dir_functest_conf'))
        else:
            logger.debug("   %s already exists." %
                         CONST.__getattribute__('dir_functest_conf'))

        if not os.path.exists(CONST.__getattribute__('dir_functest_data')):
            os.makedirs(CONST.__getattribute__('dir_functest_data'))
            logger.info("    %s created." %
                        CONST.__getattribute__('dir_functest_data'))
        else:
            logger.debug("   %s already exists." %
                         CONST.__getattribute__('dir_functest_data'))
        if not os.path.exists(CONST.__getattribute__('dir_functest_images')):
            os.makedirs(CONST.__getattribute__('dir_functest_images'))
            logger.info("    %s created." %
                        CONST.__getattribute__('dir_functest_images'))
        else:
            logger.debug("   %s already exists." %
                         CONST.__getattribute__('dir_functest_images'))

    @staticmethod
    def source_rc_file():
        print_separator()

        logger.info("Sourcing the OpenStack RC file...")
        os_utils.source_credentials(CONST.__getattribute__('openstack_creds'))
        for key, value in os.environ.iteritems():
            if re.search("OS_", key):
                if key == 'OS_AUTH_URL':
                    CONST.__setattr__('OS_AUTH_URL', value)
                elif key == 'OS_USERNAME':
                    CONST.__setattr__('OS_USERNAME', value)
                elif key == 'OS_TENANT_NAME':
                    CONST.__setattr__('OS_TENANT_NAME', value)
                elif key == 'OS_PASSWORD':
                    CONST.__setattr__('OS_PASSWORD', value)

    @staticmethod
    def update_config_file():
        Environment.patch_file(CONFIG_PATCH_PATH)

        if POD_ARCH and POD_ARCH in ARCH_FILTER:
            Environment.patch_file(CONFIG_AARCH64_PATCH_PATH)

        if "TEST_DB_URL" in os.environ:
            Environment.update_db_url()

    @staticmethod
    def patch_file(patch_file_path):
        logger.debug('Updating file: %s', patch_file_path)
        with open(patch_file_path) as f:
            patch_file = yaml.safe_load(f)

        updated = False
        for key in patch_file:
            if key in CONST.__getattribute__('DEPLOY_SCENARIO'):
                new_functest_yaml = dict(ft_utils.merge_dicts(
                    ft_utils.get_functest_yaml(), patch_file[key]))
                updated = True

        if updated:
            os.remove(CONFIG_FUNCTEST_PATH)
            with open(CONFIG_FUNCTEST_PATH, "w") as f:
                f.write(yaml.dump(new_functest_yaml, default_style='"'))

    @staticmethod
    def update_db_url():
        with open(CONFIG_FUNCTEST_PATH) as f:
            functest_yaml = yaml.safe_load(f)

        with open(CONFIG_FUNCTEST_PATH, "w") as f:
            functest_yaml["results"]["test_db_url"] = (
                os.environ.get('TEST_DB_URL'))
            f.write(yaml.dump(functest_yaml, default_style='"'))

    @staticmethod
    def verify_deployment():
        print_separator()
        logger.info("Verifying OpenStack deployment...")
        deployment = check_deployment.CheckDeployment()
        deployment.check_all()

    @staticmethod
    def install_rally():
        print_separator()

        if POD_ARCH and POD_ARCH in ARCH_FILTER:
            logger.info("Apply aarch64 specific to rally config...")
            with open(RALLY_AARCH64_PATCH_PATH, "r") as f:
                rally_patch_conf = f.read()

            for line in fileinput.input(RALLY_CONF_PATH, inplace=1):
                print line,
                if "cirros|testvm" in line:
                    print rally_patch_conf

        logger.info("Creating Rally environment...")

        cmd = "rally deployment destroy opnfv-rally"
        ft_utils.execute_command(cmd, error_msg=(
            "Deployment %s does not exist."
            % CONST.__getattribute__('rally_deployment_name')),
            verbose=False)

        rally_conf = os_utils.get_credentials_for_rally()
        with open('rally_conf.json', 'w') as fp:
            json.dump(rally_conf, fp)
        cmd = ("rally deployment create "
               "--file=rally_conf.json --name={0}"
               .format(CONST.__getattribute__('rally_deployment_name')))
        error_msg = "Problem while creating Rally deployment"
        ft_utils.execute_command_raise(cmd, error_msg=error_msg)

        cmd = "rally deployment check"
        error_msg = "OpenStack not responding or faulty Rally deployment."
        ft_utils.execute_command_raise(cmd, error_msg=error_msg)

        cmd = "rally deployment list"
        ft_utils.execute_command(cmd,
                                 error_msg=("Problem while listing "
                                            "Rally deployment."))

        cmd = "rally plugin list | head -5"
        ft_utils.execute_command(cmd,
                                 error_msg=("Problem while showing "
                                            "Rally plugins."))

    @staticmethod
    def install_tempest():
        logger.info("Installing tempest from existing repo...")
        cmd = ("rally verify list-verifiers | "
               "grep '{0}' | wc -l".format(
                   CONST.__getattribute__('tempest_deployment_name')))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while p.poll() is None:
            line = p.stdout.readline().rstrip()
            if str(line) == '0':
                logger.debug(
                    "Tempest %s does not exist" %
                    CONST.__getattribute__('tempest_deployment_name'))
                cmd = ("rally verify create-verifier --source {0} "
                       "--name {1} --type tempest --system-wide" .format(
                           CONST.__getattribute__('dir_repo_tempest'),
                           CONST.__getattribute__('tempest_deployment_name')))
                error_msg = "Problem while installing Tempest."
                ft_utils.execute_command_raise(cmd, error_msg=error_msg)

    @staticmethod
    def create_flavor():
        _, flavor_id = os_utils.get_or_create_flavor('m1.tiny',
                                                     '512',
                                                     '1',
                                                     '1',
                                                     public=True)
        if flavor_id is None:
            raise Exception('Failed to create flavor')

    def check_environment(self):
        msg_not_active = "The Functest environment is not installed."
        if not os.path.isfile(CONST.__getattribute__('env_active')):
            raise Exception(msg_not_active)
        with open(CONST.__getattribute__('env_active'), "r") as env_file:
            s = env_file.read()
            if not re.search("1", s):
                raise Exception(msg_not_active)
        logger.info("Functest environment is installed.")

    def main(self, **kwargs):
        try:
            if not (kwargs['action'] in ACTIONS):
                logger.error('Argument not valid.')
                return Result.EX_ERROR
            elif kwargs['action'] == "start":
                logger.info("####### Preparing Functest environment #######\n")
                Environment.verify_deployment()
                Environment.check_env_variables()
                Environment.create_directories()
                Environment.source_rc_file()
                Environment.update_config_file()
                Environment.install_rally()
                Environment.install_tempest()
                Environment.create_flavor()
                with open(CONST.__getattribute__('env_active'), "w") as file:
                    file.write("1")
                self.check_environment()
            elif kwargs['action'] == "check":
                self.check_environment()
        except Exception as error:
            logger.error(error)
            return Result.EX_ERROR
        return Result.EX_OK


def main():
    logging.config.fileConfig(pkg_resources.resource_filename(
        'functest', 'ci/logging.ini'))
    parser = PrepareEnvParser()
    args = parser.parse_args(sys.argv[1:])
    env = Environment()
    return env.main(**args).value
