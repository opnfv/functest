#!/usr/bin/env python
#
# Description:
#   Cleans possible leftovers after running functest tests:
#       - Nova instances
#       - Neutron networks, subnets and ports
#       - Routers
#       - Cinder volumes
#       - Glance images
#
# Author:
#    jose.lausuch@ericsson.com
#


import re, json, os, urllib2, argparse, logging, shutil, yaml, subprocess, sys, getpass
import functest_utils
from git import Repo
from os import stat
from pwd import getpwuid
from neutronclient.v2_0 import client as neutronclient

parser = argparse.ArgumentParser()
parser.add_argument("repo_path", help="Path to the repository")
parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
args = parser.parse_args()


""" logging configuration """
logger = logging.getLogger('clean_openstack')
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






def main():

    if not functest_utils.check_credentials():
        logger.error("Please source the openrc credentials and run the script again.")
        exit(-1)

    # Remove instances
    logger.info("Removing Nova nstances")
    instances = functest_utils.get_instances(nova_client)
    for instance in instances:
        id = getattr(instance, 'id')
        instance.force_delete()
        logger.info("Deleted instance " + id + "...")

    # Remove images
    logger.info("Removing Glance images")
    images = functest_utils.get_images(nova_client)
    for image in images:
        id = getattr(image, 'id')
        image.delete()
        logger.info("Deleted image " + id + "...")

    # Remove volumes
    logger.info("Removing Cinder volumes")
    volumes = functest_utils.get_cinder_volumes()
    for volume in volumes:
        functest_utils.delete_cinder_volume(volume['id'])

    # Remove networks
    logger.info("Removing Neutron networks")
    networks = functest_utils.get_neutron_networks()
    for network in networks:
        #for each port in network
            #if dhcp_router
                #remove dhcp_router tag
            #delete port
        #for each subnet in network
            #remove subnet
        pass

    # Remove users
    logger.info("Removing Users")
    users = functest_utils.get_users()
    for user in users:
        name=getattr(user, 'name')
        if name not in ["heat", "heat-cfn", "cinder", "nova", "swift", "glance", "neutron", "admin", "fuel_stats_user"]:
            user.delete()


    logger.info("Removing Tenants")
    tenants = functest_utils.get_tenants(keystone_client)
    for tenant in tenants:
        name=getattr(tenant, 'name')
        if name not in ["admin", "services"]:
            tenant.delete()

    exit(0)


if __name__ == '__main__':
    main()
