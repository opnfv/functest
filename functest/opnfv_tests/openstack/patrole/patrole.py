#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import os
import time

from xtesting.core import testcase

from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.opnfv_tests.openstack.tempest import tempest
from functest.utils import config


class Patrole(tempest.TempestCommon):

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'patrole'
        super(Patrole, self).__init__(**kwargs)
        self.mode = ("'(?!.*test_networks_multiprovider_rbac)"
                     "(?=patrole_tempest_plugin.tests.api.(image|network))'")
        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), 'patrole')

    def run(self, **kwargs):
        self.start_time = time.time()
        try:
            if not os.path.exists(self.res_dir):
                os.makedirs(self.res_dir)
            resources = self.resources.create()
            compute_cnt = snaps_utils.get_active_compute_cnt(
                self.resources.os_creds)
            self.configure_tempest_patrole(
                self.deployment_dir,
                network_name=resources.get("network_name"),
                image_id=resources.get("image_id"),
                flavor_id=resources.get("flavor_id"),
                compute_cnt=compute_cnt,
                role=kwargs.get('role', 'admin'))
            self.generate_test_list(self.verifier_repo_dir)
            self.apply_tempest_blacklist()
            self.run_verifier_tests()
            self.parse_verifier_result()
            self.generate_report()
            res = testcase.TestCase.EX_OK
        except Exception as err:  # pylint: disable=broad-except
            self.__logger.error('Error with run: %s', err)
            res = testcase.TestCase.EX_RUN_ERROR
        finally:
            self.resources.cleanup()
        self.stop_time = time.time()
        return res

    def configure_tempest_patrole(
            self, deployment_dir, network_name=None, image_id=None,
            flavor_id=None, compute_cnt=None, role='admin'):
        # pylint: disable=too-many-arguments
        """
        Add/update needed parameters into tempest.conf file
        """
        self.__logger.debug(
            "Updating selected tempest.conf parameters for Patrole")
        conf_file = conf_utils.configure_verifier(deployment_dir)
        conf_utils.configure_tempest_update_params(
            conf_file, network_name, image_id, flavor_id, compute_cnt)
        rconfig = conf_utils.ConfigParser.RawConfigParser()
        rconfig.read(conf_file)
        rconfig.set('identity-feature-enabled', 'api_v2', False)
        rconfig.add_section('rbac')
        rconfig.set('rbac', 'enable_rbac', True)
        rconfig.set('rbac', 'rbac_test_role', role)
        with open(conf_file, 'wb') as config_file:
            rconfig.write(config_file)
