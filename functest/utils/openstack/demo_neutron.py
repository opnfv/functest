#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import neutron
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("demo_neutron").getLogger()
net_name = 'demo-net'
subnet_name = 'demo-subnet'
router_name = 'demo-router'
subnet_cidr = '192.168.110.0/24'


def print_separator(id, service):
    logger.info("============DEMO %s: %s Client============" % (id, service))


def main():
    neutron_client = neutron.get_neutron_client()

    print_separator(3, 'Neutron')

    network = neutron.create_shared_network_full(net_name,
                                                 subnet_name,
                                                 router_name,
                                                 subnet_cidr)
    logger.info("network: %s" % network)
    network_id = network.get('net_id')
    subnet_id = network.get('subnet_id')
    router_id = network.get('router_id')

    networks = neutron.get_network_list(neutron_client)
    for network in networks:
        if network.get('name') == net_name:
            network_detail = network
            logger.info("network data: %s" % network_detail)
            break
    else:
        logger.info("Network %s is not found" % net_name)

    routers = neutron.get_router_list(neutron_client)
    if routers:
        logger.info("First router: %s" % routers[0])
    else:
        logger.info("No router")

    ports = neutron.get_port_list(neutron_client)
    if ports:
        logger.info("First port: %s" % ports[0])
    else:
        logger.info("No port")

    gateway_router_deleted = neutron.remove_gateway_router(neutron_client,
                                                           router_id)
    logger.info("gateway_router_deleted: %s" % gateway_router_deleted)
    interface_router_deleted = neutron.remove_interface_router(neutron_client,
                                                               router_id,
                                                               subnet_id)
    logger.info("interface_router_deleted: %s" % interface_router_deleted)
    subnet_deleted = neutron.delete_neutron_subnet(neutron_client, subnet_id)
    logger.info("subnet_deleted: %s" % subnet_deleted)
    router_deleted = neutron.delete_neutron_router(neutron_client, router_id)
    logger.info("router_deleted: %s" % router_deleted)
    net_deleted = neutron.delete_neutron_net(neutron_client, network_id)
    logger.info("net_deleted: %s" % net_deleted)


if __name__ == '__main__':
    main()
