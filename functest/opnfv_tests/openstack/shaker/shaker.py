#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Shaker_ wraps around popular system network testing tools like iperf, iperf3
and netperf (with help of flent). Shaker is able to deploy OpenStack instances
and networks in different topologies. Shaker scenario specifies the deployment
and list of tests to execute.

.. _Shaker: http://pyshaker.readthedocs.io/en/latest/
"""

import logging
import os

from scp import SCPClient

from functest.core import simple

class Shaker(simple.Simple):
    # pylint: disable=too-many-instance-attributes

    __logger = logging.getLogger(__name__)

    filename = '/home/opnfv/functest/images/shaker-image.qcow2'
    flavor_ram = 512
    flavor_vcpus = 1
    flavor_disk = 3
    username = 'ubuntu'

    def create_sg_rules(self):
        super(Shaker, self).create_sg_rules()
        self.cloud.create_security_group_rule(
            self.sec.id, port_range_min='9000', port_range_max='9000',
            protocol='tcp', direction='ingress')

    def execute(self):
        scp = SCPClient(self.ssh.get_transport())
        scp.put('/home/opnfv/functest/conf/env_file', '~/')
        (_, stdout, stderr) = self.ssh.exec_command(
            'source ~/env_file && export OS_INTERFACE=public &&'
            'shaker --server-endpoint {}:9000 --scenario '
            'openstack/full_l2,openstack/full_l3_east_west,'
            'openstack/full_l3_north_south,openstack/perf_l2,'
            'openstack/perf_l3_east_west,openstack/perf_l3_north_south '
            '--report report.html --output report.json ; echo $?'.format(
                self.sshvm.public_v4))
        self.__logger.info("output:\n%s", stdout.read())
        self.__logger.info("error:\n%s", stderr.read())
        if not os.path.exists(self.res_dir):
            os.makedirs(self.res_dir)
        scp.get('report.*', self.res_dir)
        return stdout.channel.recv_exit_status()
