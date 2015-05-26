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
from git import Repo

from neutronclient.v2_0 import client

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
VPING_DIR = REPO_PATH + functest_yaml.get("general").get("directories").get("dir_vping")
ODL_DIR = REPO_PATH + functest_yaml.get("general").get("directories").get("dir_odl")

# NEUTRON Private Network parameters
NEUTRON_PRIVATE_NET_NAME = functest_yaml.get("general").get("openstack").get("neutron_private_net_name")
NEUTRON_PRIVATE_SUBNET_NAME = functest_yaml.get("general").get("openstack").get("neutron_private_subnet_name")
NEUTRON_PRIVATE_SUBNET_CIDR = functest_yaml.get("general").get("openstack").get("neutron_private_subnet_cidr")
ROUTER_NAME = functest_yaml.get("general").get("openstack").get("neutron_router_name")

#GLANCE image parameters
IMAGE_URL = functest_yaml.get("general").get("openstack").get("image_url")
IMAGE_DISK_FORMAT = functest_yaml.get("general").get("openstack").get("image_disk_format")
IMAGE_NAME = functest_yaml.get("general").get("openstack").get("image_name")
IMAGE_FILE_NAME = IMAGE_URL.rsplit('/')[-1]
IMAGE_DIR = HOME + functest_yaml.get("general").get("openstack").get("image_download_path")
IMAGE_PATH = IMAGE_DIR + IMAGE_FILE_NAME


credentials = None
neutron_client = None

def action_start():
    """
    Start the functest environment installation
    """
    if not check_internet_connectivity():
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

        credentials = get_credentials()
        neutron_client = client.Client(**credentials)

        logger.info("Configuring Neutron...")
        logger.info("Checking if private network '%s' exists..." % NEUTRON_PRIVATE_NET_NAME)
        #Now: if exists we don't create it again (the clean command does not clean the neutron networks yet)
        if check_neutron_net(neutron_client, NEUTRON_PRIVATE_NET_NAME):
            logger.info("Private network '%s' found. No need to create another one." % NEUTRON_PRIVATE_NET_NAME)
        else:
            logger.info("Private network '%s' not found. Creating..." % NEUTRON_PRIVATE_NET_NAME)
            if not create_private_neutron_net(neutron_client):
                logger.error("There has been a problem while creating the Neutron network.")
                #action_clean()
                exit(-1)


        logger.info("Donwloading image...")
        if not download_url(IMAGE_URL, IMAGE_DIR):
            logger.error("There has been a problem while downloading the image.")
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
    credentials = get_credentials()
    neutron_client = client.Client(**credentials)

    logger.debug("Checking directories...")
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
        logger.debug("   Rally deployment NOT found.")
        errors_all = True
        logger.debug("...FAIL")
    else:
        logger.debug("...OK")


    logger.debug("Checking Neutron...")
    if not check_neutron_net(neutron_client, NEUTRON_PRIVATE_NET_NAME):
        logger.debug("   Private network '%s' NOT found." % NEUTRON_PRIVATE_NET_NAME)
        logger.debug("...FAIL")
        errors_all = True
    else:
        logger.debug("   Private network '%s' found." % NEUTRON_PRIVATE_NET_NAME)
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
        execute_command(cmd)
    #logger.debug("Deleting Neutron network %s" % NEUTRON_PRIVATE_NET_NAME)
    #if not delete_neutron_net() :
    #    logger.error("Error deleting the network. Remove it manually.")

    logger.debug("Deleting glance images")
    if os.path.exists(IMAGE_PATH):
        os.remove(IMAGE_PATH)

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
    cmd = "chmod +x " + ODL_DIR + "start_tests.sh"
    execute_command(cmd)
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


def get_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d

def get_nova_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d



def create_private_neutron_net(neutron):
    try:
        neutron.format = 'json'
        logger.debug('Creating Neutron network %s...' % NEUTRON_PRIVATE_NET_NAME)
        json_body = {'network': {'name': NEUTRON_PRIVATE_NET_NAME,
                    'admin_state_up': True}}
        netw = neutron.create_network(body=json_body)
        net_dict = netw['network']
        network_id = net_dict['id']
        logger.debug("Network '%s' created successfully" % network_id)

        logger.debug('Creating Subnet....')
        json_body = {'subnets': [{'name': NEUTRON_PRIVATE_SUBNET_NAME, 'cidr': NEUTRON_PRIVATE_SUBNET_CIDR,
                           'ip_version': 4, 'network_id': network_id}]}

        subnet = neutron.create_subnet(body=json_body)
        subnet_id = subnet['subnets'][0]['id']
        logger.debug("Subnet '%s' created successfully" % subnet_id)


        logger.debug('Creating Router...')
        json_body = {'router': {'name': ROUTER_NAME, 'admin_state_up': True}}
        router = neutron.create_router(json_body)
        router_id = router['router']['id']
        logger.debug("Router '%s' created successfully" % router_id)

        logger.debug('Adding router to subnet...')
        json_body = {"subnet_id": subnet_id}
        neutron.add_interface_router(router=router_id, body=json_body)
        logger.debug("Interface added successfully.")

    except:
        print "Error:", sys.exc_info()[0]
        return False

    logger.info("Private Neutron network created successfully.")
    return True

def get_network_id(neutron, network_name):
    networks = neutron.list_networks()['networks']
    id  = ''
    for n in networks:
        if n['name'] == network_name:
            id = n['id']
            break
    return id

def check_neutron_net(neutron, net_name):
    for network in neutron.list_networks()['networks']:
        if network['name'] == net_name :
            for subnet in network['subnets']:
                return True
    return False

def delete_neutron_net(neutron):
    #TODO: remove router, ports
    try:
        #https://github.com/isginf/openstack_tools/blob/master/openstack_remove_tenant.py
        for network in neutron.list_networks()['networks']:
            if network['name'] == NEUTRON_PRIVATE_NET_NAME :
                for subnet in network['subnets']:
                    print "Deleting subnet " + subnet
                    neutron.delete_subnet(subnet)
                print "Deleting network " + network['name']
                neutron.delete_neutron_net(network['id'])
    finally:
        return True
    return False





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
    output_file = "output.txt"
    f = open(output_file, 'w+')
    p = subprocess.call(cmd,shell=True, stdout=f, stderr=subprocess.STDOUT)
    f.close()
    f = open(output_file, 'r')
    result = f.read()
    if result != "":
        logger.debug(result)
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


    if not check_credentials():
        logger.error("Please source the openrc credentials and run the script again.")
        #TODO: source the credentials in this script
        exit(-1)

    if args.action == "start":
        action_start()

    if args.action == "check":
        if action_check():
            logger.info("Functest environment correctly installed")
        else:
            logger.info("Functest environment faulty")

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

