#!/usr/bin/env python
#
# Copyright (c) 2015 Ericsson
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import re, json, os, urllib2, argparse, logging, shutil, subprocess, yaml, sys
import functest_utils
from git import Repo

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
HOME = os.environ['HOME']+"/"
REPO_PATH = args.repo_path
RALLY_DIR = REPO_PATH + functest_yaml.get("general").get("directories").get("dir_rally")
RALLY_REPO_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_rally_repo")
RALLY_INSTALLATION_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_rally_inst")
RALLY_RESULT_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_rally_res")
VPING_DIR = REPO_PATH + functest_yaml.get("general").get("directories").get("dir_vping")
ODL_DIR = REPO_PATH + functest_yaml.get("general").get("directories").get("dir_odl")


#GLANCE image parameters
IMAGE_URL = functest_yaml.get("general").get("openstack").get("image_url")
IMAGE_DISK_FORMAT = functest_yaml.get("general").get("openstack").get("image_disk_format")
IMAGE_NAME = functest_yaml.get("general").get("openstack").get("image_name")
IMAGE_FILE_NAME = IMAGE_URL.rsplit('/')[-1]
IMAGE_DIR = HOME + functest_yaml.get("general").get("openstack").get("image_download_path")
IMAGE_PATH = IMAGE_DIR + IMAGE_FILE_NAME


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
        logger.info("Installing Rally...")
        if not install_rally():
            logger.error("There has been a problem while installing Rally.")
            action_clean()
            exit(-1)

        logger.info("Installing ODL environment...")
        if not install_odl():
            logger.error("There has been a problem while installing Robot.")
            action_clean()
            exit(-1)

        # Create result folder under functest if necessary
        if not os.path.exists(RALLY_RESULT_DIR):
            os.makedirs(RALLY_RESULT_DIR)

        logger.info("Downloading image...")
        if not functest_utils.download_url(IMAGE_URL, IMAGE_DIR):
            logger.error("There has been a problem downloading the image '%s'." %IMAGE_URL)
            action_clean()
            exit(-1)

        logger.info("Creating Glance image: %s ..." %IMAGE_NAME)
        if not create_glance_image(IMAGE_PATH,IMAGE_NAME,IMAGE_DISK_FORMAT):
            logger.error("There has been a problem while creating the Glance image.")
            action_clean()
            exit(-1)

        exit(0)


def action_check():
    """
    Check if the functest environment is properly installed
    """
    errors_all = False

    logger.info("Checking current functest configuration...")

    logger.debug("Checking script directories...")
    errors = False
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

    cmd="glance image-list | grep " + IMAGE_NAME
    FNULL = open(os.devnull, 'w');
    logger.debug('   Executing command : {}'.format(cmd))
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=FNULL);
    #if the command does not exist or there is no glance image
    line = p.stdout.readline()
    if line == "":
        logger.debug("   Glance image NOT found.")
        errors = True
        errors_all = True
    else:
        logger.debug("   Glance image found.")

    if not errors:
        logger.debug("...OK")
    else:
        logger.debug("...FAIL")

    #TODO: check OLD environment setup
    if errors_all:
        return False
    else:
        return True




def action_clean():
    """
    Clean the existing functest environment
    """
    logger.info("Removing current functest environment...")
    if os.path.exists(RALLY_INSTALLATION_DIR):
        logger.debug("Removing Rally installation directory %s" % RALLY_INSTALLATION_DIR)
        shutil.rmtree(RALLY_INSTALLATION_DIR,ignore_errors=True)

    if os.path.exists(RALLY_REPO_DIR):
        logger.debug("Removing Rally repository %s" % RALLY_REPO_DIR)
        cmd = "sudo rm -rf " + RALLY_REPO_DIR #need to be sudo, not possible with rmtree
        functest_utils.execute_command(cmd,logger)

    if os.path.exists(IMAGE_PATH):
        logger.debug("Deleting image")
        os.remove(IMAGE_PATH)

    cmd = "glance image-list | grep "+IMAGE_NAME+" | cut -c3-38"
    p = os.popen(cmd,"r")

    #while image_id = p.readline()
    for image_id in p.readlines():
        cmd = "glance image-delete " + image_id
        functest_utils.execute_command(cmd,logger)

    if os.path.exists(RALLY_RESULT_DIR):
        logger.debug("Removing Result directory")
        shutil.rmtree(RALLY_RESULT_DIR,ignore_errors=True)


    logger.info("Functest environment clean!")





def install_rally():
    if check_rally():
        logger.info("Rally is already installed.")
    else:
        logger.debug("Cloning repository...")
        url = "https://git.openstack.org/openstack/rally"
        Repo.clone_from(url, RALLY_REPO_DIR)

        logger.debug("Executing %s./install_rally.sh..." %RALLY_REPO_DIR)
        install_script = RALLY_REPO_DIR + "install_rally.sh"
        functest_utils.execute_command(install_script,logger)

        logger.debug("Creating Rally environment...")
        cmd = "rally deployment create --fromenv --name=opnfv-arno-rally"
        functest_utils.execute_command(cmd,logger)

        logger.debug("Installing tempest...")
        cmd = "rally-manage tempest install"
        functest_utils.execute_command(cmd,logger)

        cmd = "rally deployment check"
        functest_utils.execute_command(cmd,logger)
        #TODO: check that everything is 'Available' and warn if not

        cmd = "rally show images"
        functest_utils.execute_command(cmd,logger)

        cmd = "rally show flavors"
        functest_utils.execute_command(cmd,logger)

    return True



def check_rally():
    """
    Check if Rally is installed and properly configured
    """
    if os.path.exists(RALLY_INSTALLATION_DIR):
        logger.debug("   Rally installation directory found in %s" % RALLY_INSTALLATION_DIR)
        FNULL = open(os.devnull, 'w');
        cmd="rally deployment list | grep opnfv";
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


def install_odl():
    cmd = "chmod +x " + ODL_DIR + "start_tests.sh"
    functest_utils.execute_command(cmd,logger)
    cmd = "chmod +x " + ODL_DIR + "create_venv.sh"
    functest_utils.execute_command(cmd,logger)
    cmd = ODL_DIR + "create_venv.sh"
    functest_utils.execute_command(cmd,logger)
    return True



def create_glance_image(path,name,disk_format):
    """
    Create a glance image given the absolute path of the image, its name and the disk format
    """
    cmd = "glance image-create --name "+name+" --is-public true --disk-format "+disk_format+" --container-format bare --file "+path
    functest_utils.execute_command(cmd,logger)
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

