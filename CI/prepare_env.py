#!/bin/bash

#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# Installs the Functest framework within the Docker container
# and run the tests automatically
#
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import argparse
import logging
import os
import subprocess
import sys
import yaml

import functest_utils as ftu
import openstack_utils as osu

actions = ['start', 'check']
parser = argparse.ArgumentParser()
parser.add_argument("action", help="Possible actions are: "
                    "'{d[0]}|{d[1]}' ".format(d=actions))
parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
args = parser.parse_args()

# TO BE CHANGED. generate_defaults will be in the same directory
# and no need to add the path
sys.path.append('../testcases/VIM/OpenStack/CI/libraries/')
import generate_defaults as gendef

""" logging configuration """
logger = logging.getLogger('prepare_env')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

INSTALLERS = ['fuel', 'compass', 'apex', 'joid']
CI_INSTALLER_TYPE = ""
CI_INSTALLER_IP = ""
CI_DEBUG = False
REPOS_DIR = os.getenv('repos_dir')
FUNCTEST_REPO = REPOS_DIR + '/functest/'

with open("/home/opnfv/repos/functest/testcases/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)

FUNCTEST_CONF_DIR = functest_yaml.get("general").get(
    "directories").get("dir_functest_conf")

FUNCTEST_DATA_DIR = functest_yaml.get("general").get(
    "directories").get("dir_functest_data")
FUNCTEST_RESULTS_DIR = functest_yaml.get("general").get(
    "directories").get("dir_results")
DEPLOYMENT_MAME = functest_yaml.get("rally").get("deployment_name")
TEMPEST_REPO_DIR = functest_yaml.get("general").get(
    "directories").get("dir_repo_tempest")


def check_env_variables():
    logger.info("Checking environment variables...")
    global CI_INSTALLER_TYPE
    global CI_INSTALLER_IP
    global CI_DEBUG
    CI_INSTALLER_TYPE = os.getenv('INSTALLER_TYPE')
    CI_INSTALLER_IP = os.getenv('INSTALLER_IP')
    CI_SCENARIO = os.getenv('DEPLOY_SCENARIO')
    CI_NODE = os.getenv('NODE_NAME')
    CI_BUILD_TAG = os.getenv('BUILD_TAG')
    CI_DEBUG = os.getenv('CI_DEBUG')

    if CI_DEBUG:
        logger.debug("Found 'CI_DEBUG=%s'" % CI_DEBUG)
        if CI_DEBUG in ['true', 'True', 'TRUE']:
            CI_DEBUG = True
            ch.setLevel(logging.DEBUG)

    # Mandatory environment variables
    if CI_INSTALLER_TYPE is None:
        logger.error("The env variable 'INSTALLER_TYPE' is not defined. "
                     "Please add it to the 'docker run' command.")
        sys.exit("INSTALLER_TYPE not found.")
    else:
        logger.debug("Found 'INSTALLER_TYPE=%s'." % CI_INSTALLER_TYPE)

    if os.getenv('INSTALLER_TYPE') not in INSTALLERS:
        logger.error("'INSTALLER_TYPE=%s' is not a valid installer. "
                     "Available OPNFV Installers are ")
        sys.exit("Wrong INSTALLER_TYPE.")

    if CI_SCENARIO is None:
        logger.error("The env variable 'DEPLOY_SCENARIO' is not defined. "
                     "Please add it to the 'docker run' command.")
        sys.exit()
    else:
        logger.debug("Found 'DEPLOY_SCENARIO=%s'" % CI_SCENARIO)

    # Optional environment variables
    if CI_INSTALLER_IP is None:
        logger.warning("The env variable 'INSTALLER_IP' is not defined. "
                       "It is needed to fetch the OpenStack credentials. "
                       "If the credentials are not provided to the "
                       "container as a volume, please add this env variable "
                       "to the 'docker run' command.")
    else:
        logger.debug("Found 'INSTALLER_IP=%s'." % CI_INSTALLER_IP)

    if CI_NODE:
        logger.debug("Found 'NODE_NAME=%s'." % CI_NODE)

    if CI_BUILD_TAG:
        logger.debug("Found 'BUILD_TAG=%s'." % CI_BUILD_TAG)


def create_directories():
    logger.info("Creating needed directories...")
    if not os.path.exists(FUNCTEST_CONF_DIR):
        os.makedirs(FUNCTEST_CONF_DIR)
        logger.debug("%s created." % FUNCTEST_CONF_DIR)

    if not os.path.exists(FUNCTEST_DATA_DIR):
        os.makedirs(FUNCTEST_DATA_DIR)
        logger.debug("%s created." % FUNCTEST_DATA_DIR)

    if not os.path.exists(FUNCTEST_RESULTS_DIR):
        os.makedirs(FUNCTEST_RESULTS_DIR)
        logger.debug("%s created." % FUNCTEST_RESULTS_DIR)
        os.makedirs(FUNCTEST_RESULTS_DIR + "/ODL/")
        logger.debug("%s created." % (FUNCTEST_RESULTS_DIR + "/ODL/"))


def source_rc_file():
    rc_file = os.getenv('creds')
    if rc_file is None:
        logger.warning("The environment variable 'creds' must be set and"
                       "pointing to the local RC file. Using default: "
                       "/home/opnfv/functest/conf/openstack.creds ...")
        rc_file = "/home/opnfv/functest/conf/openstack.creds ..."

    if not os.path.isfile(rc_file):
        logger.info("OpenStack RC file not provided. "
                    "Fetching it from the installer...")

        cmd = ("/home/opnfv/repos/releng/utils/fetch_os_creds.sh "
               "-d %s -i %s -a %s"
               % (rc_file, CI_INSTALLER_TYPE, CI_INSTALLER_IP))
        logger.debug("Executing command: %s" % cmd)
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]

        logger.debug(output)

    else:
        logger.info("OpenStack RC file provided in %s." % rc_file)

    logger.info("Sourcing the OpenStack RC file...")
    creds = osu.source_credentials(rc_file)
    logger.debug(creds)


def verify_deployment():
    logger.info("Verifying OpenStack services...")
    cmd = ("%s/testcases/VIM/OpenStack/CI/libraries/check_os.sh"
           % FUNCTEST_REPO)

    logger.debug("Executing command: %s" % cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    while p.poll() is None:
        line = p.stdout.readline().rstrip()
        if "ERROR" in line:
            logger.error(line)
            sys.exit("Problem while running 'check_os.sh'.")
        logger.debug(line)


def install_rally():
    logger.info("Creating Rally environment...")

    cmd = "rally deployment destroy opnfv-rally"
    ftu.execute_command(cmd, logger=None, exit_on_error=False)

    cmd = "rally deployment create --fromenv --name=" + DEPLOYMENT_MAME
    if not ftu.execute_command(cmd, logger):
        logger.error("Problem while creating Rally deployment.")
        sys.exit(cmd)

    logger.info("Installing tempest from existing repo...")
    cmd = ("rally verify install --source " + TEMPEST_REPO_DIR +
           " --system-wide")
    if not ftu.execute_command(cmd, logger):
        logger.error("Problem while installing Tempest.")
        sys.exit(cmd)

    cmd = "rally deployment check"
    if not ftu.execute_command(cmd, logger):
        logger.error("OpenStack not responding or faulty Rally deployment.")
        sys.exit(cmd)

    cmd = "rally show images"
    if not ftu.execute_command(cmd, logger):
        logger.error("Problem while listing OpenStack images.")
        sys.exit(cmd)

    cmd = "rally show flavors"
    if not ftu.execute_command(cmd, logger):
        logger.error("Problem while showing OpenStack flavors.")
        sys.exit(cmd)


def generate_os_defaults():
    logger.info("Generating OpenStack defaults...")
    gendef.main()
"""
def generate_tiers():
def check_environment():
"""


def main():
    if not (args.action in actions):
        logger.error('Argument not valid.')
        sys.exit()

    if args.action == "start":
        print ("\n######### Preparing Functest environment #########\n")
        check_env_variables()
        create_directories()
        source_rc_file()
        verify_deployment()
        install_rally()
        generate_os_defaults()
        """
        generate_tiers()
        """

    """
    if args.action == "check":
        check_environment()
    """

    exit(0)


if __name__ == '__main__':
    main()
