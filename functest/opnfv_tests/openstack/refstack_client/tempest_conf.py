#!/usr/bin/env python

# matthew.lijun@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

""" Used to generate tempest.conf """

import logging
import os

from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.opnfv_tests.openstack.tempest import tempest
from functest.utils import constants


class TempestConf(object):
    """ TempestConf class"""

    logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        self.resdir = os.path.join(
            getattr(constants.CONST, 'dir_results'), 'refstack')
        self.confpath = os.path.join(self.resdir, 'refstack_tempest.conf')
        self.resources = tempest.TempestResourcesManager(**kwargs)
        self.deployment_dir = conf_utils.get_verifier_deployment_dir(
            conf_utils.get_verifier_id(),
            conf_utils.get_verifier_deployment_id())


    def main(self):
        """ Generate tempest.conf file"""
        try:
            if not os.path.exists(self.resdir):
                os.makedirs(self.resdir)
            resources = self.resources.create(
                create_project=True, use_custom_images=True,
                use_custom_flavors=True)
            conf_utils.configure_tempest_defcore(
                self.confpath, self.deployment_dir,
                network_name=resources.get("network_name"),
                image_id=resources.get("image_id"),
                flavor_id=resources.get("flavor_id"),
                image_id_alt=resources.get("image_id_alt"),
                flavor_id_alt=resources.get("flavor_id_alt"),
                tenant_id=resources.get("project_id"))
            self.logger.info(
                "a reference tempest conf file generated at %s", self.confpath)
        except Exception as err:  # pylint: disable=broad-except
            self.logger.error(
                "error with generating refstack client reference tempest "
                "conf file: %s", err)

    def clean(self):
        """Clean up the resources"""
        self.resources.cleanup()


def main():
    """Entry point"""
    logging.basicConfig()
    tempestconf = TempestConf()
    tempestconf.main()
