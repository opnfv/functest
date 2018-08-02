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

import scp

from functest.core import singlevm


class Shaker(singlevm.SingleVm2):
    """Run shaker full+perf l2 and l3"""
    # pylint: disable=too-many-instance-attributes

    __logger = logging.getLogger(__name__)

    filename = '/home/opnfv/functest/images/shaker-image.qcow2'
    flavor_ram = 512
    flavor_vcpus = 1
    flavor_disk = 3
    username = 'ubuntu'
    port = 9000
    ssh_connect_loops = 12
    create_server_timeout = 300

    def __init__(self, **kwargs):
        super(Shaker, self).__init__(**kwargs)
        self.role = None

    def prepare(self):
        super(Shaker, self).prepare()
        self.cloud.create_security_group_rule(
            self.sec.id, port_range_min=self.port, port_range_max=self.port,
            protocol='tcp', direction='ingress')

    def execute(self):
        """
        Returns:
            - 0 if success
            - 1 on operation error
        """
        assert self.ssh
        endpoint = self.get_public_auth_url(self.orig_cloud)
        self.__logger.debug("keystone endpoint: %s", endpoint)
        if self.orig_cloud.get_role("admin"):
            role_name = "admin"
        elif self.orig_cloud.get_role("Admin"):
            role_name = "Admin"
        else:
            raise Exception("Cannot detect neither admin nor Admin")
        self.orig_cloud.grant_role(
            role_name, user=self.project.user.id,
            project=self.project.project.id,
            domain=self.project.domain.id)
        if not self.orig_cloud.get_role("heat_stack_owner"):
            self.role = self.orig_cloud.create_role("heat_stack_owner")
        self.orig_cloud.grant_role(
            "heat_stack_owner", user=self.project.user.id,
            project=self.project.project.id,
            domain=self.project.domain.id)
        scpc = scp.SCPClient(self.ssh.get_transport())
        scpc.put('/home/opnfv/functest/conf/env_file', remote_path='~/')
        if os.environ.get('OS_CACERT'):
            scpc.put(os.environ.get('OS_CACERT'), remote_path='~/os_cacert')
        (_, stdout, stderr) = self.ssh.exec_command(
            'source ~/env_file && '
            'export OS_INTERFACE=public && '
            'export OS_AUTH_URL={} && '
            'export OS_USERNAME={} && '
            'export OS_PROJECT_NAME={} && '
            'export OS_PROJECT_ID={} && '
            'unset OS_TENANT_NAME && '
            'unset OS_TENANT_ID && '
            'export OS_PASSWORD={} && '
            '{}'
            'env && '
            'shaker --image-name {} --flavor-name {} '
            '--server-endpoint {}:9000 --scenario '
            'openstack/full_l2,'
            'openstack/full_l3_east_west,'
            'openstack/full_l3_north_south,'
            'openstack/perf_l3_north_south '
            '--report report.html --output report.json'.format(
                endpoint, self.project.user.name, self.project.project.name,
                self.project.project.id, self.project.password,
                'export OS_CACERT=~/os_cacert && ' if os.environ.get(
                    'OS_CACERT') else '',
                self.image.name, self.flavor.name,
                self.fip.floating_ip_address))
        self.__logger.info("output:\n%s", stdout.read())
        self.__logger.info("error:\n%s", stderr.read())
        if not os.path.exists(self.res_dir):
            os.makedirs(self.res_dir)
        try:
            scpc.get('report.json', self.res_dir)
            scpc.get('report.html', self.res_dir)
        except scp.SCPException:
            self.__logger.exception("cannot get report files")
            return 1
        return stdout.channel.recv_exit_status()

    def clean(self):
        super(Shaker, self).clean()
        if self.role:
            self.orig_cloud.delete_role(self.role.id)
