#!/usr/bin/python

import os
import unittest
import yaml
from functest_utils import getTestEnv, isTestRunnable, generateTestcaseList


class TestFunctestUtils(unittest.TestCase):

    def setUp(self):
        os.environ["INSTALLER_TYPE"] = "fuel"
        os.environ["DEPLOY_SCENARIO"] = "os-odl_l3-ovs-ha"

        global functest_yaml

        with open("../config_functest.yaml") as f:
            functest_yaml = yaml.safe_load(f)
            f.close()

    def test_getTestEnv(self):

        env_test = getTestEnv('ovno', functest_yaml)
        self.assertEqual(env_test, {'scenario': 'ocl'})

        env_test = getTestEnv('doctor', functest_yaml)
        self.assertEqual(env_test, {'installer': 'fuel'})

        env_test = getTestEnv('promise', functest_yaml)
        self.assertEqual(env_test, {'installer': '(fuel)|(joid)'})

        env_test = getTestEnv('functest/tempest', functest_yaml)
        self.assertEqual(env_test, None)

        env_test = getTestEnv('functest/vims', functest_yaml)
        self.assertEqual(env_test, None)

        env_test = getTestEnv('functest/odl', functest_yaml)
        self.assertEqual(env_test, {'scenario': 'odl'})

        env_test = getTestEnv('functest/onos', functest_yaml)
        self.assertEqual(env_test, {'scenario': 'onos'})

        env_test = getTestEnv('policy-test', functest_yaml)
        self.assertEqual(env_test, {'scenario': 'odl'})

        env_test = getTestEnv('foo', functest_yaml)
        self.assertEqual(env_test, '')

    def test_isTestRunnable(self):

        test = isTestRunnable('ovno', functest_yaml)
        self.assertFalse(test)

        test = isTestRunnable('doctor', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('promise', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('functest/onos', functest_yaml)
        self.assertFalse(test)

        test = isTestRunnable('functest/odl', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('functest/vping_ssh', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('functest/vping_userdata', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('functest/tempest', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('functest/rally', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('functest/vims', functest_yaml)
        self.assertTrue(test)

    def test_generateTestcaseList(self):

        test = generateTestcaseList(functest_yaml)

        expected_list = ("vping_ssh vping_userdata tempest odl doctor " +
                         "promise policy-test odl-vpn_service-tests vims " +
                         "rally ")
        self.assertEqual(test, expected_list)

    def tearDown(self):
        os.environ["INSTALLER_TYPE"] = ""
        os.environ["DEPLOY_SCENARIO"] = ""


if __name__ == '__main__':
    unittest.main()
