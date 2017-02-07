#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

import functest.core.testcase_base as testcase_base
from functest.opnfv_tests.openstack.vping import vping_ssh


class OSVpingSSHTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.neutron_client = mock.Mock()
        self.glance_client = mock.Mock()
        self.nova_client = mock.Mock()

        self.vm = mock.Mock()
        attrs = {'id': 'test_id',
                 'get_console_output.return_value': ''}
        self.vm.configure_mock(**attrs)

        self.fail_ssh_client = mock.Mock()
        attrs = {'connect.return_value': Exception}
        self.fail_ssh_client.configure_mock(**attrs)

        with mock.patch('functest.opnfv_tests.openstack.vping.vping_base.'
                        'os_utils.get_neutron_client',
                        return_value=self.neutron_client), \
            mock.patch('functest.opnfv_tests.openstack.vping.vping_base.'
                       'os_utils.get_glance_client',
                       return_value=self.glance_client), \
            mock.patch('functest.opnfv_tests.openstack.vping.vping_base.'
                       'os_utils.get_nova_client',
                       return_value=self.nova_client):
            self.vping_ssh = vping_ssh.VPingSSH()

    def test_do_vping_missing_floatip(self):
        with mock.patch.object(self.vping_ssh, 'add_float_ip',
                               return_value=None):
            self.assertEqual(self.vping_ssh.do_vping(self.vm, 'test_ip'),
                             testcase_base.TestcaseBase.EX_RUN_ERROR)

    def test_do_vping_missing_ssh(self):
        with mock.patch.object(self.vping_ssh, 'add_float_ip',
                               return_value='test_float_ip'), \
            mock.patch.object(self.vping_ssh, 'establish_ssh',
                              return_value=None):
            self.assertEqual(self.vping_ssh.do_vping(self.vm, 'test_ip'),
                             testcase_base.TestcaseBase.EX_RUN_ERROR)

    def test_do_vping_missing_transfer_script(self):
        with mock.patch.object(self.vping_ssh, 'add_float_ip',
                               return_value='test_float_ip'), \
            mock.patch.object(self.vping_ssh, 'establish_ssh',
                              return_value='test_ssh'), \
            mock.patch.object(self.vping_ssh, 'transfer_ping_script',
                              return_value=None):
            self.assertEqual(self.vping_ssh.do_vping(self.vm, 'test_ip'),
                             testcase_base.TestcaseBase.EX_RUN_ERROR)

    def test_do_vping_default(self):
        with mock.patch.object(self.vping_ssh, 'add_float_ip',
                               return_value='test_float_ip'), \
            mock.patch.object(self.vping_ssh, 'establish_ssh',
                              return_value='test_ssh'), \
            mock.patch.object(self.vping_ssh, 'transfer_ping_script',
                              return_value='test_ping_script'), \
                mock.patch.object(self.vping_ssh, 'do_vping_ssh') as m:
            self.vping_ssh.do_vping(self.vm, 'test_ip')
            m.assert_any_call('test_ssh', 'test_ip')

    def test_add_float_ip_missing_floatip(self):
        floatip_dic = {'fip_addr': None}
        with mock.patch('functest.opnfv_tests.openstack.vping.vping_ssh.'
                        'os_utils.create_floating_ip',
                        return_value=floatip_dic):
            self.assertEqual(self.vping_ssh.add_float_ip(self.vm),
                             None)

    def test_add_float_ip_assosciation_failed(self):
        floatip_dic = {'fip_addr': 'test_fip_addr'}
        with mock.patch('functest.opnfv_tests.openstack.vping.vping_ssh.'
                        'os_utils.create_floating_ip',
                        return_value=floatip_dic), \
            mock.patch('functest.opnfv_tests.openstack.vping.vping_ssh.'
                       'os_utils.add_floating_ip',
                       return_value=False):
            self.assertEqual(self.vping_ssh.add_float_ip(self.vm),
                             None)

    def test_add_float_ip_default(self):
        floatip_dic = {'fip_addr': 'test_fip_addr'}
        with mock.patch('functest.opnfv_tests.openstack.vping.vping_ssh.'
                        'os_utils.create_floating_ip',
                        return_value=floatip_dic), \
            mock.patch('functest.opnfv_tests.openstack.vping.vping_ssh.'
                       'os_utils.add_floating_ip',
                       return_value=True):
            self.assertEqual(self.vping_ssh.add_float_ip(self.vm),
                             'test_fip_addr')

    # TODO: Implementation takes 5 minutes to finish this test
    # def test_establish_ssh_connection_failed(self):
    #     m = mock.Mock()
    #     attrs = {'connect.side_effect': Exception}
    #     m.configure_mock(**attrs)
    #
    #     with mock.patch('functest.opnfv_tests.openstack.vping.'
    #                     'vping_ssh.paramiko.SSHClient',
    #                     return_value=m):
    #         self.assertEqual(self.vping_ssh.establish_ssh(self.vm,
    #                                                       'test_ip'),
    #                          None)

    def test_transfer_ping_script_scp_put_failed(self):
        scp = mock.Mock()
        attrs = {'put.side_effect': Exception}
        scp.configure_mock(**attrs)

        ssh = mock.Mock()
        attrs = {'exec_command.return_value': ('', '', '')}
        ssh.configure_mock(**attrs)

        with mock.patch('functest.opnfv_tests.openstack.vping.'
                        'vping_ssh.SCPClient',
                        return_value=scp):
            self.assertEqual(self.vping_ssh.
                             transfer_ping_script(ssh, 'test_ip'),
                             False)

    def test_transfer_ping_script_default(self):
        scp = mock.Mock()
        attrs = {'put.side_effect': 'successful'}
        scp.configure_mock(**attrs)

        stdout = mock.Mock()
        attrs = {'readlines.return_value': ''}
        stdout.configure_mock(**attrs)

        ssh = mock.Mock()
        attrs = {'exec_command.return_value': ('', stdout, '')}
        ssh.configure_mock(**attrs)

        with mock.patch('functest.opnfv_tests.openstack.vping.'
                        'vping_ssh.SCPClient',
                        return_value=scp):
            self.assertEqual(self.vping_ssh.
                             transfer_ping_script(ssh, 'test_ip'),
                             True)

    def test_do_vping_ssh_default(self):
        self.vping_ssh.ping_timeout = 1
        stdout = mock.Mock()
        attrs = {'readlines.return_value': ['vPing OK']}
        stdout.configure_mock(**attrs)

        ssh = mock.Mock()
        attrs = {'exec_command.return_value': ('', stdout, '')}
        ssh.configure_mock(**attrs)

        self.assertEqual(self.vping_ssh.
                         do_vping_ssh(ssh, 'test_ip'),
                         0)

    def test_do_vping_ssh_timeout(self):
        stdout = mock.Mock()
        attrs = {'readlines.return_value': ['test']}
        stdout.configure_mock(**attrs)

        ssh = mock.Mock()
        attrs = {'exec_command.return_value': ('', stdout, '')}
        ssh.configure_mock(**attrs)

        self.vping_ssh.ping_timeout = 1
        self.assertEqual(self.vping_ssh.
                         do_vping_ssh(ssh, 'test_ip'),
                         -1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
