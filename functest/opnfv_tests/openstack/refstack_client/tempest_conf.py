#!/usr/bin/env python

# matthew.lijun@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
import logging
import os

from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils import openstack_utils
from functest.utils.constants import CONST

""" logging configuration """
logger = logging.getLogger(__name__)


class TempestConf(object):
    def __init__(self):
        self.VERIFIER_ID = conf_utils.get_verifier_id()
        self.VERIFIER_REPO_DIR = conf_utils.get_verifier_repo_dir(
            self.VERIFIER_ID)
        self.DEPLOYMENT_ID = conf_utils.get_verifier_deployment_id()
        self.DEPLOYMENT_DIR = conf_utils.get_verifier_deployment_dir(
            self.VERIFIER_ID, self.DEPLOYMENT_ID)
        self.confpath = os.path.join(CONST.dir_functest_test,
                                     CONST.refstack_tempest_conf_path)

    def generate_tempestconf(self):
        try:
            openstack_utils.source_credentials(CONST.openstack_creds)
            img_flavor_dict = conf_utils.create_tempest_resources(
                use_custom_images=True, use_custom_flavors=True)
            conf_utils.configure_tempest_defcore(
                self.DEPLOYMENT_DIR, img_flavor_dict)
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


if __name__ == '__main__':
    tempestconf = TempestConf()
    tempestconf.main()
