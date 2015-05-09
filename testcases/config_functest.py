#!/usr/bin/env python
#
# Copyright (c) 2015 Ericsson
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import re, json, os, urllib2, argparse, logging, shutil, subprocess, yaml
from git import Repo

actions = ['start', 'check', 'clean']

with open('functest.yaml') as f: 
    functest_yaml = yaml.safe_load(f)
f.close()

""" global variables """
HOME = os.environ['HOME']+"/"
FUNCTEST_BASE_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_functest")
RALLY_REPO_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_rally_repo")
RALLY_TEST_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_rally")
RALLY_INSTALLATION_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_rally_inst")
BENCH_TESTS_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_rally_scn")
VPING_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_vping")
ODL_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_odl")
IMAGE_URL = functest_yaml.get("general").get("openstack").get("image_url")
IMAGE_DISK_FORMAT = functest_yaml.get("general").get("openstack").get("image_disk_format")
IMAGE_NAME = functest_yaml.get("general").get("openstack").get("image_name")
IMAGE_FILE_NAME = IMAGE_URL.rsplit('/')[-1]
IMAGE_DOWNLOAD_PATH = FUNCTEST_BASE_DIR + IMAGE_FILE_NAME
"""
print "FUNCTEST_BASE_DIR=" +FUNCTEST_BASE_DIR
print "IMAGE_URL=" +IMAGE_URL
print "IMAGE_DISK_FORMAT=" +  IMAGE_DISK_FORMAT
print "IMAGE_FILE_NAME=" +  IMAGE_FILE_NAME
print "IMAGE_NAME=" +  IMAGE_NAME
print "IMAGE_DOWNLOAD_PATH=" +  IMAGE_DOWNLOAD_PATH
print "RALLY_REPO_DIR=" +  RALLY_REPO_DIR
print "RALLY_TEST_DIR=" +  RALLY_TEST_DIR
print "BENCH_TESTS_DIR=" +  BENCH_TESTS_DIR
print "RALLY_INSTALLATION_DIR=" +  RALLY_INSTALLATION_DIR
print "VPING_DIR=" +  VPING_DIR
print "ODL_DIR=" +  ODL_DIR
"""

parser = argparse.ArgumentParser()
parser.add_argument("action", help="Possible actions are: '{d[0]}|{d[1]}|{d[2]}' ".format(d=actions))
parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
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



def config_functest_start():
    """
    Start the functest environment installation
    """
    if config_functest_check():
        logger.info("Functest environment already installed in %s. Nothing to do." %FUNCTEST_BASE_DIR)
        exit(0)
    elif not check_internet_connectivity():
        logger.error("There is no Internet connectivity. Please check the network configuration.")
        exit(-1)
    elif not check_credentials():
        logger.error("Please source the openrc credentials and run the script again.")
        #TODO: source the credentials in this script
        exit(-1)
    else:
        config_functest_clean()

        logger.info("Starting installationg of functest environment in %s" %FUNCTEST_BASE_DIR)
        os.makedirs(FUNCTEST_BASE_DIR)
        if not os.path.exists(FUNCTEST_BASE_DIR):
            logger.error("There has been a problem while creating the environment directory.")
            exit(-1)

        logger.info("Donwloading test scripts and scenarios...")
        if not download_tests():
            logger.error("There has been a problem while downloading the test scripts and scenarios.")
            config_functest_clean()
            exit(-1)

        logger.info("Installing Rally...")
        if not install_rally():
            logger.error("There has been a problem while installing Rally.")
            config_functest_clean()
            exit(-1)

        logger.info("Installing ODL environment...")
        if not install_odl():
            logger.error("There has been a problem while installing Robot.")
            config_functest_clean()
            exit(-1)

        logger.info("Donwloading image...")
        if not download_url_with_progress(IMAGE_URL, FUNCTEST_BASE_DIR):
            logger.error("There has been a problem while downloading the image.")
            config_functest_clean()
            exit(-1)

        logger.info("Creating Glance image: %s ..." %IMAGE_NAME)
        if not create_glance_image(IMAGE_DOWNLOAD_PATH,IMAGE_NAME,IMAGE_DISK_FORMAT):
            logger.error("There has been a problem while creating the Glance image.")
            config_functest_clean()
            exit(-1)

        exit(0)



def config_functest_check():
    """
    Check if the functest environment is properly installed
    """
    logger.info("Checking current functest configuration...")

    logger.debug("Checking directories...")
    dirs = [FUNCTEST_BASE_DIR, RALLY_INSTALLATION_DIR, RALLY_REPO_DIR, RALLY_TEST_DIR, BENCH_TESTS_DIR, VPING_DIR, ODL_DIR]
    for dir in dirs:
        if not os.path.exists(dir):
            logger.debug("The directory %s does not exist." %dir)
            return False
        logger.debug("   %s found" % dir)

    logger.debug("...OK")
    logger.debug("Checking Rally deployment...")
    if not check_rally():
        logger.debug("Rally deployment not found.")
        return False
    logger.debug("...OK")

    logger.debug("Checking Image...")
    if not os.path.isfile(IMAGE_DOWNLOAD_PATH):
        return False
    logger.debug("   Image file found in %s" %IMAGE_DOWNLOAD_PATH)

    cmd="glance image-list | grep " + IMAGE_NAME
    FNULL = open(os.devnull, 'w');
    logger.debug('   Executing command : {}'.format(cmd))
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=FNULL);
    #if the command does not exist or there is no glance image
    line = p.stdout.readline()
    if line == "":
        logger.debug("   Glance image not found")
        return False
    logger.debug("   Glance image found")
    logger.debug("...OK")

    #TODO: check OLD environment setup

    return True




def config_functest_clean():
    """
    Clean the existing functest environment
    """
    logger.info("Removing current functest environment...")
    if os.path.exists(RALLY_INSTALLATION_DIR):
        logger.debug("Removing rally installation directory %s" % RALLY_INSTALLATION_DIR)
        shutil.rmtree(RALLY_INSTALLATION_DIR,ignore_errors=True)

    if os.path.exists(FUNCTEST_BASE_DIR):
        logger.debug("Removing functest directory %s" % FUNCTEST_BASE_DIR)
        cmd = "sudo rm -rf " + FUNCTEST_BASE_DIR #need to be sudo, not possible with rmtree
        execute_command(cmd)

    logger.debug("Deleting glance images")
    cmd = "glance image-list | grep "+IMAGE_NAME+" | cut -c3-38"
    p = os.popen(cmd,"r")

    #while image_id = p.readline()
    for image_id in p.readlines():
        cmd = "glance image-delete " + image_id
        execute_command(cmd)

    return True


def install_rally():
    if check_rally():
        logger.info("Rally is already installed.")
    else:
        logger.debug("Cloning repository...")
        url = "https://git.openstack.org/openstack/rally"
        Repo.clone_from(url, RALLY_REPO_DIR)

        logger.debug("Executing %s./install_rally.sh..." %RALLY_REPO_DIR)
        install_script = RALLY_REPO_DIR + "install_rally.sh"
        cmd = 'sudo ' + install_script
        execute_command(cmd)
        #subprocess.call(['sudo', install_script])

        logger.debug("Creating Rally environment...")
        cmd = "rally deployment create --fromenv --name=opnfv-arno-rally"
        execute_command(cmd)

        logger.debug("Installing tempest...")
        cmd = "rally-manage tempest install"
        execute_command(cmd)

        cmd = "rally deployment check"
        execute_command(cmd)
        #TODO: check that everything is 'Available' and warn if not

        cmd = "rally show images"
        execute_command(cmd)

        cmd = "rally show flavors"
        execute_command(cmd)

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
            logger.debug("   Rally deployment not found")
            return False
        logger.debug("   Rally deployment found")
        return True
    else:
        logger.debug("   Rally installation directory not found")
        return False


def install_odl():
    cmd = "chmod +x " + ODL_DIR + "create_venv.sh"
    execute_command(cmd)
    cmd = ODL_DIR + "create_venv.sh"
    execute_command(cmd)
    return True


def check_credentials():
    """
    Check if the OpenStack credentials (openrc) are sourced
    """
    #TODO: there must be a short way to do this, doing if os.environ["something"] == "" throws an error
    try:
       os.environ['OS_AUTH_URL']
    except KeyError:
        return False
    try:
       os.environ['OS_USERNAME']
    except KeyError:
        return False
    try:
       os.environ['OS_PASSWORD']
    except KeyError:
        return False
    try:
       os.environ['OS_TENANT_NAME']
    except KeyError:
        return False
    try:
       os.environ['OS_REGION_NAME']
    except KeyError:
        return False
    return True


def download_tests():
    os.makedirs(VPING_DIR)
    os.makedirs(ODL_DIR)
    os.makedirs(BENCH_TESTS_DIR)

    logger.info("Downloading vPing test...")
    vPing_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/vPing/CI/libraries/vPing.py'
    if not download_url(vPing_url,VPING_DIR):
        return False


    logger.info("Downloading Rally bench tests...")
    run_rally_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/VIM/OpenStack/CI/libraries/run_rally.py'
    if not download_url(run_rally_url,RALLY_TEST_DIR):
        return False

    rally_bench_base_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/VIM/OpenStack/CI/suites/'
    bench_tests = ['authenticate', 'cinder', 'glance', 'heat', 'keystone', 'neutron', 'nova', 'quotas', 'requests', 'tempest', 'vm']
    for i in bench_tests:
        rally_bench_url = rally_bench_base_url + "opnfv-" + i + ".json"
        logger.debug("Downloading %s" %rally_bench_url)
        if not download_url(rally_bench_url,BENCH_TESTS_DIR):
            return False

    logger.info("Downloading OLD tests...")
    odl_base_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/Controllers/ODL/CI/'
    odl_tests = ['create_venv.sh', 'requirements.pip', 'start_tests.sh', 'test_list.txt']
    for i in odl_tests:
        odl_url = odl_base_url + i
        logger.debug("Downloading %s" %odl_url)
        if not download_url(odl_url,ODL_DIR):
            return False

    return True



def create_glance_image(path,name,disk_format):
    """
    Create a glance image given the absolute path of the image, its name and the disk format
    """
    cmd = "glance image-create --name "+name+" --is-public true --disk-format "+disk_format+" --container-format bare --file "+path
    execute_command(cmd)
    return True


def download_url(url, dest_path):
    """
    Download a file to a destination path given a URL
    """
    name = url.rsplit('/')[-1]
    dest = dest_path + name
    try:
        response = urllib2.urlopen(url)
    except (urllib2.HTTPError, urllib2.URLError):
        logger.error("Error in fetching %s" %url)
        return False

    with open(dest, 'wb') as f:
        f.write(response.read())
    return True


def download_url_with_progress(url, dest_path):
    """
    Download a file to a destination path given a URL showing the progress
    """
    name = url.rsplit('/')[-1]
    dest = dest_path + name
    try:
        response = urllib2.urlopen(url)
    except (urllib2.HTTPError, urllib2.URLError):
        logger.error("Error in fetching %s" %url)
        return False

    f = open(dest, 'wb')
    meta = response.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    logger.info("Downloading: %s Bytes: %s" %(dest, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = response.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()
    print("\n")
    return True


def check_internet_connectivity(url='http://www.google.com/'):
    """
    Check if there is access to the internet
    """
    try:
        urllib2.urlopen(url, timeout=5)
        return True
    except urllib.request.URLError:
        return False

def execute_command(cmd):
    """
    Execute Linux command
    """
    logger.debug('Executing command : {}'.format(cmd))
    #p = os.popen(cmd,"r")
    #logger.debug(p.read())
    output_file = "/tmp/output.txt"
    f = open(output_file, 'w+')
    p = subprocess.call(cmd,shell=True, stdout=f, stderr=subprocess.STDOUT)
    f.close()
    f = open(output_file, 'r')
    logger.debug(f.read())
    #p = subprocess.call(cmd,shell=True);
    if p == 0 :
        return True
    else:
        logger.error("Error when executing command %s" %cmd)
        exit(-1)




def main():
    if not (args.action in actions):
        logger.error('argument not valid')
        exit(-1)

    if args.action == "start":
        config_functest_start()

    if args.action == "check":
        if config_functest_check():
            logger.info("Functest environment correctly installed")
        else:
            logger.info("Functest environment not found or faulty")

    if args.action == "clean":
        while True:
            print("Are you sure? [y|n]")
            answer = raw_input("")
            if answer == "y":
                config_functest_clean()
                break
            elif answer == "n":
                break
            else:
                print("Invalid option.")
    exit(0)


if __name__ == '__main__':
    main()

