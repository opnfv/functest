#!/usr/bin/env python
#
# Copyright (c) 2015 Ericsson
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import re, json, os, urllib2, argparse, logging, shutil, subprocess
from git import Repo

actions = ['start', 'check', 'clean']

""" global variables """
functest_dir = os.environ['HOME'] + '/.functest/'
image_url = 'https://cloud-images.ubuntu.com/trusty/current/trusty-server-cloudimg-amd64-disk1.img'
#image_url = 'http://download.cirros-cloud.net/0.3.0/cirros-0.3.0-i386-disk.img'

image_disk_format = 'raw'
image_name = image_url.rsplit('/')[-1]
image_path = functest_dir + image_name
rally_repo_dir = functest_dir + "Rally_repo/"
rally_test_dir = functest_dir + "Rally_test/"
bench_tests_dir = rally_test_dir + "scenarios/"
rally_installation_dir = os.environ['HOME'] + "/.rally"
vPing_dir = functest_dir + "vPing/"
odl_dir = functest_dir + "ODL/"


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
        logger.info("Functest environment already installed in %s. Nothing to do." %functest_dir)
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

        logger.info("Starting installationg of functest environment in %s" %functest_dir)
        os.makedirs(functest_dir)
        if not os.path.exists(functest_dir):
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
        if not download_url_with_progress(image_url, functest_dir):
            logger.error("There has been a problem while downloading the image.")
            config_functest_clean()
            exit(-1)

        logger.info("Creating Glance image: %s ..." %image_name)
        if not create_glance_image(image_path,image_name,image_disk_format):
            logger.error("There has been a problem while creating the Glance image.")
            config_functest_clean()
            exit(-1)

        exit(0)



def config_functest_check():
    """
    Check if the functest environment is installed
    """
    logger.info("Checking current functest configuration...")
    if os.path.exists(functest_dir) and os.path.exists(rally_installation_dir):
        logger.info("Functest environment directory found in %s" %functest_dir)
        return True
    else:
        logger.info("Functest environment directory not found")
        return False



def config_functest_clean():
    """
    Clean the existing functest environment
    """
    logger.info("Removing current functest environment...")
    if os.path.exists(rally_installation_dir):
        logger.debug("Removing rally installation directory %s" % rally_installation_dir)
        shutil.rmtree(rally_installation_dir,ignore_errors=True)

    if os.path.exists(functest_dir):
        logger.debug("Removing functest directory %s" % functest_dir)
        cmd = "sudo rm -rf " + functest_dir #need to be sudo, not possible with rmtree
        execute_command(cmd)

    logger.debug("Deleting glance images")
    cmd = "glance image-list | grep "+image_name+" | cut -c3-38"
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
        Repo.clone_from(url, rally_repo_dir)

        logger.debug("Executing %s./install_rally.sh..." %rally_repo_dir)
        install_script = rally_repo_dir + "install_rally.sh"
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
    if os.path.exists(os.environ['HOME']+"/.rally/"):
        #TODO: do a more consistent check, for example running the comand rally deployment check
        return True
    else:
        return False


def install_odl():
    cmd = "chmod +x " + odl_dir + "create_venv.sh"
    execute_command(cmd)
    cmd = odl_dir + "create_venv.sh"
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
    os.makedirs(vPing_dir)
    os.makedirs(odl_dir)
    os.makedirs(bench_tests_dir)
    os.makedirs(rally_test_dir)

    logger.info("Downloading vPing test...")
    vPing_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/vPing/CI/libraries/vPing.py'
    if not download_url(vPing_url,vPing_dir):
        return False


    logger.info("Downloading Rally bench tests...")
    run_rally_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/VIM/OpenStack/CI/libraries/run_rally.py'
    if not download_url(run_rally_url,rally_test_dir):
        return False

    rally_bench_base_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/VIM/OpenStack/CI/suites/'
    bench_tests = ['authenticate', 'cinder', 'glance', 'heat', 'keystone', 'neutron', 'nova', 'quotas', 'requests', 'tempest', 'vm']
    for i in bench_tests:
        rally_bench_url = rally_bench_base_url + "opnfv-" + i + ".json"
        logger.debug("Downloading %s" %rally_bench_url)
        if not download_url(rally_bench_url,bench_tests_dir):
            return False

    logger.info("Downloading OLD tests...")
    odl_base_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/Controllers/ODL/CI/'
    odl_tests = ['create_venv.sh', 'requirements.pip', 'start_tests.sh', 'test_list.txt']
    for i in odl_tests:
        odl_url = odl_base_url + i
        logger.debug("Downloading %s" %odl_url)
        if not download_url(odl_url,odl_dir):
            return False

    return True
    #TODO: complete



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
        config_functest_check()

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

