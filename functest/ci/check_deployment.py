##############################################################################
# Copyright (c) 2017 Ericsson and others.
#
# Author: Jose Lausuch
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import logging
import logging.config
import os
import pkg_resources
import socket
import sys
import time
from urlparse import urlparse


from snaps.openstack.utils import glance_utils
from snaps.openstack.utils import keystone_utils
from snaps.openstack.utils import neutron_utils
from snaps.openstack.utils import nova_utils
from snaps.openstack.tests import openstack_tests


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

    def _print_ok(self):
        logger.info("   OK!")

    def _print_fail(self):
        logger.error("  FAILED!")

    def check_rc(self):
        if not os.path.isfile(self.rc_file):
            raise Exception('RC file {} does not exist!'.format(self.rc_file))

        if 'OS_AUTH_URL' not in open(self.rc_file).read():
            raise Exception('OS_AUTH_URL not defined in {}.'.
                            format(self.rc_file))
        self._print_ok()

    def check_auth_endpoint(self, os_creds):
        rc_endpoint = os_creds.auth_url
        logger.info("Verifying connectivity to OS_AUTH_URL {} ..."
                    .format(rc_endpoint))
        if not (verify_connectivity(urlparse(rc_endpoint).hostname,
                                    urlparse(rc_endpoint).port)):
            self._print_fail()
            raise Exception("OS_AUTH_URL {} is not reachable.".
                            format(rc_endpoint))
        self._print_ok()

    def check_public_endpoint(self, os_creds):
        public_endpoint = keystone_utils.get_endpoint(os_creds,
                                                      'identity',
                                                      interface='public')
        logger.info("Verifying connectivity to the public endpoint {} ..."
                    .format(public_endpoint))
        if not (verify_connectivity(urlparse(public_endpoint).hostname,
                                    urlparse(public_endpoint).port)):
            self._print_fail()
            raise Exception("Public endpoint {} is not reachable.".
                            format(public_endpoint))
        self._print_ok()

    def check_service_endpoint(self, service, os_creds):
        endpoint = keystone_utils.get_endpoint(os_creds,
                                               service,
                                               interface='public')
        logger.info("Verifying connectivity to endpoint '{}' {} ...".
                    format(service, endpoint))
        if not (verify_connectivity(urlparse(endpoint).hostname,
                                    urlparse(endpoint).port)):
            self._print_fail()
            raise Exception("{} endpoint {} is not reachable.".
                            format(service, endpoint))
        self._print_ok()

    def check_nova(self, os_creds):
        logger.info("Checking Nova service...")
        try:
            client = nova_utils.nova_client(os_creds)
            client.servers.list()
        except Exception as e:
            self._print_fail()
            raise(e)
        self._print_ok()

    def check_neutron(self, os_creds):
        logger.info("Checking Neutron service...")
        try:
            client = neutron_utils.neutron_client(os_creds)
            client.list_networks()
        except Exception as e:
            self._print_fail()
            raise(e)
        self._print_ok()

    def check_glance(self, os_creds):
        logger.info("Checking Glance service...")
        try:
            client = glance_utils.glance_client(os_creds)
            client.images.list()
        except Exception as e:
            self._print_fail()
            raise(e)
        self._print_ok()

    def check_all(self):
        os_creds = openstack_tests.get_credentials(os_env_file=self.rc_file,
                                                   proxy_settings_str=None,
                                                   ssh_proxy_cmd=None)
        self.check_auth_endpoint(os_creds)
        self.check_public_endpoint(os_creds)
        for service in self.services:
            self.check_service_endpoint(service, os_creds)
        self.check_nova(os_creds)
        self.check_neutron(os_creds)
        self.check_glance(os_creds)
        return 0


def main():
    logging.config.fileConfig(pkg_resources.resource_filename(
        'functest', 'ci/logging.ini'))
    deployment = CheckDeployment()
    return deployment.check_all()


if __name__ == '__main__':
    sys.exit(main())
