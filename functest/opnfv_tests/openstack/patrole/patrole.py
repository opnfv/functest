#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

from six.moves import configparser

from functest.opnfv_tests.openstack.tempest import tempest


class Patrole(tempest.TempestCommon):

    def configure(self, **kwargs):
        super().configure(**kwargs)
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        if not rconfig.has_section('rbac'):
            rconfig.add_section('rbac')
        rconfig.set('rbac', 'rbac_test_roles', kwargs.get('roles', 'admin'))
        with open(self.conf_file, 'w', encoding='utf-8') as config_file:
            rconfig.write(config_file)
        self.backup_tempest_config(self.conf_file, self.res_dir)
