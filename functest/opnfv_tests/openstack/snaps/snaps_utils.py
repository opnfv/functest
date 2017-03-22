# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

from snaps.openstack.utils import neutron_utils


def get_ext_net_name(os_creds):
    """
    Returns the first external network name
    :param: os_creds: an instance of snaps OSCreds object
    :return:
    """
    neutron = neutron_utils.neutron_client(os_creds)
    ext_nets = neutron_utils.get_external_networks(neutron)
    return ext_nets[0]['network']['name']
