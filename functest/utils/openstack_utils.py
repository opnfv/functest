#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# valentin.boucher@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import os
import os.path
import re
import sys
import time

from keystoneauth1 import loading
from keystoneauth1 import session
from cinderclient import client as cinderclient
from glanceclient import client as glanceclient
from heatclient import client as heatclient
from novaclient import client as novaclient
from keystoneclient import client as keystoneclient
from neutronclient.neutron import client as neutronclient

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils

logger = ft_logger.Logger("openstack_utils").getLogger()

DEFAULT_API_VERSION = '2'
DEFAULT_HEAT_API_VERSION = '1'


# *********************************************
#   CREDENTIALS
# *********************************************
class MissingEnvVar(Exception):

    def __init__(self, var):
        self.var = var

    def __str__(self):
        return str.format("Please set the mandatory env var: {}", self.var)


def is_keystone_v3():
    keystone_api_version = os.getenv('OS_IDENTITY_API_VERSION')
    if (keystone_api_version is None or
            keystone_api_version == '2'):
        return False
    else:
        return True


def get_rc_env_vars():
    env_vars = ['OS_AUTH_URL', 'OS_USERNAME', 'OS_PASSWORD']
    if is_keystone_v3():
        env_vars.extend(['OS_PROJECT_NAME',
                         'OS_USER_DOMAIN_NAME',
                         'OS_PROJECT_DOMAIN_NAME'])
    else:
        env_vars.extend(['OS_TENANT_NAME'])
    return env_vars


def check_credentials():
    """
    Check if the OpenStack credentials (openrc) are sourced
    """
    env_vars = get_rc_env_vars()
    return all(map(lambda v: v in os.environ and os.environ[v], env_vars))


def get_env_cred_dict():
    env_cred_dict = {
        'OS_USERNAME': 'username',
        'OS_PASSWORD': 'password',
        'OS_AUTH_URL': 'auth_url',
        'OS_TENANT_NAME': 'tenant_name',
        'OS_USER_DOMAIN_NAME': 'user_domain_name',
        'OS_PROJECT_DOMAIN_NAME': 'project_domain_name',
        'OS_PROJECT_NAME': 'project_name',
        'OS_ENDPOINT_TYPE': 'endpoint_type',
        'OS_REGION_NAME': 'region_name',
        'OS_CACERT': 'https_cacert'
    }
    return env_cred_dict


def get_credentials(other_creds={}):
    """Returns a creds dictionary filled with parsed from env
    """
    creds = {}
    env_vars = get_rc_env_vars()
    env_cred_dict = get_env_cred_dict()

    for envvar in env_vars:
        if os.getenv(envvar) is None:
            raise MissingEnvVar(envvar)
        else:
            creds_key = env_cred_dict.get(envvar)
            creds.update({creds_key: os.getenv(envvar)})

    if 'tenant' in other_creds.keys():
        if is_keystone_v3():
            tenant = 'project_name'
        else:
            tenant = 'tenant_name'
        other_creds[tenant] = other_creds.pop('tenant')

    creds.update(other_creds)

    return creds


def source_credentials(rc_file):
    with open(rc_file, "r") as f:
        for line in f:
            var = line.rstrip('"\n').replace('export ', '').split("=")
            # The two next lines should be modified as soon as rc_file
            # conforms with common rules. Be aware that it could induce
            # issues if value starts with '
            key = re.sub(r'^["\' ]*|[ \'"]*$', '', var[0])
            value = re.sub(r'^["\' ]*|[ \'"]*$', '', "".join(var[1:]))
            os.environ[key] = value


def get_credentials_for_rally():
    creds = get_credentials()
    env_cred_dict = get_env_cred_dict()
    rally_conf = {"type": "ExistingCloud", "admin": {}}
    for key in creds:
        if key == 'auth_url':
            rally_conf[key] = creds[key]
        else:
            rally_conf['admin'][key] = creds[key]

    endpoint_types = [('internalURL', 'internal'),
                      ('publicURL', 'public'), ('adminURL', 'admin')]

    endpoint_type = os.getenv('OS_ENDPOINT_TYPE')
    if endpoint_type is not None:
        cred_key = env_cred_dict.get('OS_ENDPOINT_TYPE')
        for k, v in endpoint_types:
            if endpoint_type == k:
                rally_conf[cred_key] = v

    region_name = os.getenv('OS_REGION_NAME')
    if region_name is not None:
        cred_key = env_cred_dict.get('OS_REGION_NAME')
        rally_conf[cred_key] = region_name

    cacert = os.getenv('OS_CACERT')
    if cacert is not None:
        cred_key = env_cred_dict.get('OS_CACERT')
        rally_conf[cred_key] = cacert
    return rally_conf


def get_session_auth(other_creds={}):
    loader = loading.get_plugin_loader('password')
    creds = get_credentials(other_creds)
    auth = loader.load_from_options(**creds)
    return auth


def get_endpoint(service_type, endpoint_type='publicURL'):
    auth = get_session_auth()
    return get_session().get_endpoint(auth=auth,
                                      service_type=service_type,
                                      endpoint_type=endpoint_type)


def get_session(other_creds={}):
    auth = get_session_auth(other_creds)
    cacert = os.getenv('OS_CACERT')
    if cacert is not None:
        if not os.path.isfile(cacert):
            raise Exception("The 'OS_CACERT' environment"
                            "variable is set to %s but the file"
                            "does not exist.", cacert)

    return session.Session(auth=auth, verify=cacert)


# *********************************************
#   CLIENTS
# *********************************************
def get_keystone_client_version():
    api_version = os.getenv('OS_IDENTITY_API_VERSION')
    if api_version is not None:
        logger.info("OS_IDENTITY_API_VERSION is set in env as '%s'",
                    api_version)
        return api_version
    return DEFAULT_API_VERSION


def get_keystone_client(other_creds={}):
    sess = get_session(other_creds)
    return keystoneclient.Client(get_keystone_client_version(), session=sess)


def get_nova_client_version():
    api_version = os.getenv('OS_COMPUTE_API_VERSION')
    if api_version is not None:
        logger.info("OS_COMPUTE_API_VERSION is set in env as '%s'",
                    api_version)
        return api_version
    return DEFAULT_API_VERSION


def get_nova_client(other_creds={}):
    sess = get_session(other_creds)
    return novaclient.Client(get_nova_client_version(), session=sess)


def get_cinder_client_version():
    api_version = os.getenv('OS_VOLUME_API_VERSION')
    if api_version is not None:
        logger.info("OS_VOLUME_API_VERSION is set in env as '%s'",
                    api_version)
        return api_version
    return DEFAULT_API_VERSION


def get_cinder_client(other_creds={}):
    sess = get_session(other_creds)
    return cinderclient.Client(get_cinder_client_version(), session=sess)


def get_neutron_client_version():
    api_version = os.getenv('OS_NETWORK_API_VERSION')
    if api_version is not None:
        logger.info("OS_NETWORK_API_VERSION is set in env as '%s'",
                    api_version)
        return api_version
    return DEFAULT_API_VERSION


def get_neutron_client(other_creds={}):
    sess = get_session(other_creds)
    return neutronclient.Client(get_neutron_client_version(), session=sess)


def get_glance_client_version():
    api_version = os.getenv('OS_IMAGE_API_VERSION')
    if api_version is not None:
        logger.info("OS_IMAGE_API_VERSION is set in env as '%s'", api_version)
        return api_version
    return DEFAULT_API_VERSION


def get_glance_client(other_creds={}):
    sess = get_session(other_creds)
    return glanceclient.Client(get_glance_client_version(), session=sess)


def get_heat_client_version():
    api_version = os.getenv('OS_ORCHESTRATION_API_VERSION')
    if api_version is not None:
        logger.info("OS_ORCHESTRATION_API_VERSION is set in env as '%s'",
                    api_version)
        return api_version
    return DEFAULT_HEAT_API_VERSION


def get_heat_client(other_creds={}):
    sess = get_session(other_creds)
    return heatclient.Client(get_heat_client_version(), session=sess)


# *********************************************
#   NOVA
# *********************************************
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


def get_aggregates(nova_client):
    try:
        aggregates = nova_client.aggregates.list()
        return aggregates
    except Exception, e:
        logger.error("Error [get_aggregates(nova_client)]: %s" % e)
        return None


def get_aggregate_id(nova_client, aggregate_name):
    try:
        aggregates = get_aggregates(nova_client)
        _id = [ag.id for ag in aggregates if ag.name == aggregate_name][0]
        return _id
    except Exception, e:
        logger.error("Error [get_aggregate_id(nova_client, %s)]:"
                     " %s" % (aggregate_name, e))
        return None


def get_availability_zones(nova_client):
    try:
        availability_zones = nova_client.availability_zones.list()
        return availability_zones
    except Exception, e:
        logger.error("Error [get_availability_zones(nova_client)]: %s" % e)
        return None


def get_availability_zone_names(nova_client):
    try:
        az_names = [az.zoneName for az in get_availability_zones(nova_client)]
        return az_names
    except Exception, e:
        logger.error("Error [get_availability_zone_names(nova_client)]:"
                     " %s" % e)
        return None


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


def create_aggregate(nova_client, aggregate_name, av_zone):
    try:
        nova_client.aggregates.create(aggregate_name, av_zone)
        return True
    except Exception, e:
        logger.error("Error [create_aggregate(nova_client, %s, %s)]: %s"
                     % (aggregate_name, av_zone, e))
        return None


def add_host_to_aggregate(nova_client, aggregate_name, compute_host):
    try:
        aggregate_id = get_aggregate_id(nova_client, aggregate_name)
        nova_client.aggregates.add_host(aggregate_id, compute_host)
        return True
    except Exception, e:
        logger.error("Error [add_host_to_aggregate(nova_client, %s, %s)]: %s"
                     % (aggregate_name, compute_host, e))
        return None


def create_aggregate_with_host(
        nova_client, aggregate_name, av_zone, compute_host):
    try:
        create_aggregate(nova_client, aggregate_name, av_zone)
        add_host_to_aggregate(nova_client, aggregate_name, compute_host)
        return True
    except Exception, e:
        logger.error("Error [create_aggregate_with_host("
                     "nova_client, %s, %s, %s)]: %s"
                     % (aggregate_name, av_zone, compute_host, e))
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
    extnet_id = get_external_net_id(neutron_client)
    props = {'floating_network_id': extnet_id}
    try:
        ip_json = neutron_client.create_floatingip({'floatingip': props})
        fip_addr = ip_json['floatingip']['floating_ip_address']
        fip_id = ip_json['floatingip']['id']
    except Exception, e:
        logger.error("Error [create_floating_ip(neutron_client)]: %s" % e)
        return None
    return {'fip_addr': fip_addr, 'fip_id': fip_id}


def add_floating_ip(nova_client, server_id, floatingip_addr):
    try:
        nova_client.servers.add_floating_ip(server_id, floatingip_addr)
        return True
    except Exception, e:
        logger.error("Error [add_floating_ip(nova_client, '%s', '%s')]: %s"
                     % (server_id, floatingip_addr, e))
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


def remove_host_from_aggregate(nova_client, aggregate_name, compute_host):
    try:
        aggregate_id = get_aggregate_id(nova_client, aggregate_name)
        nova_client.aggregates.remove_host(aggregate_id, compute_host)
        return True
    except Exception, e:
        logger.error("Error [remove_host_from_aggregate(nova_client, %s, %s)]:"
                     " %s" % (aggregate_name, compute_host, e))
        return False


def remove_hosts_from_aggregate(nova_client, aggregate_name):
    aggregate_id = get_aggregate_id(nova_client, aggregate_name)
    hosts = nova_client.aggregates.get(aggregate_id).hosts
    assert(
        all(remove_host_from_aggregate(nova_client, aggregate_name, host)
            for host in hosts))


def delete_aggregate(nova_client, aggregate_name):
    try:
        remove_hosts_from_aggregate(nova_client, aggregate_name)
        nova_client.aggregates.delete(aggregate_name)
        return True
    except Exception, e:
        logger.error("Error [delete_aggregate(nova_client, %s)]: %s"
                     % (aggregate_name, e))
        return False


# *********************************************
#   NEUTRON
# *********************************************
def get_network_list(neutron_client):
    network_list = neutron_client.list_networks()['networks']
    if len(network_list) == 0:
        return None
    else:
        return network_list


def get_router_list(neutron_client):
    router_list = neutron_client.list_routers()['routers']
    if len(router_list) == 0:
        return None
    else:
        return router_list


def get_port_list(neutron_client):
    port_list = neutron_client.list_ports()['ports']
    if len(port_list) == 0:
        return None
    else:
        return port_list


def get_network_id(neutron_client, network_name):
    networks = neutron_client.list_networks()['networks']
    id = ''
    for n in networks:
        if n['name'] == network_name:
            id = n['id']
            break
    return id


def get_subnet_id(neutron_client, subnet_name):
    subnets = neutron_client.list_subnets()['subnets']
    id = ''
    for s in subnets:
        if s['name'] == subnet_name:
            id = s['id']
            break
    return id


def get_router_id(neutron_client, router_name):
    routers = neutron_client.list_routers()['routers']
    id = ''
    for r in routers:
        if r['name'] == router_name:
            id = r['id']
            break
    return id


def get_private_net(neutron_client):
    # Checks if there is an existing shared private network
    networks = neutron_client.list_networks()['networks']
    if len(networks) == 0:
        return None
    for net in networks:
        if (net['router:external'] is False) and (net['shared'] is True):
            return net
    return None


def get_external_net(neutron_client):
    for network in neutron_client.list_networks()['networks']:
        if network['router:external']:
            return network['name']
    return None


def get_external_net_id(neutron_client):
    for network in neutron_client.list_networks()['networks']:
        if network['router:external']:
            return network['id']
    return None


def check_neutron_net(neutron_client, net_name):
    for network in neutron_client.list_networks()['networks']:
        if network['name'] == net_name:
            for subnet in network['subnets']:
                return True
    return False


def create_neutron_net(neutron_client, name):
    json_body = {'network': {'name': name,
                             'admin_state_up': True}}
    try:
        network = neutron_client.create_network(body=json_body)
        network_dict = network['network']
        return network_dict['id']
    except Exception, e:
        logger.error("Error [create_neutron_net(neutron_client, '%s')]: %s"
                     % (name, e))
        return None


def create_neutron_subnet(neutron_client, name, cidr, net_id):
    json_body = {'subnets': [{'name': name, 'cidr': cidr,
                              'ip_version': 4, 'network_id': net_id}]}
    try:
        subnet = neutron_client.create_subnet(body=json_body)
        return subnet['subnets'][0]['id']
    except Exception, e:
        logger.error("Error [create_neutron_subnet(neutron_client, '%s', "
                     "'%s', '%s')]: %s" % (name, cidr, net_id, e))
        return None


def create_neutron_router(neutron_client, name):
    json_body = {'router': {'name': name, 'admin_state_up': True}}
    try:
        router = neutron_client.create_router(json_body)
        return router['router']['id']
    except Exception, e:
        logger.error("Error [create_neutron_router(neutron_client, '%s')]: %s"
                     % (name, e))
        return None


def create_neutron_port(neutron_client, name, network_id, ip):
    json_body = {'port': {
                 'admin_state_up': True,
                 'name': name,
                 'network_id': network_id,
                 'fixed_ips': [{"ip_address": ip}]
                 }}
    try:
        port = neutron_client.create_port(body=json_body)
        return port['port']['id']
    except Exception, e:
        logger.error("Error [create_neutron_port(neutron_client, '%s', '%s', "
                     "'%s')]: %s" % (name, network_id, ip, e))
        return None


def update_neutron_net(neutron_client, network_id, shared=False):
    json_body = {'network': {'shared': shared}}
    try:
        neutron_client.update_network(network_id, body=json_body)
        return True
    except Exception, e:
        logger.error("Error [update_neutron_net(neutron_client, '%s', '%s')]: "
                     "%s" % (network_id, str(shared), e))
        return False


def update_neutron_port(neutron_client, port_id, device_owner):
    json_body = {'port': {
                 'device_owner': device_owner,
                 }}
    try:
        port = neutron_client.update_port(port=port_id,
                                          body=json_body)
        return port['port']['id']
    except Exception, e:
        logger.error("Error [update_neutron_port(neutron_client, '%s', '%s')]:"
                     " %s" % (port_id, device_owner, e))
        return None


def add_interface_router(neutron_client, router_id, subnet_id):
    json_body = {"subnet_id": subnet_id}
    try:
        neutron_client.add_interface_router(router=router_id, body=json_body)
        return True
    except Exception, e:
        logger.error("Error [add_interface_router(neutron_client, '%s', "
                     "'%s')]: %s" % (router_id, subnet_id, e))
        return False


def add_gateway_router(neutron_client, router_id):
    ext_net_id = get_external_net_id(neutron_client)
    router_dict = {'network_id': ext_net_id}
    try:
        neutron_client.add_gateway_router(router_id, router_dict)
        return True
    except Exception, e:
        logger.error("Error [add_gateway_router(neutron_client, '%s')]: %s"
                     % (router_id, e))
        return False


def delete_neutron_net(neutron_client, network_id):
    try:
        neutron_client.delete_network(network_id)
        return True
    except Exception, e:
        logger.error("Error [delete_neutron_net(neutron_client, '%s')]: %s"
                     % (network_id, e))
        return False


def delete_neutron_subnet(neutron_client, subnet_id):
    try:
        neutron_client.delete_subnet(subnet_id)
        return True
    except Exception, e:
        logger.error("Error [delete_neutron_subnet(neutron_client, '%s')]: %s"
                     % (subnet_id, e))
        return False


def delete_neutron_router(neutron_client, router_id):
    try:
        neutron_client.delete_router(router=router_id)
        return True
    except Exception, e:
        logger.error("Error [delete_neutron_router(neutron_client, '%s')]: %s"
                     % (router_id, e))
        return False


def delete_neutron_port(neutron_client, port_id):
    try:
        neutron_client.delete_port(port_id)
        return True
    except Exception, e:
        logger.error("Error [delete_neutron_port(neutron_client, '%s')]: %s"
                     % (port_id, e))
        return False


def remove_interface_router(neutron_client, router_id, subnet_id):
    json_body = {"subnet_id": subnet_id}
    try:
        neutron_client.remove_interface_router(router=router_id,
                                               body=json_body)
        return True
    except Exception, e:
        logger.error("Error [remove_interface_router(neutron_client, '%s', "
                     "'%s')]: %s" % (router_id, subnet_id, e))
        return False


def remove_gateway_router(neutron_client, router_id):
    try:
        neutron_client.remove_gateway_router(router_id)
        return True
    except Exception, e:
        logger.error("Error [remove_gateway_router(neutron_client, '%s')]: %s"
                     % (router_id, e))
        return False


def create_network_full(neutron_client,
                        net_name,
                        subnet_name,
                        router_name,
                        cidr):

    # Check if the network already exists
    network_id = get_network_id(neutron_client, net_name)
    subnet_id = get_subnet_id(neutron_client, subnet_name)
    router_id = get_router_id(neutron_client, router_name)

    if network_id != '' and subnet_id != '' and router_id != '':
        logger.info("A network with name '%s' already exists..." % net_name)
    else:
        neutron_client.format = 'json'
        logger.info('Creating neutron network %s...' % net_name)
        network_id = create_neutron_net(neutron_client, net_name)

        if not network_id:
            return False

        logger.debug("Network '%s' created successfully" % network_id)
        logger.debug('Creating Subnet....')
        subnet_id = create_neutron_subnet(neutron_client, subnet_name,
                                          cidr, network_id)
        if not subnet_id:
            return None

        logger.debug("Subnet '%s' created successfully" % subnet_id)
        logger.debug('Creating Router...')
        router_id = create_neutron_router(neutron_client, router_name)

        if not router_id:
            return None

        logger.debug("Router '%s' created successfully" % router_id)
        logger.debug('Adding router to subnet...')

        if not add_interface_router(neutron_client, router_id, subnet_id):
            return None

        logger.debug("Interface added successfully.")

        logger.debug('Adding gateway to router...')
        if not add_gateway_router(neutron_client, router_id):
            return None

        logger.debug("Gateway added successfully.")

    network_dic = {'net_id': network_id,
                   'subnet_id': subnet_id,
                   'router_id': router_id}
    return network_dic


def create_shared_network_full(net_name, subnt_name, router_name, subnet_cidr):
    neutron_client = get_neutron_client()

    network_dic = create_network_full(neutron_client,
                                      net_name,
                                      subnt_name,
                                      router_name,
                                      subnet_cidr)
    if network_dic:
        if not update_neutron_net(neutron_client,
                                  network_dic['net_id'],
                                  shared=True):
            logger.error("Failed to update network %s..." % net_name)
            return None
        else:
            logger.debug("Network '%s' is available..." % net_name)
    else:
        logger.error("Network %s creation failed" % net_name)
        return None
    return network_dic


def create_bgpvpn(neutron_client, **kwargs):
    # route_distinguishers
    # route_targets
    json_body = {"bgpvpn": kwargs}
    return neutron_client.create_bgpvpn(json_body)


def create_network_association(neutron_client, bgpvpn_id, neutron_network_id):
    json_body = {"network_association": {"network_id": neutron_network_id}}
    return neutron_client.create_network_association(bgpvpn_id, json_body)


def create_router_association(neutron_client, bgpvpn_id, router_id):
    json_body = {"router_association": {"router_id": router_id}}
    return neutron_client.create_router_association(bgpvpn_id, json_body)


def update_bgpvpn(neutron_client, bgpvpn_id, **kwargs):
    json_body = {"bgpvpn": kwargs}
    return neutron_client.update_bgpvpn(bgpvpn_id, json_body)


def delete_bgpvpn(neutron_client, bgpvpn_id):
    return neutron_client.delete_bgpvpn(bgpvpn_id)


def get_bgpvpn(neutron_client, bgpvpn_id):
    return neutron_client.show_bgpvpn(bgpvpn_id)


def get_bgpvpn_routers(neutron_client, bgpvpn_id):
    return get_bgpvpn(neutron_client, bgpvpn_id)['bgpvpn']['routers']


def get_bgpvpn_networks(neutron_client, bgpvpn_id):
    return get_bgpvpn(neutron_client, bgpvpn_id)['bgpvpn']['networks']

# *********************************************
#   SEC GROUPS
# *********************************************


def get_security_groups(neutron_client):
    try:
        security_groups = neutron_client.list_security_groups()[
            'security_groups']
        return security_groups
    except Exception, e:
        logger.error("Error [get_security_groups(neutron_client)]: %s" % e)
        return None


def get_security_group_id(neutron_client, sg_name):
    security_groups = get_security_groups(neutron_client)
    id = ''
    for sg in security_groups:
        if sg['name'] == sg_name:
            id = sg['id']
            break
    return id


def create_security_group(neutron_client, sg_name, sg_description):
    json_body = {'security_group': {'name': sg_name,
                                    'description': sg_description}}
    try:
        secgroup = neutron_client.create_security_group(json_body)
        return secgroup['security_group']
    except Exception, e:
        logger.error("Error [create_security_group(neutron_client, '%s', "
                     "'%s')]: %s" % (sg_name, sg_description, e))
        return None


def create_secgroup_rule(neutron_client, sg_id, direction, protocol,
                         port_range_min=None, port_range_max=None):
    # We create a security group in 2 steps
    # 1 - we check the format and set the json body accordingly
    # 2 - we call neturon client to create the security group

    # Format check
    json_body = {'security_group_rule': {'direction': direction,
                                         'security_group_id': sg_id,
                                         'protocol': protocol}}
    # parameters may be
    # - both None => we do nothing
    # - both Not None => we add them to the json description
    # but one cannot be None is the other is not None
    if (port_range_min is not None and port_range_max is not None):
        # add port_range in json description
        json_body['security_group_rule']['port_range_min'] = port_range_min
        json_body['security_group_rule']['port_range_max'] = port_range_max
        logger.debug("Security_group format set (port range included)")
    else:
        # either both port range are set to None => do nothing
        # or one is set but not the other => log it and return False
        if port_range_min is None and port_range_max is None:
            logger.debug("Security_group format set (no port range mentioned)")
        else:
            logger.error("Bad security group format."
                         "One of the port range is not properly set:"
                         "range min: {},"
                         "range max: {}".format(port_range_min,
                                                port_range_max))
            return False

    # Create security group using neutron client
    try:
        neutron_client.create_security_group_rule(json_body)
        return True
    except:
        logger.exception("Impossible to create_security_group_rule,"
                         "security group rule probably already exists")
        return False


def create_security_group_full(neutron_client,
                               sg_name, sg_description):
    sg_id = get_security_group_id(neutron_client, sg_name)
    if sg_id != '':
        logger.info("Using existing security group '%s'..." % sg_name)
    else:
        logger.info("Creating security group  '%s'..." % sg_name)
        SECGROUP = create_security_group(neutron_client,
                                         sg_name,
                                         sg_description)
        if not SECGROUP:
            logger.error("Failed to create the security group...")
            return None

        sg_id = SECGROUP['id']

        logger.debug("Security group '%s' with ID=%s created successfully."
                     % (SECGROUP['name'], sg_id))

        logger.debug("Adding ICMP rules in security group '%s'..."
                     % sg_name)
        if not create_secgroup_rule(neutron_client, sg_id,
                                    'ingress', 'icmp'):
            logger.error("Failed to create the security group rule...")
            return None

        logger.debug("Adding SSH rules in security group '%s'..."
                     % sg_name)
        if not create_secgroup_rule(
                neutron_client, sg_id, 'ingress', 'tcp', '22', '22'):
            logger.error("Failed to create the security group rule...")
            return None

        if not create_secgroup_rule(
                neutron_client, sg_id, 'egress', 'tcp', '22', '22'):
            logger.error("Failed to create the security group rule...")
            return None
    return sg_id


def add_secgroup_to_instance(nova_client, instance_id, secgroup_id):
    try:
        nova_client.servers.add_security_group(instance_id, secgroup_id)
        return True
    except Exception, e:
        logger.error("Error [add_secgroup_to_instance(nova_client, '%s', "
                     "'%s')]: %s" % (instance_id, secgroup_id, e))
        return False


def update_sg_quota(neutron_client, tenant_id, sg_quota, sg_rule_quota):
    json_body = {"quota": {
        "security_group": sg_quota,
        "security_group_rule": sg_rule_quota
    }}

    try:
        neutron_client.update_quota(tenant_id=tenant_id,
                                    body=json_body)
        return True
    except Exception, e:
        logger.error("Error [update_sg_quota(neutron_client, '%s', '%s', "
                     "'%s')]: %s" % (tenant_id, sg_quota, sg_rule_quota, e))
        return False


def delete_security_group(neutron_client, secgroup_id):
    try:
        neutron_client.delete_security_group(secgroup_id)
        return True
    except Exception, e:
        logger.error("Error [delete_security_group(neutron_client, '%s')]: %s"
                     % (secgroup_id, e))
        return False


# *********************************************
#   GLANCE
# *********************************************
def get_images(nova_client):
    try:
        images = nova_client.images.list()
        return images
    except Exception, e:
        logger.error("Error [get_images]: %s" % e)
        return None


def get_image_id(glance_client, image_name):
    images = glance_client.images.list()
    id = ''
    for i in images:
        if i.name == image_name:
            id = i.id
            break
    return id


def create_glance_image(glance_client, image_name, file_path, disk="qcow2",
                        container="bare", public="public"):
    if not os.path.isfile(file_path):
        logger.error("Error: file %s does not exist." % file_path)
        return None
    try:
        image_id = get_image_id(glance_client, image_name)
        if image_id != '':
            logger.info("Image %s already exists." % image_name)
        else:
            logger.info("Creating image '%s' from '%s'..." % (image_name,
                                                              file_path))

            image = glance_client.images.create(name=image_name,
                                                visibility=public,
                                                disk_format=disk,
                                                container_format=container)
            image_id = image.id
            with open(file_path) as image_data:
                glance_client.images.upload(image_id, image_data)
        return image_id
    except Exception, e:
        logger.error("Error [create_glance_image(glance_client, '%s', '%s', "
                     "'%s')]: %s" % (image_name, file_path, public, e))
        return None


def get_or_create_image(name, path, format):
    image_exists = False
    glance_client = get_glance_client()

    image_id = get_image_id(glance_client, name)
    if image_id != '':
        logger.info("Using existing image '%s'..." % name)
        image_exists = True
    else:
        logger.info("Creating image '%s' from '%s'..." % (name, path))
        image_id = create_glance_image(glance_client, name, path, format)
        if not image_id:
            logger.error("Failed to create a Glance image...")
        else:
            logger.debug("Image '%s' with ID=%s created successfully."
                         % (name, image_id))

    return image_exists, image_id


def delete_glance_image(nova_client, image_id):
    try:
        nova_client.images.delete(image_id)
        return True
    except Exception, e:
        logger.error("Error [delete_glance_image(nova_client, '%s')]: %s"
                     % (image_id, e))
        return False


# *********************************************
#   CINDER
# *********************************************
def get_volumes(cinder_client):
    try:
        volumes = cinder_client.volumes.list(search_opts={'all_tenants': 1})
        return volumes
    except Exception, e:
        logger.error("Error [get_volumes(cinder_client)]: %s" % e)
        return None


def list_volume_types(cinder_client, public=True, private=True):
    try:
        volume_types = cinder_client.volume_types.list()
        if not public:
            volume_types = [vt for vt in volume_types if not vt.is_public]
        if not private:
            volume_types = [vt for vt in volume_types if vt.is_public]
        return volume_types
    except Exception, e:
        logger.error("Error [list_volume_types(cinder_client)]: %s" % e)
        return None


def create_volume_type(cinder_client, name):
    try:
        volume_type = cinder_client.volume_types.create(name)
        return volume_type
    except Exception, e:
        logger.error("Error [create_volume_type(cinder_client, '%s')]: %s"
                     % (name, e))
        return None


def update_cinder_quota(cinder_client, tenant_id, vols_quota,
                        snapshots_quota, gigabytes_quota):
    quotas_values = {"volumes": vols_quota,
                     "snapshots": snapshots_quota,
                     "gigabytes": gigabytes_quota}

    try:
        cinder_client.quotas.update(tenant_id, **quotas_values)
        return True
    except Exception, e:
        logger.error("Error [update_cinder_quota(cinder_client, '%s', '%s', "
                     "'%s' '%s')]: %s" % (tenant_id, vols_quota,
                                          snapshots_quota, gigabytes_quota, e))
        return False


def delete_volume(cinder_client, volume_id, forced=False):
    try:
        if forced:
            try:
                cinder_client.volumes.detach(volume_id)
            except:
                logger.error(sys.exc_info()[0])
            cinder_client.volumes.force_delete(volume_id)
        else:
            cinder_client.volumes.delete(volume_id)
        return True
    except Exception, e:
        logger.error("Error [delete_volume(cinder_client, '%s', '%s')]: %s"
                     % (volume_id, str(forced), e))
        return False


def delete_volume_type(cinder_client, volume_type):
    try:
        cinder_client.volume_types.delete(volume_type)
        return True
    except Exception, e:
        logger.error("Error [delete_volume_type(cinder_client, '%s')]: %s"
                     % (volume_type, e))
        return False


# *********************************************
#   KEYSTONE
# *********************************************
def get_tenants(keystone_client):
    try:
        if is_keystone_v3():
            tenants = keystone_client.projects.list()
        else:
            tenants = keystone_client.tenants.list()
        return tenants
    except Exception, e:
        logger.error("Error [get_tenants(keystone_client)]: %s" % e)
        return None


def get_users(keystone_client):
    try:
        users = keystone_client.users.list()
        return users
    except Exception, e:
        logger.error("Error [get_users(keystone_client)]: %s" % e)
        return None


def get_tenant_id(keystone_client, tenant_name):
    tenants = get_tenants(keystone_client)
    id = ''
    for t in tenants:
        if t.name == tenant_name:
            id = t.id
            break
    return id


def get_user_id(keystone_client, user_name):
    users = get_users(keystone_client)
    id = ''
    for u in users:
        if u.name == user_name:
            id = u.id
            break
    return id


def get_role_id(keystone_client, role_name):
    roles = keystone_client.roles.list()
    id = ''
    for r in roles:
        if r.name == role_name:
            id = r.id
            break
    return id


def create_tenant(keystone_client, tenant_name, tenant_description):
    try:
        if is_keystone_v3():
            tenant = keystone_client.projects.create(
                name=tenant_name,
                description=tenant_description,
                domain="default",
                enabled=True)
        else:
            tenant = keystone_client.tenants.create(tenant_name,
                                                    tenant_description,
                                                    enabled=True)
        return tenant.id
    except Exception, e:
        logger.error("Error [create_tenant(keystone_client, '%s', '%s')]: %s"
                     % (tenant_name, tenant_description, e))
        return None


def create_user(keystone_client, user_name, user_password,
                user_email, tenant_id):
    try:
        if is_keystone_v3():
            user = keystone_client.users.create(name=user_name,
                                                password=user_password,
                                                email=user_email,
                                                project_id=tenant_id,
                                                enabled=True)
        else:
            user = keystone_client.users.create(user_name,
                                                user_password,
                                                user_email,
                                                tenant_id,
                                                enabled=True)
        return user.id
    except Exception, e:
        logger.error("Error [create_user(keystone_client, '%s', '%s', '%s'"
                     "'%s')]: %s" % (user_name, user_password,
                                     user_email, tenant_id, e))
        return None


def add_role_user(keystone_client, user_id, role_id, tenant_id):
    try:
        if is_keystone_v3():
            keystone_client.roles.grant(role=role_id,
                                        user=user_id,
                                        project=tenant_id)
        else:
            keystone_client.roles.add_user_role(user_id, role_id, tenant_id)
        return True
    except Exception, e:
        logger.error("Error [add_role_user(keystone_client, '%s', '%s'"
                     "'%s')]: %s " % (user_id, role_id, tenant_id, e))
        return False


def delete_tenant(keystone_client, tenant_id):
    try:
        if is_keystone_v3():
            keystone_client.projects.delete(tenant_id)
        else:
            keystone_client.tenants.delete(tenant_id)
        return True
    except Exception, e:
        logger.error("Error [delete_tenant(keystone_client, '%s')]: %s"
                     % (tenant_id, e))
        return False


def delete_user(keystone_client, user_id):
    try:
        keystone_client.users.delete(user_id)
        return True
    except Exception, e:
        logger.error("Error [delete_user(keystone_client, '%s')]: %s"
                     % (user_id, e))
        return False


# *********************************************
#   HEAT
# *********************************************
def get_resource(heat_client, stack_id, resource):
    try:
        resources = heat_client.resources.get(stack_id, resource)
        return resources
    except Exception, e:
        logger.error("Error [get_resource]: %s" % e)
        return None
