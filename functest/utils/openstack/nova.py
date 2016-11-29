#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import os
import time

import novaclient.client as nova_client

import utils
import neutron
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("nova").getLogger()

DEFAULT_API_VERSION = '2'
API_NAME = 'compute'


def get_client_version():
    api_version = os.getenv('OS_COMPUTE_API_VERSION')
    if api_version is not None:
        logger.info("OS_COMPUTE_API_VERSION is set in env as '%s'",
                    api_version)
        return api_version
    return DEFAULT_API_VERSION


def get_nova_client():
    creds_nova = utils.get_credentials('nova')
    return nova_client.Client(get_client_version(), **creds_nova)


def get_instances(nova_client):
    try:
        instances = nova_client.servers.list(search_opts={'all_tenants': 1})
        return instances
    except Exception, e:
        logger.error("Error [get_instances(nova_client)]: %s" % e)
        return None


def get_instance_status(nova_client, instance):
    try:
        instance = nova_client.servers.get(instance.id)
        return instance.status
    except Exception, e:
        logger.error("Error [get_instance_status(nova_client)]: %s" % e)
        return None


def get_instance_by_name(nova_client, instance_name):
    try:
        instance = nova_client.servers.find(name=instance_name)
        return instance
    except Exception, e:
        logger.error("Error [get_instance_by_name(nova_client, '%s')]: %s"
                     % (instance_name, e))
        return None


def get_flavor_id(nova_client, flavor_name):
    flavors = nova_client.flavors.list(detailed=True)
    id = ''
    for f in flavors:
        if f.name == flavor_name:
            id = f.id
            break
    return id


def get_flavor_id_by_ram_range(nova_client, min_ram, max_ram):
    flavors = nova_client.flavors.list(detailed=True)
    id = ''
    for f in flavors:
        if min_ram <= f.ram and f.ram <= max_ram:
            id = f.id
            break
    return id


def create_flavor(nova_client, flavor_name, ram, disk, vcpus, public=True):
    try:
        flavor = nova_client.flavors.create(
            flavor_name, ram, vcpus, disk, is_public=public)
        try:
            extra_specs = ft_utils.get_functest_config(
                'general.flavor_extra_specs')
            flavor.set_keys(extra_specs)
        except ValueError:
            # flavor extra specs are not configured, therefore skip the update
            pass

    except Exception, e:
        logger.error("Error [create_flavor(nova_client, '%s', '%s', '%s', "
                     "'%s')]: %s" % (flavor_name, ram, disk, vcpus, e))
        return None
    return flavor.id


def get_or_create_flavor(flavor_name, ram, disk, vcpus, public=True):
    flavor_exists = False
    nova_client = get_nova_client()

    flavor_id = get_flavor_id(nova_client, flavor_name)
    if flavor_id != '':
        logger.info("Using existing flavor '%s'..." % flavor_name)
        flavor_exists = True
    else:
        logger.info("Creating flavor '%s' with '%s' RAM, '%s' disk size, "
                    "'%s' vcpus..." % (flavor_name, ram, disk, vcpus))
        flavor_id = create_flavor(
            nova_client, flavor_name, ram, disk, vcpus, public=public)
        if not flavor_id:
            logger.error("Failed to create flavor '%s'..." % (flavor_name))
        else:
            logger.debug("Flavor '%s' with ID=%s created successfully."
                         % (flavor_name, flavor_id))

    return flavor_exists, flavor_id


def get_floating_ips(nova_client):
    try:
        floating_ips = nova_client.floating_ips.list()
        return floating_ips
    except Exception, e:
        logger.error("Error [get_floating_ips(nova_client)]: %s" % e)
        return None


def get_hypervisors(nova_client):
    try:
        nodes = []
        hypervisors = nova_client.hypervisors.list()
        for hypervisor in hypervisors:
            if hypervisor.state == "up":
                nodes.append(hypervisor.hypervisor_hostname)
        return nodes
    except Exception, e:
        logger.error("Error [get_hypervisors(nova_client)]: %s" % e)
        return None


def create_instance(flavor_name,
                    image_id,
                    network_id,
                    instance_name="functest-vm",
                    confdrive=True,
                    userdata=None,
                    av_zone='',
                    fixed_ip=None,
                    files=None):
    nova_client = get_nova_client()
    try:
        flavor = nova_client.flavors.find(name=flavor_name)
    except:
        flavors = nova_client.flavors.list()
        logger.error("Error: Flavor '%s' not found. Available flavors are: "
                     "\n%s" % (flavor_name, flavors))
        return None
    if fixed_ip is not None:
        nics = {"net-id": network_id, "v4-fixed-ip": fixed_ip}
    else:
        nics = {"net-id": network_id}
    if userdata is None:
        instance = nova_client.servers.create(
            name=instance_name,
            flavor=flavor,
            image=image_id,
            nics=[nics],
            availability_zone=av_zone,
            files=files
        )
    else:
        instance = nova_client.servers.create(
            name=instance_name,
            flavor=flavor,
            image=image_id,
            nics=[nics],
            config_drive=confdrive,
            userdata=userdata,
            availability_zone=av_zone,
            files=files
        )
    return instance


def create_instance_and_wait_for_active(flavor_name,
                                        image_id,
                                        network_id,
                                        instance_name="",
                                        config_drive=False,
                                        userdata="",
                                        av_zone='',
                                        fixed_ip=None,
                                        files=None):
    SLEEP = 3
    VM_BOOT_TIMEOUT = 180
    nova_client = get_nova_client()
    instance = create_instance(flavor_name,
                               image_id,
                               network_id,
                               instance_name,
                               config_drive,
                               userdata,
                               av_zone=av_zone,
                               fixed_ip=fixed_ip,
                               files=files)
    count = VM_BOOT_TIMEOUT / SLEEP
    for n in range(count, -1, -1):
        status = get_instance_status(nova_client, instance)
        if status.lower() == "active":
            return instance
        elif status.lower() == "error":
            logger.error("The instance %s went to ERROR status."
                         % instance_name)
            return None
        time.sleep(SLEEP)
    logger.error("Timeout booting the instance %s." % instance_name)
    return None


def create_floating_ip(neutron_client):
    extnet_id = neutron.get_external_net_id(neutron_client)
    props = {'floating_network_id': extnet_id}
    try:
        ip_json = neutron_client.create_floatingip({'floatingip': props})
        fip_addr = ip_json['floatingip']['floating_ip_address']
        fip_id = ip_json['floatingip']['id']
    except Exception, e:
        logger.error("Error [create_floating_ip(neutron_client)]: %s" % e)
        return None
    return {'fip_addr': fip_addr, 'fip_id': fip_id}


def add_floating_ip(nova_client, server_id, floatingip_id):
    try:
        nova_client.servers.add_floating_ip(server_id, floatingip_id)
        return True
    except Exception, e:
        logger.error("Error [add_floating_ip(nova_client, '%s', '%s')]: %s"
                     % (server_id, floatingip_id, e))
        return False


def delete_instance(nova_client, instance_id):
    try:
        nova_client.servers.force_delete(instance_id)
        return True
    except Exception, e:
        logger.error("Error [delete_instance(nova_client, '%s')]: %s"
                     % (instance_id, e))
        return False


def delete_floating_ip(nova_client, floatingip_id):
    try:
        nova_client.floating_ips.delete(floatingip_id)
        return True
    except Exception, e:
        logger.error("Error [delete_floating_ip(nova_client, '%s')]: %s"
                     % (floatingip_id, e))
        return False
