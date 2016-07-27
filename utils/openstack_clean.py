#!/usr/bin/env python
#
# Description:
#   Cleans possible leftovers after running functest tests:
#       - Nova instances
#       - Glance images
#       - Cinder volumes
#       - Floating IPs
#       - Neutron networks, subnets and ports
#       - Routers
#       - Users and tenants
#
# Author:
#    jose.lausuch@ericsson.com
#
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import time
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
import yaml


logger = ft_logger.Logger("openstack_clean").getLogger()

OS_SNAPSHOT_FILE = ft_utils.get_parameter_from_yaml(
    "general.openstack.snapshot_file")


def separator():
    logger.debug("-------------------------------------------")


def remove_instances(nova_client, default_instances):
    logger.debug("Removing Nova instances...")
    instances = os_utils.get_instances(nova_client)
    if instances is None or len(instances) == 0:
        logger.debug("No instances found.")
        return

    for instance in instances:
        instance_name = getattr(instance, 'name')
        instance_id = getattr(instance, 'id')
        logger.debug("'%s', ID=%s " % (instance_name, instance_id))
        if (instance_id not in default_instances and
                instance_name not in default_instances.values()):
            logger.debug("Removing instance '%s' ..." % instance_id)
            if os_utils.delete_instance(nova_client, instance_id):
                logger.debug("  > Request sent.")
            else:
                logger.error("There has been a problem removing the "
                             "instance %s..." % instance_id)
        else:
            logger.debug("   > this is a default instance and will "
                         "NOT be deleted.")

    timeout = 50
    while timeout > 0:
        instances = os_utils.get_instances(nova_client)
        for instance in instances:
            instance_id = getattr(instance, 'id')
            if instance_id not in default_instances:
                logger.debug("Waiting for instances to be terminated...")
                timeout -= 1
                time.sleep(1)
                continue
        break


def remove_images(nova_client, default_images):
    logger.debug("Removing Glance images...")
    images = os_utils.get_images(nova_client)
    if images is None or len(images) == 0:
        logger.debug("No images found.")
        return

    for image in images:
        image_name = getattr(image, 'name')
        image_id = getattr(image, 'id')
        logger.debug("'%s', ID=%s " % (image_name, image_id))
        if (image_id not in default_images and
                image_name not in default_images.values()):
            logger.debug("Removing image '%s', ID=%s ..."
                         % (image_name, image_id))
            if os_utils.delete_glance_image(nova_client, image_id):
                logger.debug("  > Done!")
            else:
                logger.error("There has been a problem removing the"
                             "image %s..." % image_id)
        else:
            logger.debug("   > this is a default image and will "
                         "NOT be deleted.")


def remove_volumes(cinder_client, default_volumes):
    logger.debug("Removing Cinder volumes...")
    volumes = os_utils.get_volumes(cinder_client)
    if volumes is None or len(volumes) == 0:
        logger.debug("No volumes found.")
        return

    for volume in volumes:
        volume_id = getattr(volume, 'id')
        volume_name = getattr(volume, 'display_name')
        logger.debug("'%s', ID=%s " % (volume_name, volume_id))
        if (volume_id not in default_volumes and
                volume_name not in default_volumes.values()):
            logger.debug("Removing cinder volume %s ..." % volume_id)
            if os_utils.delete_volume(cinder_client, volume_id):
                logger.debug("  > Done!")
            else:
                logger.debug("Trying forced removal...")
                if os_utils.delete_volume(cinder_client,
                                          volume_id,
                                          forced=True):
                    logger.debug("  > Done!")
                else:
                    logger.error("There has been a problem removing the "
                                 "volume %s..." % volume_id)
        else:
            logger.debug("   > this is a default volume and will "
                         "NOT be deleted.")


def remove_floatingips(nova_client, default_floatingips):
    logger.debug("Removing floating IPs...")
    floatingips = os_utils.get_floating_ips(nova_client)
    if floatingips is None or len(floatingips) == 0:
        logger.debug("No floating IPs found.")
        return

    init_len = len(floatingips)
    deleted = 0
    for fip in floatingips:
        fip_id = getattr(fip, 'id')
        fip_ip = getattr(fip, 'ip')
        logger.debug("'%s', ID=%s " % (fip_ip, fip_id))
        if (fip_id not in default_floatingips and
                fip_ip not in default_floatingips.values()):
            logger.debug("Removing floating IP %s ..." % fip_id)
            if os_utils.delete_floating_ip(nova_client, fip_id):
                logger.debug("  > Done!")
                deleted += 1
            else:
                logger.error("There has been a problem removing the "
                             "floating IP %s..." % fip_id)
        else:
            logger.debug("   > this is a default floating IP and will "
                         "NOT be deleted.")

    timeout = 50
    while timeout > 0:
        floatingips = os_utils.get_floating_ips(nova_client)
        if floatingips is None or len(floatingips) == (init_len - deleted):
            break
        else:
            logger.debug("Waiting for floating ips to be released...")
            timeout -= 1
            time.sleep(1)


def remove_networks(neutron_client, default_networks, default_routers):
    logger.debug("Removing Neutron objects")
    network_ids = []
    networks = os_utils.get_network_list(neutron_client)
    if networks is None:
        logger.debug("There are no networks in the deployment. ")
    else:
        logger.debug("Existing networks:")
        for network in networks:
            net_id = network['id']
            net_name = network['name']
            logger.debug(" '%s', ID=%s " % (net_name, net_id))
            if (net_id in default_networks and
                    net_name in default_networks.values()):
                logger.debug("   > this is a default network and will "
                             "NOT be deleted.")
            elif network['router:external'] is True:
                logger.debug("   > this is an external network and will "
                             "NOT be deleted.")
            else:
                logger.debug("   > this network will be deleted.")
                network_ids.append(net_id)

    # delete ports
    ports = os_utils.get_port_list(neutron_client)
    if ports is None:
        logger.debug("There are no ports in the deployment. ")
    else:
        remove_ports(neutron_client, ports, network_ids)

    # remove routers
    routers = os_utils.get_router_list(neutron_client)
    if routers is None:
        logger.debug("There are no routers in the deployment. ")
    else:
        remove_routers(neutron_client, routers, default_routers)

    # remove networks
    if network_ids is not None:
        for net_id in network_ids:
            logger.debug("Removing network %s ..." % net_id)
            if os_utils.delete_neutron_net(neutron_client, net_id):
                logger.debug("  > Done!")
            else:
                logger.error("There has been a problem removing the "
                             "network %s..." % net_id)


def remove_ports(neutron_client, ports, network_ids):
    for port in ports:
        if port['network_id'] in network_ids:
            port_id = port['id']
            try:
                subnet_id = port['fixed_ips'][0]['subnet_id']
            except:
                logger.debug("  > WARNING: Port %s does not contain fixed_ips"
                             % port_id)
                print port
            router_id = port['device_id']
            if len(port['fixed_ips']) == 0 and router_id == '':
                logger.debug("Removing port %s ..." % port_id)
                if (os_utils.delete_neutron_port(neutron_client, port_id)):
                    logger.debug("  > Done!")
                else:
                    logger.error("There has been a problem removing the "
                                 "port %s ..." % port_id)
                    force_remove_port(neutron_client, port_id)

            elif port['device_owner'] == 'network:router_interface':
                logger.debug("Detaching port %s (subnet %s) from router %s ..."
                             % (port_id, subnet_id, router_id))
                if os_utils.remove_interface_router(
                        neutron_client, router_id, subnet_id):
                    time.sleep(5)  # leave 5 seconds to detach
                    logger.debug("  > Done!")
                else:
                    logger.error("There has been a problem removing the "
                                 "interface %s from router %s..."
                                 % (subnet_id, router_id))
                    force_remove_port(neutron_client, port_id)
            else:
                force_remove_port(neutron_client, port_id)


def force_remove_port(neutron_client, port_id):
    logger.debug("Clearing device_owner for port %s ..." % port_id)
    os_utils.update_neutron_port(neutron_client, port_id,
                                 device_owner='clear')
    logger.debug("Removing port %s ..." % port_id)
    if os_utils.delete_neutron_port(neutron_client, port_id):
        logger.debug("  > Done!")
    else:
        logger.error("There has been a problem removing the port %s..."
                     % port_id)


def remove_routers(neutron_client, routers, default_routers):
    for router in routers:
        router_id = router['id']
        router_name = router['name']
        if (router_id not in default_routers and
                router_name not in default_routers.values()):
            logger.debug("Checking '%s' with ID=(%s) ..." % (router_name,
                                                             router_id))
            if router['external_gateway_info'] is not None:
                logger.debug("Router has gateway to external network."
                             "Removing link...")
                if os_utils.remove_gateway_router(neutron_client, router_id):
                    logger.debug("  > Done!")
                else:
                    logger.error("There has been a problem removing "
                                 "the gateway...")
            else:
                logger.debug("Router is not connected to anything."
                             "Ready to remove...")
            logger.debug("Removing router %s(%s) ..."
                         % (router_name, router_id))
            if os_utils.delete_neutron_router(neutron_client, router_id):
                logger.debug("  > Done!")
            else:
                logger.error("There has been a problem removing the "
                             "router '%s'(%s)..." % (router_name, router_id))


def remove_security_groups(neutron_client, default_security_groups):
    logger.debug("Removing Security groups...")
    secgroups = os_utils.get_security_groups(neutron_client)
    if secgroups is None or len(secgroups) == 0:
        logger.debug("No security groups found.")
        return

    for secgroup in secgroups:
        secgroup_name = secgroup['name']
        secgroup_id = secgroup['id']
        logger.debug("'%s', ID=%s " % (secgroup_name, secgroup_id))
        if secgroup_id not in default_security_groups:
            logger.debug(" Removing '%s'..." % secgroup_name)
            if os_utils.delete_security_group(neutron_client, secgroup_id):
                logger.debug("  > Done!")
            else:
                logger.error("There has been a problem removing the "
                             "security group %s..." % secgroup_id)
        else:
            logger.debug("   > this is a default security group and will NOT "
                         "be deleted.")


def remove_users(keystone_client, default_users):
    logger.debug("Removing Users...")
    users = os_utils.get_users(keystone_client)
    if users is None:
        logger.debug("There are no users in the deployment. ")
        return

    for user in users:
        user_name = getattr(user, 'name')
        user_id = getattr(user, 'id')
        logger.debug("'%s', ID=%s " % (user_name, user_id))
        if (user_id not in default_users and
                user_name not in default_users.values()):
            logger.debug(" Removing '%s'..." % user_name)
            if os_utils.delete_user(keystone_client, user_id):
                logger.debug("  > Done!")
            else:
                logger.error("There has been a problem removing the "
                             "user '%s'(%s)..." % (user_name, user_id))
        else:
            logger.debug("   > this is a default user and will "
                         "NOT be deleted.")


def remove_tenants(keystone_client, default_tenants):
    logger.debug("Removing Tenants...")
    tenants = os_utils.get_tenants(keystone_client)
    if tenants is None:
        logger.debug("There are no tenants in the deployment. ")
        return

    for tenant in tenants:
        tenant_name = getattr(tenant, 'name')
        tenant_id = getattr(tenant, 'id')
        logger.debug("'%s', ID=%s " % (tenant_name, tenant_id))
        if (tenant_id not in default_tenants and
                tenant_name not in default_tenants.values()):
            logger.debug(" Removing '%s'..." % tenant_name)
            if os_utils.delete_tenant(keystone_client, tenant_id):
                logger.debug("  > Done!")
            else:
                logger.error("There has been a problem removing the "
                             "tenant '%s'(%s)..." % (tenant_name, tenant_id))
        else:
            logger.debug("   > this is a default tenant and will "
                         "NOT be deleted.")


def main():
    logger.info("Cleaning OpenStack resources...")

    nova_client = os_utils.get_nova_client()
    neutron_client = os_utils.get_neutron_client()
    keystone_client = os_utils.get_keystone_client()
    cinder_client = os_utils.get_cinder_client()

    try:
        with open(OS_SNAPSHOT_FILE) as f:
            snapshot_yaml = yaml.safe_load(f)
    except Exception:
        logger.info("The file %s does not exist. The OpenStack snapshot must"
                    " be created first. Aborting cleanup." % OS_SNAPSHOT_FILE)
        exit(0)

    default_images = snapshot_yaml.get('images')
    default_instances = snapshot_yaml.get('instances')
    default_volumes = snapshot_yaml.get('volumes')
    default_networks = snapshot_yaml.get('networks')
    default_routers = snapshot_yaml.get('routers')
    default_security_groups = snapshot_yaml.get('secgroups')
    default_floatingips = snapshot_yaml.get('floatingips')
    default_users = snapshot_yaml.get('users')
    default_tenants = snapshot_yaml.get('tenants')

    if not os_utils.check_credentials():
        logger.error("Please source the openrc credentials and run "
                     "the script again.")
        exit(-1)

    remove_instances(nova_client, default_instances)
    separator()
    remove_images(nova_client, default_images)
    separator()
    remove_volumes(cinder_client, default_volumes)
    separator()
    remove_floatingips(nova_client, default_floatingips)
    separator()
    remove_networks(neutron_client, default_networks, default_routers)
    separator()
    remove_security_groups(neutron_client, default_security_groups)
    separator()
    remove_users(keystone_client, default_users)
    separator()
    remove_tenants(keystone_client, default_tenants)
    separator()


if __name__ == '__main__':
    main()
