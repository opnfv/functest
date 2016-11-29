#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import os

import utils
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("neutron").getLogger()

DEFAULT_API_VERSION = '2'
API_NAME = 'network'
API_VERSIONS = {
    '2': 'neutronclient.v2_0.client'
}


def get_client_version():
    api_version = os.getenv('OS_NETWORK_API_VERSION')
    if api_version is not None:
        logger.info("OS_NETWORK_API_VERSION is set in env as '%s'",
                    api_version)
        return api_version
    return DEFAULT_API_VERSION


def get_neutron_client():
    creds_neutron = utils.get_credentials('neutron')
    neutron_client_cls = utils.get_client_class(
        API_NAME,
        get_client_version(),
        API_VERSIONS)
    logger.debug('Instantiating network client: %s', neutron_client_cls)
    return neutron_client_cls.Client(**creds_neutron)


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
    if port_range_min is None and port_range_max is None:
        json_body = {'security_group_rule': {'direction': direction,
                                             'security_group_id': sg_id,
                                             'protocol': protocol}}
    elif port_range_min is not None and port_range_max is not None:
        json_body = {'security_group_rule': {'direction': direction,
                                             'security_group_id': sg_id,
                                             'port_range_min': port_range_min,
                                             'port_range_max': port_range_max,
                                             'protocol': protocol}}
    else:
        logger.error("Error [create_secgroup_rule(neutron_client, '%s', '%s', "
                     "'%s', '%s', '%s', '%s')]:" % (neutron_client,
                                                    sg_id, direction,
                                                    port_range_min,
                                                    port_range_max,
                                                    protocol),
                     " Invalid values for port_range_min, port_range_max")
        return False
    try:
        neutron_client.create_security_group_rule(json_body)
        return True
    except Exception, e:
        logger.error("Error [create_secgroup_rule(neutron_client, '%s', '%s', "
                     "'%s', '%s', '%s', '%s')]: %s" % (neutron_client,
                                                       sg_id,
                                                       direction,
                                                       port_range_min,
                                                       port_range_max,
                                                       protocol, e))
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
