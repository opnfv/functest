#!/usr/bin/env python

# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""Some common utils wrapping snaps functions """

from functest.utils.constants import CONST
from functest.utils import env

from snaps.openstack.tests import openstack_tests
from snaps.openstack.utils import neutron_utils, nova_utils


def get_ext_net_name(os_creds):
    """
    Returns the configured external network name or
    the first retrieved external network name
    :param: os_creds: an instance of snaps OSCreds object
    :return:
    """
    neutron = neutron_utils.neutron_client(os_creds)
    ext_nets = neutron_utils.get_external_networks(neutron)
    if env.get('EXTERNAL_NETWORK'):
        extnet_config = env.get('EXTERNAL_NETWORK')
        for ext_net in ext_nets:
            if ext_net.name == extnet_config:
                return extnet_config
    return ext_nets[0].name if ext_nets else ""


def get_active_compute_cnt(os_creds):
    """
    Returns the number of active compute servers
    :param: os_creds: an instance of snaps OSCreds object
    :return: the number of active compute servers
    """
    nova = nova_utils.nova_client(os_creds)
    computes = nova_utils.get_availability_zone_hosts(nova, zone_name='nova')
    return len(computes)


def get_credentials(proxy_settings_str=None, ssh_proxy_cmd=None):
    """
    Returns snaps OSCreds object instance
    :param: proxy_settings_str: proxy settings string <host>:<port>
    :param: ssh_proxy_cmd: the SSH proxy command for the environment
    :return: an instance of snaps OSCreds object
    """
    creds_override = None
    if hasattr(CONST, 'snaps_os_creds_override'):
        creds_override = CONST.__getattribute__(
            'snaps_os_creds_override')
    os_creds = openstack_tests.get_credentials(
        os_env_file=CONST.__getattribute__('env_file'),
        proxy_settings_str=proxy_settings_str, ssh_proxy_cmd=ssh_proxy_cmd,
        overrides=creds_override)
    return os_creds
