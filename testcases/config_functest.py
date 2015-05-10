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

from neutronclient.v2_0 import client

actions = ['start', 'check', 'clean']



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



yaml_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/functest.yaml'
name = yaml_url.rsplit('/')[-1]
dest = "./" + name
if not os.path.exists(dest):
    logger.info("Downloading functest.yaml...")
    try:
        response = urllib2.urlopen(yaml_url)
    except (urllib2.HTTPError, urllib2.URLError):
        logger.error("Error in fetching %s" %yaml_url)
        exit(-1)
    with open(dest, 'wb') as f:
        f.write(response.read())
    logger.info("functest.yaml stored in %s" % dest)
else:
    logger.info("functest.yaml found in %s" % dest)


with open('./functest.yaml') as f:
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
NEUTRON_PUBLIC_NAME = functest_yaml.get("general").get("openstack").get("neutron_public_net_name")
NEUTRON_NET_NAME = functest_yaml.get("general").get("openstack").get("neutron_net_name")
NEUTRON_SUBNET_NAME = functest_yaml.get("general").get("openstack").get("neutron_subnet_name")
NEUTRON_RANGE = functest_yaml.get("general").get("openstack").get("neutron_subnet_range")
ROUTER_NAME = functest_yaml.get("general").get("openstack").get("neutron_router_name")

IMAGE_URL = functest_yaml.get("general").get("openstack").get("image_url")
IMAGE_DISK_FORMAT = functest_yaml.get("general").get("openstack").get("image_disk_format")
IMAGE_NAME = functest_yaml.get("general").get("openstack").get("image_name")
IMAGE_FILE_NAME = IMAGE_URL.rsplit('/')[-1]
IMAGE_DOWNLOAD_PATH = FUNCTEST_BASE_DIR + IMAGE_FILE_NAME


def config_functest_start():
    """
    Start the functest environment installation
    """
    #if config_functest_check():
    #    logger.info("Functest environment already installed in %s. Nothing to do." %FUNCTEST_BASE_DIR)
    #    exit(0)
    if not check_internet_connectivity():
        logger.error("There is no Internet connectivity. Please check the network configuration.")
        exit(-1)
    elif not check_credentials():
        logger.error("Please source the openrc credentials and run the script again.")
        #TODO: source the credentials in this script
        exit(-1)
    elif not check_neutron_net(NEUTRON_PUBLIC_NAME):
        #The public network is normally created by default, no need to create a new one
        logger.debug("Public network '%s' not found." % NEUTRON_PUBLIC_NAME)
        logger.error("A public Neutron network is needed for the environment. Please create one.")
        #TODO: source the credentials in this script
        exit(-1)
    else:
        # Clean in case there are left overs
        config_functest_clean()

        logger.info("Starting installationg of functest environment in %s" % FUNCTEST_BASE_DIR)
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

        logger.info("Creating a private Neutron network...")
        logger.debug("Checking if private network '%s' exists..." % NEUTRON_NET_NAME)
        #Now: if exists we don't create it again (the clean command does not clean the neutron network)
        #TODO: this check will not be needed when cleaning the neutron is implemented
        if check_neutron_net(NEUTRON_NET_NAME):
            logger.info("Private network '%s' found. No need to create another one." % NEUTRON_NET_NAME)
        else:
            logger.info("Private network '%s' not found. Creating..." % NEUTRON_NET_NAME)
            if not create_neutron_net():
                logger.error("There has been a problem while creating the Neutron network.")
                #config_functest_clean()
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
    errors_all = False

    logger.info("Checking current functest configuration...")


    logger.debug("Checking directories...")
    errors = False
    dirs = [FUNCTEST_BASE_DIR, RALLY_INSTALLATION_DIR, RALLY_REPO_DIR, RALLY_TEST_DIR, BENCH_TESTS_DIR, VPING_DIR, ODL_DIR]
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
        logger.debug("Rally deployment NOT found.")
        errors_all = True
        logger.debug("...FAIL")
    else:
        logger.debug("...OK")


    logger.debug("Checking Neutron...")
    errors = False
    if not check_neutron_net(NEUTRON_NET_NAME):
        logger.debug("   Private network '%s' NOT found." % NEUTRON_NET_NAME)
        errors = True
        errors_all = True
    else:
        logger.debug("   Private network '%s' found." % NEUTRON_NET_NAME)

    if not check_neutron_net(NEUTRON_PUBLIC_NAME):
        logger.debug("   Public network '%s' NOT found." % NEUTRON_PUBLIC_NAME)
        errors = True
        errors_all = True
    else:
        logger.debug("   Public network '%s' found." % NEUTRON_PUBLIC_NAME)

    if not errors:
        logger.debug("...OK")
    else:
        logger.debug("...FAIL")


    logger.debug("Checking Image...")
    errors = False
    if not os.path.isfile(IMAGE_DOWNLOAD_PATH):
        logger.debug("   Image file '%s' NOT found." % IMAGE_DOWNLOAD_PATH)
        errors = True
        errors_all = True
    else:
        logger.debug("   Image file found in %s" % IMAGE_DOWNLOAD_PATH)

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

    #logger.debug("Deleting Neutron network %s" % NEUTRON_NET_NAME)
    #if not delete_neutron_net() :
    #    logger.error("Error deleting the network. Remove it manually.")

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


def download_tests():
    os.makedirs(VPING_DIR)
    os.makedirs(ODL_DIR)
    os.makedirs(BENCH_TESTS_DIR)

    logger.info("Downloading functest.yaml...")
    yaml_url = 'https://git.opnfv.org/cgit/functest/plain/testcases/functest.yaml'
    if not download_url(yaml_url,FUNCTEST_BASE_DIR):
        logger.error("Unable to download the configuration file functest.yaml")
        return False

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


def create_neutron_net():
    credentials = get_credentials()
    neutron = client.Client(**credentials)
    try:
        neutron.format = 'json'
        logger.debug('Creating Neutron network %s...' % NEUTRON_NET_NAME)
        json_body = {'network': {'name': NEUTRON_NET_NAME,
                    'admin_state_up': True}}
        netw = neutron.create_network(body=json_body)
        net_dict = netw['network']
        network_id = net_dict['id']
        logger.debug("Network '%s' created successfully" % network_id)

        logger.debug('Creating Subnet....')
        json_body = {'subnets': [{'cidr': NEUTRON_RANGE,
                           'ip_version': 4, 'network_id': network_id}]}
        subnet = neutron.create_subnet(body=json_body)
        logger.debug("Subnet '%s' created successfully" % subnet)

        logger.debug('Creating Router...')
        json_body = {'router': {'name': ROUTER_NAME, 'admin_state_up': True}}
        router = neutron.create_router(json_body)
        logger.debug("Router '%s' created successfully" % router)
        router_id = router['router']['id']

        logger.debug('Creating Port')
        json_body = {'port': {
         'admin_state_up': True,
         'device_id': router_id,
         'name': 'port1',
         'network_id': network_id,
        }}
        response = neutron.create_port(body=json_body)
        logger.debug("Port created successfully.")

        logger.debug('Setting up gateway...')
        public_network_id = get_network_id(neutron,NEUTRON_PUBLIC_NAME)
        json_body = {'network_id': public_network_id, 'enable_snat' :  True}
        gateway = neutron.add_gateway_router(router_id,body=json_body)
        logger.debug("Gateway '%s' added successfully" % gateway)
    except:
        logger.error("There has been a problem when creating the Neutron network.")
        return False
    finally:
        logger.info("Neutron network created successfully.")
        return True

    return False

def get_network_id(neutron_client, network_name):
    networks = neutron_client.list_networks()['networks']
    id  = ''
    for n in networks:
        if n['name'] == network_name:
            id = n['id']
            break
    return id

def check_neutron_net(net_name):
    credentials = get_credentials()
    neutron = client.Client(**credentials)
    for network in neutron.list_networks()['networks']:
        if network['name'] == net_name :
            for subnet in network['subnets']:
                return True
    return False

def delete_neutron_net():
    #TODO: remove router, ports
    credentials = get_credentials()
    neutron = client.Client(**credentials)
    try:
        #https://github.com/isginf/openstack_tools/blob/master/openstack_remove_tenant.py
        for network in neutron.list_networks()['networks']:
            if network['name'] == NEUTRON_NET_NAME :
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

