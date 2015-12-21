import unittest
import os
import sys

sys.path.append("../")
from functest_utils import getTestEnv, isTestRunnable


class TestFunctestUtils(unittest.TestCase):

    def setUp(self):
        os.environ["INSTALLER_TYPE"] = "fuel"
        os.environ["SDN_CONTROLLER"] = "odl"
        os.environ["OPNFV_FEATURE"] = "ovs2.4"

    def test_getTestEnv(self):

        env_test = getTestEnv('ovno')
        self.assertEqual(env_test, {'controller': 'opencontrail'})

        env_test = getTestEnv('functest/tempest')
        self.assertEqual(env_test, '')

        env_test = getTestEnv('functest/vims')
        self.assertEqual(env_test, '')

        env_test = getTestEnv('functest/odl')
        self.assertEqual(env_test, {'controller': 'odl'})

        env_test = getTestEnv('functest/onos')
        self.assertEqual(env_test, {'controller': 'onos'})

        env_test = getTestEnv('functest/onos-ovsdb')
        self.assertEqual(env_test, {'controller': 'onos'})

        env_test = getTestEnv('policy-test')
        self.assertEqual(env_test, {'controller': 'odl'})

        env_test = getTestEnv('sdnvpn/odl-vpn_service-tests')
        self.assertEqual(env_test, {'controller': 'odl', 'options': 'ovs2.4'})

        env_test = getTestEnv('sdnvpn/opnfv-yardstick-tc026-sdnvpn')
        self.assertEqual(env_test, {'controller': 'nosdn', 'options': 'ovs2.4'})

        env_test = getTestEnv('sdnvpn/openstack-neutron-bgpvpn-api-extension-tests')
        self.assertEqual(env_test,  {'controller': 'nosdn', 'options': 'ovs2.4'})

        env_test = getTestEnv('foo')
        self.assertEqual(env_test, '')

    def test_isTestRunnable(self):

        test = isTestRunnable('ovno')
        self.assertFalse(test)

        test = isTestRunnable('functest/onos')
        self.assertFalse(test)

        test = isTestRunnable('functest/odl')
        self.assertTrue(test)

        test = isTestRunnable('functest/vping')
        self.assertTrue(test)

        test = isTestRunnable('functest/tempest')
        self.assertTrue(test)

        test = isTestRunnable('functest/rally')
        self.assertTrue(test)

        test = isTestRunnable('functest/vims')
        self.assertTrue(test)

        test = isTestRunnable('sdnvpn/odl-vpn_service-tests')
        self.assertTrue(test)

        test = isTestRunnable('sdnvpn/opnfv-yardstick-tc026-sdnvpn')
        self.assertFalse(test)

    def tearDown(self):
        os.environ["INSTALLER_TYPE"] = ""
        os.environ["SDN_CONTROLLER"] = ""
        os.environ["OPNFV_FEATURE"] = ""


if __name__ == '__main__':
    unittest.main()
