#!/usr/bin/env python

# matthew.lijun@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

""" Used to generate tempest.conf """

import logging
import pkg_resources

from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.opnfv_tests.openstack.tempest.tempest \
    import TempestResourcesManager

LOGGER = logging.getLogger(__name__)


class TempestConf(object):
    """ TempestConf class"""
    def __init__(self, **kwargs):
        self.verifier_id = conf_utils.get_verifier_id()
        self.deployment_id = conf_utils.get_verifier_deployment_id()
        self.deployment_dir = conf_utils.get_verifier_deployment_dir(
            self.verifier_id, self.deployment_id)
        self.confpath = pkg_resources.resource_filename(
            'functest',
            'opnfv_tests/openstack/refstack_client/refstack_tempest.conf')
        self.resources = TempestResourcesManager(**kwargs)

    def generate_tempestconf(self):
        """ Generate tempest.conf file"""
        try:
            resources = self.resources.create(create_project=True,
                                              use_custom_images=True,
                                              use_custom_flavors=True)
            conf_utils.configure_tempest_defcore(
                self.deployment_dir,
                image_id=resources.get("image_id"),
                flavor_id=resources.get("flavor_id"),
                image_id_alt=resources.get("image_id_alt"),
                flavor_id_alt=resources.get("flavor_id_alt"),
                tenant_id=resources.get("project_id"))
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.error("error with generating refstack client "
                         "reference tempest conf file: %s", err)

    def main(self):
        """ The main function called by entry point"""
        try:
            self.generate_tempestconf()
            LOGGER.info("a reference tempest conf file generated "
                        "at %s", self.confpath)
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.error('Error with run: %s', err)

    def clean(self):
        """Clean up the resources"""
        self.resources.cleanup()


def main():
    """Entry point"""
    logging.basicConfig()
    tempestconf = TempestConf()
    tempestconf.main()
