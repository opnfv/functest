#!/usr/bin/env python

# Copyright (c) 2019 Intracom Telecom and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring


import unittest

import mock
import munch

from functest.opnfv_tests.openstack.intel_nfv_ci import intel_nfv_ci


class IntelNfvCiTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'TempestCommon.__init__') as tempest_mock:
            tempest_mock.return_value = None
            self.intel = intel_nfv_ci.IntelNfvCi()
            self.intel.conf_file = 'conf_file'
            self.intel.res_dir = 'res_dir'

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.TempestCommon.'
                'configure')
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.TempestCommon.'
                'backup_tempest_config')
    @mock.patch('functest.opnfv_tests.openstack.intel_nfv_ci.intel_nfv_ci.'
                'configparser.RawConfigParser')
    @mock.patch('__builtin__.open')
    def test_configure(self, *args):
        args[0].return_value.__enter__.return_value = mock.Mock()
        self.intel.configure()
        args[2].assert_called_once_with(self.intel.conf_file,
                                        self.intel.res_dir)

    def test_is_numa_enabled(self):
        node = mock.Mock()
        file = mock.Mock()
        file.read.return_value = '2'
        node.exec_command.return_value = None, file, None
        result = self.intel.is_numa_enabled(node)
        self.assertEqual(result, True)

    def test_is_numa_enabled_error(self):
        node = mock.Mock()
        file = mock.Mock()
        file.read.return_value = 'wrong'
        node.exec_command.return_value = None, file, None
        result = self.intel.is_numa_enabled(node)
        self.assertEqual(result, False)

    def test_has_hyperthreading_enabled(self):
        node = mock.Mock()
        file = mock.Mock()
        file.read.return_value = '0-1\n'
        node.exec_command.return_value = None, file, None
        result = self.intel.has_hyperthreading_enabled(node)
        self.assertEqual(result, True)

    def test_has_hugepages_enabled(self):
        node = mock.Mock()
        file = mock.Mock()
        file.read.return_value = '1'
        node.exec_command.return_value = None, file, None
        result = self.intel.has_hugepages_enabled(node)
        self.assertEqual(result, True)

    def test_has_hugepages_enabled_error(self):
        node = mock.Mock()
        file = mock.Mock()
        file.read.return_value = 'wrong'
        node.exec_command.return_value = None, file, None
        result = self.intel.has_hugepages_enabled(node)
        self.assertEqual(result, False)

    def test_check_requirements_skip(self):
        self.intel.check_requirements()
        self.assertEquals(self.intel.is_skipped, True)

    @mock.patch('functest.opnfv_tests.openstack.intel_nfv_ci.intel_nfv_ci.env',
                side_effect=['ubuntu', 'key'])
    @mock.patch('functest.opnfv_tests.openstack.intel_nfv_ci.intel_nfv_ci.'
                'shade.OpenStackCloud')
    @mock.patch('functest.opnfv_tests.openstack.intel_nfv_ci.intel_nfv_ci.'
                'paramiko.SSHClient')
    def test_check_requirements(self, *args):
        cloud = mock.Mock()
        cloud.list_hypervisors.return_value = [
            munch.Munch(host_ip='127.0.0.1')]
        args[1].return_value = cloud
        self.intel.is_numa_enabled = mock.Mock()
        self.intel.has_hyperthreading_enabled = mock.Mock()
        self.intel.has_hugepages_enabled = mock.Mock()
        self.intel.is_numa_enabled.return_value = True
        self.intel.has_hyperthreading_enabled.return_value = True
        self.intel.has_hugepages_enabled.return_value = True
        self.intel.check_requirements()

    @mock.patch('functest.opnfv_tests.openstack.intel_nfv_ci.intel_nfv_ci.env',
                side_effect=['ubuntu', 'key'])
    @mock.patch('functest.opnfv_tests.openstack.intel_nfv_ci.intel_nfv_ci.'
                'shade.OpenStackCloud')
    @mock.patch('functest.opnfv_tests.openstack.intel_nfv_ci.intel_nfv_ci.'
                'paramiko.SSHClient')
    def test_check_requirements_skip_after_check(self, *args):
        cloud = mock.Mock()
        cloud.list_hypervisors.return_value = [
            munch.Munch(host_ip='127.0.0.1')]
        args[1].return_value = cloud
        self.intel.is_numa_enabled = mock.Mock()
        self.intel.is_numa_enabled.return_value = False
        self.intel.check_requirements()
        self.assertEquals(self.intel.is_skipped, True)

    @mock.patch('functest.opnfv_tests.openstack.intel_nfv_ci.intel_nfv_ci.env',
                side_effect=['ubuntu', 'key'])
    @mock.patch('functest.opnfv_tests.openstack.intel_nfv_ci.intel_nfv_ci.'
                'shade.OpenStackCloud', side_effect=Exception)
    def test_check_requirements_exception(self, *args):
        self.intel.check_requirements()
