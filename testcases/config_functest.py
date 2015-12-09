#!/usr/bin/env python
#
# Copyright (c) 2015 Ericsson
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import re, json, os, urllib2, argparse, logging, shutil, subprocess, yaml, sys, getpass
import functest_utils
from git import Repo
from os import stat
from pwd import getpwuid
from neutronclient.v2_0 import client as neutronclient

actions = ['start', 'check', 'clean']
parser = argparse.ArgumentParser()
parser.add_argument("repo_path", help="Path to the repository")
parser.add_argument("action", help="Possible actions are: '{d[0]}|{d[1]}|{d[2]}' ".format(d=actions))
parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
parser.add_argument("-f", "--force", help="Force",  action="store_true")
args = parser.parse_args()


""" logging configuration """
logger = logging.getLogger('config_functest')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

if not os.path.exists(args.repo_path):
    logger.error("Repo directory not found '%s'" % args.repo_path)
    exit(-1)

with open(args.repo_path+"testcases/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()




""" global variables """
# Directories
REPO_PATH = args.repo_path
RALLY_DIR = REPO_PATH + functest_yaml.get("general").get("directories").get("dir_rally")
RALLY_REPO_DIR = functest_yaml.get("general").get("directories").get("dir_repo_rally")
RALLY_INSTALLATION_DIR = functest_yaml.get("general").get("directories").get("dir_rally_inst")
RALLY_RESULT_DIR = functest_yaml.get("general").get("directories").get("dir_rally_res")
VPING_DIR = REPO_PATH + functest_yaml.get("general").get("directories").get("dir_vping")
ODL_DIR = REPO_PATH + functest_yaml.get("general").get("directories").get("dir_odl")
DATA_DIR = functest_yaml.get("general").get("directories").get("dir_functest_data")

# Tempest/Rally configuration details
DEPLOYMENT_MAME = "opnfv-rally"
RALLY_COMMIT = functest_yaml.get("general").get("openstack").get("rally_stable_commit")

#Image (cirros)
IMAGE_FILE_NAME = functest_yaml.get("general").get("openstack").get("image_file_name")
IMAGE_PATH = DATA_DIR + "/" + IMAGE_FILE_NAME

# NEUTRON Private Network parameters
NEUTRON_PRIVATE_NET_NAME = functest_yaml.get("general"). \
    get("openstack").get("neutron_private_net_name")
NEUTRON_PRIVATE_SUBNET_NAME = functest_yaml.get("general"). \
    get("openstack").get("neutron_private_subnet_name")
NEUTRON_PRIVATE_SUBNET_CIDR = functest_yaml.get("general"). \
    get("openstack").get("neutron_private_subnet_cidr")
NEUTRON_ROUTER_NAME = functest_yaml.get("general"). \
    get("openstack").get("neutron_router_name")

creds_neutron = functest_utils.get_credentials("neutron")
neutron_client = neutronclient.Client(**creds_neutron)

def action_start():
    """
    Start the functest environment installation
    """
    if not functest_utils.check_internet_connectivity():
        logger.error("There is no Internet connectivity. Please check the network configuration.")
        exit(-1)

    if action_check():
        logger.info("Functest environment already installed. Nothing to do.")
        exit(0)

    else:
        # Clean in case there are left overs
        logger.debug("Cleaning possible functest environment leftovers.")
        action_clean()
        logger.info("Starting installation of functest environment")

        private_net = get_private_net(neutron_client)
        if private_net is None:
            # If there is no private network in the deployment we create one
            if not create_private_neutron_net(neutron_client):
                logger.error("There has been a problem while creating the functest network.")
                action_clean()
                exit(-1)
        else:
            logger.info("Private network '%s' already existing in the deployment."
                 % private_net['name'])


        logger.info("Installing Rally...")
        if not install_rally():
            logger.error("There has been a problem while installing Rally.")
            action_clean()
            exit(-1)

        logger.info("Configuring Tempest...")
        if not configure_tempest():
            logger.error("There has been a problem while configuring Tempest.")
            action_clean()
            exit(-1)

        # Create result folder under functest if necessary
        if not os.path.exists(RALLY_RESULT_DIR):
            os.makedirs(RALLY_RESULT_DIR)

        exit(0)


def action_check():
    """
    Check if the functest environment is properly installed
    """
    errors_all = False
    errors = False
    logger.info("Checking current functest configuration...")

    logger.debug("Checking script directories...")

    dirs = [RALLY_DIR, RALLY_INSTALLATION_DIR, VPING_DIR, ODL_DIR]
    for dir in dirs:
        if not os.path.exists(dir):
            logger.debug("The directory '%s' does NOT exist." % dir)
            errors = True
            errors_all = True
        else:
            logger.debug("   %s found" % dir)
    if not errors:
        logger.debug("...OK")
    else:
        logger.debug("...FAIL")


    logger.debug("Checking Rally deployment...")
    if not check_rally():
        logger.debug("   Rally deployment NOT installed.")
        errors_all = True
        logger.debug("...FAIL")
    else:
        logger.debug("...OK")

    logger.debug("Checking Image...")
    errors = False
    if not os.path.isfile(IMAGE_PATH):
        logger.debug("   Image file '%s' NOT found." % IMAGE_PATH)
        errors = True
        errors_all = True
    else:
        logger.debug("   Image file found in %s" % IMAGE_PATH)


    if not errors:
        logger.debug("...OK")
    else:
        logger.debug("...FAIL")

    #TODO: check OLD environment setup
    return not errors_all



def action_clean():
    """
    Clean the existing functest environment
    """
    logger.info("Removing current functest environment...")
    if os.path.exists(RALLY_INSTALLATION_DIR):
        logger.debug("Removing Rally installation directory %s" % RALLY_INSTALLATION_DIR)
        shutil.rmtree(RALLY_INSTALLATION_DIR,ignore_errors=True)

    if os.path.exists(RALLY_RESULT_DIR):
        logger.debug("Removing Result directory")
        shutil.rmtree(RALLY_RESULT_DIR,ignore_errors=True)


    logger.info("Functest environment clean!")



def install_rally():
    if check_rally():
        logger.info("Rally is already installed.")
    else:
        logger.debug("Executing %s/install_rally.sh..." %RALLY_REPO_DIR)
        install_script = RALLY_REPO_DIR + "/install_rally.sh --yes"
        cmd = 'sudo ' + install_script
        functest_utils.execute_command(cmd,logger)

        logger.debug("Creating Rally environment...")
        cmd = "rally deployment create --fromenv --name="+DEPLOYMENT_MAME
        functest_utils.execute_command(cmd,logger)

        logger.debug("Installing tempest...")
        cmd = "rally verify install"
        functest_utils.execute_command(cmd,logger)

        cmd = "rally deployment check"
        functest_utils.execute_command(cmd,logger)
        #TODO: check that everything is 'Available' and warn if not

        cmd = "rally show images"
        functest_utils.execute_command(cmd,logger)

        cmd = "rally show flavors"
        functest_utils.execute_command(cmd,logger)

    return True


def configure_tempest():
    """
    Add/update needed parameters into tempest.conf file generated by Rally
    """

    creds_neutron = functest_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)

    logger.debug("Generating tempest.conf file...")
    cmd = "rally verify genconfig"
    functest_utils.execute_command(cmd,logger)

    logger.debug("Resolving deployment UUID...")
    cmd = "rally deployment list | awk '/"+DEPLOYMENT_MAME+"/ {print $2}'"
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT);
    deployment_uuid = p.stdout.readline().rstrip()
    if deployment_uuid == "":
        logger.debug("   Rally deployment NOT found")
        return False

    logger.debug("Finding tempest.conf file...")
    tempest_conf_file = RALLY_INSTALLATION_DIR+"/tempest/for-deployment-" \
                        +deployment_uuid+"/tempest.conf"

    logger.debug("  Updating fixed_network_name...")
    fixed_network = functest_utils.get_network_list(neutron_client)[0]['name']
    if fixed_network != None:
        cmd = "crudini --set "+tempest_conf_file+" compute fixed_network_name "+fixed_network
        functest_utils.execute_command(cmd,logger)

    return True


def check_rally():
    """
    Check if Rally is installed and properly configured
    """
    if os.path.exists(RALLY_INSTALLATION_DIR):
        logger.debug("   Rally installation directory found in %s" % RALLY_INSTALLATION_DIR)
        FNULL = open(os.devnull, 'w');
        cmd="rally deployment list | grep "+DEPLOYMENT_MAME
        logger.debug('   Executing command : {}'.format(cmd))
        p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=FNULL);
        #if the command does not exist or there is no deployment
        line = p.stdout.readline()
        if line == "":
            logger.debug("   Rally deployment NOT found")
            return False
        logger.debug("   Rally deployment found")
        return True
    else:
        return False

def get_private_net(neutron):
    # Checks if there is an existing private network in the deployment
    networks = functest_utils.get_network_list(neutron_client)
    if len(networks) == 0:
        return None

    for net in networks:
        if net['router:external'] == False:
            logger.debug("Private network found '%s'" % net['name'])
            return net

    return None


def create_private_neutron_net(neutron):
    neutron.format = 'json'
    logger.info('Creating neutron network %s...' % NEUTRON_PRIVATE_NET_NAME)
    network_id = functest_utils. \
        create_neutron_net(neutron, NEUTRON_PRIVATE_NET_NAME)

    if not network_id:
        return False
    logger.debug("Network '%s' created successfully" % network_id)
    logger.debug('Creating Subnet....')
    subnet_id = functest_utils. \
        create_neutron_subnet(neutron,
                              NEUTRON_PRIVATE_SUBNET_NAME,
                              NEUTRON_PRIVATE_SUBNET_CIDR,
                              network_id)
    if not subnet_id:
        return False
    logger.debug("Subnet '%s' created successfully" % subnet_id)
    logger.debug('Creating Router...')
    router_id = functest_utils. \
        create_neutron_router(neutron, NEUTRON_ROUTER_NAME)

    if not router_id:
        return False

    logger.debug("Router '%s' created successfully" % router_id)
    logger.debug('Adding router to subnet...')

    result = functest_utils.add_interface_router(neutron, router_id, subnet_id)

    if not result:
        return False

    logger.debug("Interface added successfully.")
    network_dic = {'net_id': network_id,
                   'subnet_id': subnet_id,
                   'router_id': router_id}
    return True


def main():
    if not (args.action in actions):
        logger.error('argument not valid')
        exit(-1)


    if not functest_utils.check_credentials():
        logger.error("Please source the openrc credentials and run the script again.")
        #TODO: source the credentials in this script
        exit(-1)


    if args.action == "start":
        action_start()

    if args.action == "check":
        if action_check():
            logger.info("Functest environment correctly installed")
        else:
            logger.info("Functest environment not found or faulty")

    if args.action == "clean":
        if args.force :
            action_clean()
        else :
            while True:
                print("Are you sure? [y|n]")
                answer = raw_input("")
                if answer == "y":
                    action_clean()
                    break
                elif answer == "n":
                    break
                else:
                    print("Invalid option.")
    exit(0)


if __name__ == '__main__':
    main()

