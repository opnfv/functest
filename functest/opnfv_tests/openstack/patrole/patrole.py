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

from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.opnfv_tests.openstack.tempest import tempest
from functest.utils import config


class Patrole(tempest.TempestCommon):

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'patrole'
        super(Patrole, self).__init__(**kwargs)
        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), 'patrole')
        self.list = os.path.join(self.res_dir, 'tempest-list.txt')
        self.conf_file = None

    def run(self, **kwargs):
        self.start_time = time.time()
        for exclude in kwargs.get('exclude', []):
            self.mode = "{}(?!.*{})".format(self.mode, exclude)
        self.mode = "'{}(?=patrole_tempest_plugin.tests.api.({}))'".format(
            self.mode, '|'.join(kwargs.get('services', [])))
        try:
            self.configure()
            self.configure_tempest_patrole(kwargs.get('role', 'admin'))
            self.generate_test_list()
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

    def configure_tempest_patrole(self, role='admin'):
        rconfig = conf_utils.ConfigParser.RawConfigParser()
        rconfig.read(self.conf_file)
        rconfig.add_section('rbac')
        rconfig.set('rbac', 'enable_rbac', True)
        rconfig.set('rbac', 'rbac_test_role', role)
        with open(self.conf_file, 'wb') as config_file:
            rconfig.write(config_file)
