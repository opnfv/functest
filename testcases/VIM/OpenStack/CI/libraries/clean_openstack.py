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
from os import stat
from pwd import getpwuid

import novaclient.v2.client as novaclient
from neutronclient.v2_0 import client as neutronclient
from keystoneclient.v2_0 import client as keystoneclient
from cinderclient import client as cinderclient

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

sys.path.append("../testcases/")
import functest_utils

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    creds_nova = functest_utils.get_credentials("nova")
    nova_client = novaclient.Client(**creds_nova)

    creds_neutron = functest_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)

    creds_keystone = functest_utils.get_credentials("keystone")
    keystone_client = keystoneclient.Client(**creds_keystone)

    creds_cinder = functest_utils.get_credentials("cinder")
    #cinder_client = cinderclient.Client(**creds_cinder)
    cinder_client = cinderclient.Client('1',creds_cinder['username'],creds_cinder['api_key'],creds_cinder['project_id'],creds_cinder['auth_url'],service_type="volume")

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
    volumes = functest_utils.get_volumes(cinder_client)
    for volume in volumes:
        volume.delete()

    # Remove networks
    logger.info("Removing Neutron objects")
    network_ids = []
    networks = functest_utils.get_network_list()
    for network in networks:
        if network['name'] not in ["net04", "net04_ext"]:
            network_ids.append(network['id'])
    
    networks = functest_utils.get_port_list()        
    for ports in 
        #for each port in network
            #if dhcp_router
                #remove dhcp_router tag
            #delete port
        #for each subnet in network
            #remove subnet
        #pass
    logger.info("Removing Routers")
    routers = functest_utils.get_neutron_routers()
    for router in routers:
        if router['name'] not in ["net04"]:
            id = router['id']
            functest_utils.delete_neutron_router(neutron_client, id)
            
            
            
    # Remove users
    logger.info("Removing Users")
    users = functest_utils.get_users(keystone_client)
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
