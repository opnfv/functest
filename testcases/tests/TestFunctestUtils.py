import unittest
import os
import sys
import yaml

sys.path.append("../")
from functest_utils import getTestEnv, isTestRunnable, generateTestcaseList


class TestFunctestUtils(unittest.TestCase):

    def setUp(self):
        os.environ["INSTALLER_TYPE"] = "fuel"
        os.environ["SDN_CONTROLLER"] = "odl"
        os.environ["OPNFV_FEATURE"] = "ovs2.4"

        global functest_yaml

        with open("../config_functest.yaml") as f:
            functest_yaml = yaml.safe_load(f)
            f.close()

    def test_getTestEnv(self):

        env_test = getTestEnv('ovno', functest_yaml)
        self.assertEqual(env_test, {'controller': 'opencontrail'})

        env_test = getTestEnv('functest/tempest', functest_yaml)
        self.assertEqual(env_test, None)

        env_test = getTestEnv('functest/vims', functest_yaml)
        self.assertEqual(env_test, None)

        env_test = getTestEnv('functest/odl', functest_yaml)
        self.assertEqual(env_test, {'controller': 'odl'})

        env_test = getTestEnv('functest/onos', functest_yaml)
        self.assertEqual(env_test, {'controller': 'onos'})

        env_test = getTestEnv('functest/onos-ovsdb', functest_yaml)
        self.assertEqual(env_test, {'controller': 'onos'})

        env_test = getTestEnv('policy-test', functest_yaml)
        self.assertEqual(env_test, {'controller': 'odl'})

        env_test = getTestEnv('sdnvpn/odl-vpn_service-tests', functest_yaml)
        self.assertEqual(env_test, {'controller': 'odl', 'options': 'ovs2.4'})

        env_test = getTestEnv('sdnvpn/opnfv-yardstick-tc026-sdnvpn', functest_yaml)
        self.assertEqual(env_test, {'controller': 'nosdn', 'options': 'ovs2.4'})

        env_test = getTestEnv('sdnvpn/openstack-neutron-bgpvpn-api-extension-tests', functest_yaml)
        self.assertEqual(env_test,  {'controller': 'nosdn', 'options': 'ovs2.4'})

        env_test = getTestEnv('foo', functest_yaml)
        self.assertEqual(env_test, '')

    def test_isTestRunnable(self):

        test = isTestRunnable('ovno', functest_yaml)
        self.assertFalse(test)

        test = isTestRunnable('functest/onos', functest_yaml)
        self.assertFalse(test)

        test = isTestRunnable('functest/odl', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('functest/vping', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('functest/tempest', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('functest/rally', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('functest/vims', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('sdnvpn/odl-vpn_service-tests', functest_yaml)
        self.assertTrue(test)

        test = isTestRunnable('sdnvpn/opnfv-yardstick-tc026-sdnvpn', functest_yaml)
        self.assertFalse(test)

    def test_generateTestcaseList(self):

        test = generateTestcaseList(functest_yaml)
        self.assertEqual(test, "vims odl rally vping tempest policy-test odl-vpn_service-tests ")

    def tearDown(self):
        os.environ["INSTALLER_TYPE"] = ""
        os.environ["SDN_CONTROLLER"] = ""
        os.environ["OPNFV_FEATURE"] = ""


if __name__ == '__main__':
    unittest.main()
