#!/usr/bin/env python

# Copyright (c) 2017 Ericsson and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import logging.config
import os
import pkg_resources
import socket
import time
from urlparse import urlparse

from snaps.openstack.utils import glance_utils
from snaps.openstack.utils import keystone_utils
from snaps.openstack.utils import neutron_utils
from snaps.openstack.utils import nova_utils
from snaps.openstack.tests import openstack_tests

__author__ = "Jose Lausuch <jose.lausuch@ericsson.com>"

logger = logging.getLogger('functest.ci.check_deployment')


def verify_connectivity(ip, port, timeout=10):
    s = socket.socket()
    n = 0
    while n < timeout:
        try:
            s.connect((ip, port))
            logger.debug('{}:{} is reachable!'.format(ip, port))
            return True
        except socket.error:
            n += 1
            time.sleep(1)
            continue
    logger.info('{}:{} is not reachable.'.format(ip, port))
    return False


class CheckDeployment:

    def __init__(self, rc_file='/home/opnfv/functest/conf/openstack.creds'):
        self.rc_file = rc_file
        self.services = ('compute', 'network', 'image')
        self.os_creds = None

    def check_rc(self):
        if not os.path.isfile(self.rc_file):
            raise IOError('RC file {} does not exist!'.format(self.rc_file))
        if 'OS_AUTH_URL' not in open(self.rc_file).read():
            raise SyntaxError('OS_AUTH_URL not defined in {}.'.
                              format(self.rc_file))

    def check_auth_endpoint(self):
        rc_endpoint = self.os_creds.auth_url
        if not (verify_connectivity(urlparse(rc_endpoint).hostname,
                                    urlparse(rc_endpoint).port)):
            raise Exception("OS_AUTH_URL {} is not reachable.".
                            format(rc_endpoint))
        logger.info("Connectivity to OS_AUTH_URL {} ...OK"
                    .format(rc_endpoint))

    def check_public_endpoint(self):
        public_endpoint = keystone_utils.get_endpoint(self.os_creds,
                                                      'identity',
                                                      interface='public')
        if not (verify_connectivity(urlparse(public_endpoint).hostname,
                                    urlparse(public_endpoint).port)):
            raise Exception("Public endpoint {} is not reachable.".
                            format(public_endpoint))
        logger.info("Connectivity to the public endpoint {} ...OK"
                    .format(public_endpoint))

    def check_service_endpoint(self, service):
        endpoint = keystone_utils.get_endpoint(self.os_creds,
                                               service,
                                               interface='public')
        if not (verify_connectivity(urlparse(endpoint).hostname,
                                    urlparse(endpoint).port)):
            raise Exception("{} endpoint {} is not reachable.".
                            format(service, endpoint))
        logger.info("Connectivity to endpoint '{}' {} ...OK".
                    format(service, endpoint))

    def check_nova(self):
        try:
            client = nova_utils.nova_client(self.os_creds)
            client.servers.list()
            logger.info("Nova service ...OK")
        except Exception as e:
            logger.info("Nova service ...FAILED")
            raise(e)

    def check_neutron(self):
        try:
            client = neutron_utils.neutron_client(self.os_creds)
            client.list_networks()
            logger.info("Neutron service ...OK")
        except Exception as e:
            logger.info("Neutron service ...FAILED")
            raise Exception(e)

    def check_glance(self):
        try:
            client = glance_utils.glance_client(self.os_creds)
            client.images.list()
            logger.info("Glance service ...OK")
        except Exception as e:
            logger.info("Glance service ...FAILED")
            raise(e)

    def check_all(self):
        self.check_rc()
        try:
            self.os_creds = openstack_tests.get_credentials(
                os_env_file=self.rc_file,
                proxy_settings_str=None,
                ssh_proxy_cmd=None)
        except:
            raise Exception()
        self.check_auth_endpoint()
        self.check_public_endpoint()
        for service in self.services:
            self.check_service_endpoint(service)
        self.check_nova()
        self.check_neutron()
        self.check_glance()
        return 0


def main():
    logging.config.fileConfig(pkg_resources.resource_filename(
        'functest', 'ci/logging.ini'))
    deployment = CheckDeployment()
    return deployment.check_all()
