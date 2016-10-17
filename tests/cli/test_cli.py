#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import unittest

from click.testing import CliRunner
from functest.cli import cli_base


class CliBaseTest(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.tests = ['healthcheck', 'vping_ssh', 'vping_userdata',
                      'tempest_smoke_serial', 'rally_sanity', 'odl', 'onos',
                      'promise', 'doctor', 'bgpvpn', 'security_scan', 'copper',
                      'moon', 'multisite', 'domino', 'odl-sfc', 'onos_sfc',
                      'parser', 'tempest_full_parallel', 'rally_full', 'vims']
        self.tiers = ['healthcheck', 'smoke', 'sdn_suites', 'features',
                      'openstack', 'vnf']

        # TODO some env vars may be needed

    # main menus
    def test_env(self):
        result = self.runner.invoke(cli_base.env)
        assert result.exit_code == 0

    def test_openstack(self):
        result = self.runner.invoke(cli_base.openstack)
        assert result.exit_code == 0

    def test_testcase(self):
        result = self.runner.invoke(cli_base.testcase)
        assert result.exit_code == 0

    def test_tier(self):
        result = self.runner.invoke(cli_base.tier)
        assert result.exit_code == 0

    def test_bad(self):
        with self.assertRaises(AttributeError):
            self.runner.invoke(cli_base.bad)

    # env
    # def test_env_prepare(self):
        # result = self.runner.invoke(cli_base.env, ['prepare'])
        # TODO depends of the env

    def test_env_status(self):
        result = self.runner.invoke(cli_base.env, ['status'])
        assert result.exit_code == 0

    def test_env_show(self):
        result = self.runner.invoke(cli_base.env, ['show'])
        assert result.exit_code == 0

    def test_env_bad(self):
        result = self.runner.invoke(cli_base.env, ['bad'])
        assert result.exit_code != 0

    # openstack
    def test_os_check(self):
        result = self.runner.invoke(cli_base.os_check)
        assert result.exit_code == 0

    def test_os_snapshot_show(self):
        result = self.runner.invoke(cli_base.os_snapshot_show)
        assert result.exit_code == 0

    def test_os_show_credentials(self):
        result = self.runner.invoke(cli_base.os_show_credentials)
        assert result.exit_code == 0

    def test_os_bad(self):
        result = self.runner.invoke(cli_base, ['os_bad'])
        assert result.exit_code != 0

    # testcases
    def test_testcase_list(self):
        result = self.runner.invoke(cli_base.testcase, ['list'])
        assert result.exit_code == 0
        for test in self.tests:
            assert test in result.output

    def test_testcase_show(self):
        for test in self.tests:
            result = self.runner.invoke(cli_base.testcase, ['show', test])
            assert 'Testcase:' in result.output

    def test_testcase_show_bad(self):
        result = self.runner.invoke(cli_base.testcase, ['show',
                                                        'wrong_test_name'])
        assert 'does not exist' in result.output

    def test_testcase_run(self):
        result = self.runner.invoke(cli_base.testcase, ['run', 'healthcheck'])
        assert 'Functest environment is not ready' in result.output

    # tiers
    def test_tier_list(self):
        result = self.runner.invoke(cli_base.tier, ['list'])
        assert result.exit_code == 0
        for tier in self.tiers:
            assert tier in result.output

    def test_tier_show(self):
        for tier in self.tiers:
            result = self.runner.invoke(cli_base.tier, ['show', tier])
            assert 'Tier:' in result.output

    def test_tier_run(self):
        result = self.runner.invoke(cli_base.tier, ['run', 'healthcheck'])
        assert 'Functest environment is not ready' in result.output

    def test_tier_show_bad(self):
        result = self.runner.invoke(cli_base.tier, ['show', 'wrong_tier_name'])
        assert 'does not exist' in result.output

if __name__ == '__main__':
    unittest.main()
