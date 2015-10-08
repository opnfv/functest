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

sys.path.append(args.repo_path + "testcases/")
import functest_utils

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

default_networks = ['net04', 'net04_ext']
default_routers = ['router04']


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
    networks = functest_utils.get_network_list(neutron_client)
    logger.debug("Existing networks:")
    for network in networks:
        net_id = network['id']
        net_name = network['name']
        logger.debug(" - %s, ID=%s " %(net_name,net_id))
        if net_name not in default_networks:
            logger.debug("   > '%s'(%s) this is not a default network and will be deleted." % (net_name,net_id))
            network_ids.append(net_id)


    #remove interfaces router and delete ports
    ports = functest_utils.get_port_list(neutron_client)
    for port in ports:
        if port['network_id'] in network_ids:
            port_id = port['device_id']
            subnet_id = port['fixed_ips'][0]['subnet_id']
            router_id = port['device_id']
            if port['device_owner'] == 'network:router_interface':
                logger.debug("Detaching port %s (subnet %s) from router %s ..." % (port_id,subnet_id,router_id))
                if functest_utils.remove_interface_router(neutron_client, router_id, subnet_id):
                    logger.debug("  > Done!")
                else:
                    logger.info("  > ERROR: There has been a problem removing the interface %s from router %s..." %(subnet_id,router_id))
                    print port
            logger.debug("Removing port %s ..." % port_id)
            if functest_utils.delete_neutron_port(neutron_client, port_id):
                logger.debug("  > Done!")
            else:
                logger.info("  > ERROR: There has been a problem removing the port %s ..." %port_id)
                print port

    #remove routers
    routers = functest_utils.get_router_list(neutron_client)
    for router in routers:
        router_id = router['id']
        router_name = router['name']
        if router_name not in default_routers:
            logger.debug("Checking '%s' with ID=(%s) ..." % (router_name,router_id))
            if router['external_gateway_info'] != None:
                logger.debug("Router has gateway to external network. Removing link...")
                if functest_utils.remove_gateway_router(neutron_client, router_id):
                    logger.debug("  > Done!")
                else:
                    logger.info("  > ERROR: There has been a problem removing the gateway...")
                    print router

            else:
                logger.debug("Router is not connected to anything. Ready to remove...")
            logger.debug("Removing router %s(%s) ..." % (router_name,router_id))
            if functest_utils.delete_neutron_router(neutron_client, router_id):
                logger.debug("  > Done!")
            else:
                logger.info("  > ERROR: There has been a problem removing the router '%s'(%s)..." % (router_name,router_id))


    #remove networks
    for net_id in network_ids:
        if functest_utils.delete_neutron_net(neutron_client, net_id):
            logger.debug("  > Done!")
        else:
            logger.info("  > ERROR: There has been a problem removing the network %s..." % net_id)



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
