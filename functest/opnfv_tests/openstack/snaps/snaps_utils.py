# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import functest.utils.functest_utils as ft_utils
from snaps.openstack.tests import openstack_tests
from snaps.openstack.utils import neutron_utils


def get_ext_net_name():
    """
    Returns the first external network name
    :return:
    """
    os_env_file = ft_utils.get_functest_config('general.openstack.creds')
    os_creds = openstack_tests.get_credentials(os_env_file=os_env_file)
    neutron = neutron_utils.neutron_client(os_creds)
    ext_nets = neutron_utils.get_external_networks(neutron)
    return ext_nets[0]['network']['name']
