#!/usr/bin/env python
#
# Copyright (c) 2015 Ericsson
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import re, json, os, urllib2, argparse, logging, shutil

actions = ['start', 'check', 'clean']

""" global variables """
functest_dir = os.environ['HOME'] + '/.functest/'
#image_url = 'http://mirror.us.leaseweb.net/ubuntu-releases/14.04.2/ubuntu-14.04.2-server-amd64.iso'
image_url = 'http://download.cirros-cloud.net/0.3.0/cirros-0.3.0-i386-disk.img'
image_disk_format = 'raw'
image_name = image_url.rsplit('/')[-1]
image_path = functest_dir + image_name

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
    elif not check_rally():
        logger.error("Rally is not installed. Please follow the instructions to prepare the Rally environment.")
        exit(-1)
    else:
        logger.info("Starting installationg of functest environment in %s" %functest_dir)
        os.makedirs(functest_dir)
        if not os.path.exists(functest_dir):
            logger.error("There has been a problem why creating the environment directory")
            exit(-1)

        logger.info("Donwloading test scripts and scenarios...")
        download_tests()
        
        logger.info("Donwloading image...")
        download_url_with_progress(image_url, functest_dir)

        logger.info("Creating Glance image: %s ..." %image_name)
        create_glance_image(image_path,image_name,image_disk_format)
        exit(0)
         


def config_functest_check():
    """
    Check if the functest environment is installed
    """
    logger.info("Checking current functest configuration...")
    if not os.path.exists(functest_dir):
        logger.info("Functest environment directory not found")
        return False
    else:
        logger.info("Functest environment directory found in %s" %functest_dir)
        #TODO: more verifications here
        return True



def config_functest_clean():
    """
    Clean the existing functest environment
    """
    if not config_functest_check():
        logger.info("There is no functest environment installed. Nothing to clean.")
        return 0
    else:
        while True:
            print("Are you sure? [y|n]")
            answer = raw_input("")
            if answer == "y":
                logger.info("Removing current functest environment...")
                shutil.rmtree(functest_dir,ignore_errors=True)
                exit(0)
            elif answer == "n":
                exit(0)
            else:
                print("Invalid option.")




def check_rally():
    """
    Check if Rally is installed and properly configured
    """
    if os.path.exists(os.environ['HOME']+"/.rally/"):
        #TODO: do a more consistent check, for example running the comand rally deployment check
        return True
    else:
        return False


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
    vPing_dir = functest_dir + "vPing/"
    odl_dir = functest_dir + "ODL/"
    bench_tests_dir = functest_dir + "scenarios/"

    os.makedirs(vPing_dir)
    os.makedirs(odl_dir)
    os.makedirs(bench_tests_dir)

    logger.info("Downloading vPing test...")
    vPing_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/vPing/CI/libraries/vPing.py'
    download_url(vPing_url,vPing_dir)

    logger.info("Downloading Rally bench tests...")
    rally_bench_base_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/VIM/OpenStack/CI/suites/'
    bench_tests = ['authenticate', 'cinder', 'glance', 'heat', 'keystone', 'neutron', 'nova', 'quotas', 'requests', 'tempest', 'vm'] 
    for i in bench_tests:
        rally_bench_url = rally_bench_base_url + "opnfv-" + i + ".json"
	logger.debug("Downloading %s" %rally_bench_url)
        download_url(rally_bench_url,bench_tests_dir)

    logger.info("Downloading OLD tests...")
    odl_base_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/Controllers/ODL/CI/'
    odl_tests = ['start_tests.sh', 'test_list.txt'] 
    for i in odl_tests:
        odl_url = odl_base_url + i
	logger.debug("Downloading %s" %odl_url)
        download_url(odl_url,odl_dir)
    #TODO: complete 



def create_glance_image(path,name,disk_format):
    """
    Create a glance image given the absolute path of the image, its name and the disk format
    """
    cmd = "glance image-create --name "+name+" --is-public true --disk-format "+disk_format+" --container-format bare --file "+path
    execute_command(cmd)


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
    p = os.popen(cmd,"r")
    print (p.read())



def main():
    if not (args.action in actions):
        logger.error('argument not valid')
        exit(-1)

    if args.action == "start":
        config_functest_start()

    if args.action == "check":
        config_functest_check()

    if args.action == "clean":
        config_functest_clean()

if __name__ == '__main__':
    main()

