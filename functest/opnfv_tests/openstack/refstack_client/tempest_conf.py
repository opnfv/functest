#!/usr/bin/env python

# matthew.lijun@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
import logging
import pkg_resources

from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils import openstack_utils
from functest.utils.constants import CONST
from functest.opnfv_tests.openstack.tempest.tempest \
    import TempestResourcesManager

""" logging configuration """
logger = logging.getLogger(__name__)


class TempestConf(object):
    def __init__(self, **kwargs):
        self.VERIFIER_ID = conf_utils.get_verifier_id()
        self.VERIFIER_REPO_DIR = conf_utils.get_verifier_repo_dir(
            self.VERIFIER_ID)
        self.DEPLOYMENT_ID = conf_utils.get_verifier_deployment_id()
        self.DEPLOYMENT_DIR = conf_utils.get_verifier_deployment_dir(
            self.VERIFIER_ID, self.DEPLOYMENT_ID)
        self.confpath = pkg_resources.resource_filename(
            'functest',
            'opnfv_tests/openstack/refstack_client/refstack_tempest.conf')
        self.resources = TempestResourcesManager(**kwargs)

    def generate_tempestconf(self):
        try:
            openstack_utils.source_credentials(
                CONST.__getattribute__('openstack_creds'))
            resources = self.resources.create(create_project=True,
                                              use_custom_images=True,
                                              use_custom_flavors=True)
            conf_utils.configure_tempest_defcore(
                self.DEPLOYMENT_DIR,
                image_id=resources.get("image_id"),
                flavor_id=resources.get("flavor_id"),
                image_id_alt=resources.get("image_id_alt"),
                flavor_id_alt=resources.get("flavor_id_alt"),
                tenant_id=resources.get("project_id"))
        except Exception as e:
            logger.error("error with generating refstack client "
                         "reference tempest conf file: %s", e)

    def main(self):
        try:
            self.generate_tempestconf()
            logger.info("a reference tempest conf file generated "
                        "at %s", self.confpath)
        except Exception as e:
            logger.error('Error with run: %s', e)

    def clean(self):
        self.resources.cleanup()


def main():
    logging.basicConfig()
    tempestconf = TempestConf()
    tempestconf.main()
