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

default_images = ['TestVM']
default_networks = ['net04', 'net04_ext']
default_routers = ['router04']
default_users = ["heat", "heat-cfn", "cinder", "nova", "swift", "glance", "neutron", "admin", "fuel_stats_user"]
default_tenants = ["admin", "services"]


def separator():
    print("-------------------------------------------")

def remove_instances(nova_client):
    logger.info("Removing Nova instances...")
    instances = functest_utils.get_instances(nova_client)
    if len(instances) == 0:
        logger.debug("No instances found.")
        return

    for instance in instances:
        instance_name = getattr(instance, 'name')
        instance_id = getattr(instance, 'id')
        logger.debug("Removing instance '%s', ID=%s ..." % (instance_name,instance_id))
        if functest_utils.delete_instance(nova_client, instance_id):
            logger.debug("  > Done!")
        else:
            logger.info("  > ERROR: There has been a problem removing the instance %s..." % instance_id)


def remove_images(nova_client):
    logger.info("Removing Glance images...")
    images = functest_utils.get_images(nova_client)
    if len(images) == 0:
        logger.debug("No images found.")
        return

    for image in images:
        image_name = getattr(image, 'name')
        image_id = getattr(image, 'id')
        if image_name not in default_images:
            logger.debug("Removing image '%s', ID=%s ..." % (image_name,image_id))
            if functest_utils.delete_glance_image(nova_client, image_id):
                logger.debug("  > Done!")
            else:
                logger.info("  > ERROR: There has been a problem removing the image %s..." % image_id)
        else:
            logger.debug("    > this is a default image and will NOT be deleted.")


def remove_volumes(cinder_client):
    logger.info("Removing Cinder volumes...")
    volumes = functest_utils.get_volumes(cinder_client)
    if len(volumes) == 0:
        logger.debug("No volumes found.")
        return

    for volume in volumes:
        volume_id = getattr(volume, 'id')
        logger.debug("Removing cinder volume %s ..." % volume_id)
        if functest_utils.delete_volume(cinder_client, volume_id):
            logger.debug("  > Done!")
        else:
            logger.info("  > ERROR: There has been a problem removing the volume %s..." % volume_id)


def remove_floatingips(nova_client):
    logger.info("Removing floating IPs...")
    floatingips = functest_utils.get_floating_ips(nova_client)
    if len(floatingips) == 0:
        logger.debug("No floating IPs found.")
        return

    for fip in floatingips:
        fip_id = getattr(fip, 'id')
        logger.debug("Removing floating IP %s ..." % fip_id)
        if functest_utils.delete_floating_ip(nova_client, fip_id):
            logger.debug("  > Done!")
        else:
            logger.info("  > ERROR: There has been a problem removing the floating IP %s..." % fip_id)


def remove_networks(neutron_client):
    logger.info("Removing Neutron objects")
    network_ids = []
    networks = functest_utils.get_network_list(neutron_client)
    logger.debug("Existing networks:")
    for network in networks:
        net_id = network['id']
        net_name = network['name']
        logger.debug(" '%s', ID=%s " %(net_name,net_id))
        if net_name not in default_networks:
            logger.debug("    > this is not a default network and will be deleted.")
            network_ids.append(net_id)
        else:
            logger.debug("    > this is a default network and will NOT be deleted.")


    #remove interfaces router and delete ports
    ports = functest_utils.get_port_list(neutron_client)
    for port in ports:
        if port['network_id'] in network_ids:
            port_id = port['id']
            subnet_id = port['fixed_ips'][0]['subnet_id']
            router_id = port['device_id']
            if port['device_owner'] == 'network:router_interface':
                logger.debug("Detaching port %s (subnet %s) from router %s ..." % (port_id,subnet_id,router_id))
                if functest_utils.remove_interface_router(neutron_client, router_id, subnet_id):
                    logger.debug("  > Done!")
                else:
                    logger.info("  > ERROR: There has been a problem removing the interface %s from router %s..." %(subnet_id,router_id))
                    #print port
            logger.debug("Removing port %s ..." % port_id)
            if functest_utils.delete_neutron_port(neutron_client, port_id):
                logger.debug("  > Done!")
            else:
                logger.info("  > ERROR: There has been a problem removing the port %s ..." %port_id)
                #print port

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
                    #print router

            else:
                logger.debug("Router is not connected to anything. Ready to remove...")
            logger.debug("Removing router %s(%s) ..." % (router_name,router_id))
            if functest_utils.delete_neutron_router(neutron_client, router_id):
                logger.debug("  > Done!")
            else:
                logger.info("  > ERROR: There has been a problem removing the router '%s'(%s)..." % (router_name,router_id))


    #remove networks
    for net_id in network_ids:
        logger.debug("Removing network %s ..." % net_id)
        if functest_utils.delete_neutron_net(neutron_client, net_id):
            logger.debug("  > Done!")
        else:
            logger.info("  > ERROR: There has been a problem removing the network %s..." % net_id)


def remove_security_groups(neutron_client):
    logger.info("Removing Security groups...")
    secgroups = functest_utils.get_security_groups(neutron_client)
    if len(secgroups) == 0:
        logger.debug("No security groups found.")
        return

    for secgroup in secgroups:
        secgroup_name = secgroup['name']
        secgroup_id = secgroup['id']
        logger.debug("'%s', ID=%s " %(secgroup_name,secgroup_id))
        if secgroup_name not in default_security_groups:
            logger.debug(" Removing '%s'..." % secgroup_name)
            if functest_utils.delete_security_group(neutron_client, secgroup_id):
                logger.debug("  > Done!")
            else:
                logger.info("  > ERROR: There has been a problem removing the security group %s..." % secgroup_id)
        else:
            logger.debug("    > this is a default security group and will NOT be deleted.")

def remove_tenants(keystone_client):
    logger.info("Removing Users...")
    users = functest_utils.get_users(keystone_client)
    for user in users:
        user_name = getattr(user, 'name')
        user_id = getattr(user, 'id')
        logger.debug("'%s', ID=%s " %(user_name,user_id))
        if user_name not in default_users:
            logger.debug(" Removing '%s'..." % user_name)
            if functest_utils.delete_user(keystone_client,user_id):
                logger.debug("  > Done!")
            else:
                logger.info("  > ERROR: There has been a problem removing the user '%s'(%s)..." % (user_name,user_id))
        else:
            logger.debug("   > this is a default user and will NOT be deleted.")

    logger.info("Removing Tenants...")
    tenants = functest_utils.get_tenants(keystone_client)
    for tenant in tenants:
        tenant_name=getattr(tenant, 'name')
        tenant_id = getattr(tenant, 'id')
        logger.debug("'%s', ID=%s " %(tenant_name,tenant_id))
        if tenant_name not in default_tenants:
            logger.debug(" Removing '%s'..." % tenant_name)
            if functest_utils.delete_tenant(keystone_client,tenant_id):
                logger.debug("  > Done!")
            else:
                logger.info("  > ERROR: There has been a problem removing the tenant '%s'(%s)..." % (tenant_name,tenant_id))
        else:
            logger.debug("   > this is a default tenant and will NOT be deleted.")



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


    remove_instances(nova_client)
    separator()
    remove_images(nova_client)
    separator()
    remove_volumes(cinder_client)
    separator()
    remove_floatingips(nova_client)
    separator()
    remove_networks(neutron_client)
    separator()
    remove_security_groups(neutron_client)
    separator()
    remove_tenants(keystone_client)
    separator()

    exit(0)


if __name__ == '__main__':
    main()
