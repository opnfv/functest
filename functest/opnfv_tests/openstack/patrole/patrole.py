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

from six.moves import configparser

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

    def apply_tempest_blacklist(self):
        pass

    def configure(self, **kwargs):
        super(Patrole, self).configure(**kwargs)
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        rconfig.add_section('rbac')
        rconfig.set('rbac', 'enable_rbac', True)
        rconfig.set('rbac', 'rbac_test_role', kwargs.get('role', 'admin'))
        with open(self.conf_file, 'wb') as config_file:
            rconfig.write(config_file)
        self.backup_tempest_config(self.conf_file, self.res_dir)

    def run(self, **kwargs):
        for exclude in kwargs.get('exclude', []):
            self.mode = "{}(?!.*{})".format(self.mode, exclude)
        self.mode = "'{}(?=patrole_tempest_plugin.tests.api.({}))'".format(
            self.mode, '|'.join(kwargs.get('services', [])))
        return super(Patrole, self).run(**kwargs)
