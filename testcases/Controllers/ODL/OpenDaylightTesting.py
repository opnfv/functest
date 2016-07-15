#!/usr/bin/python

import argparse
import fileinput
import os
import re
import shutil
import sys
import functest.utils.functest_logger as ft_logger
from robot import run


class ODLTestCases:

    repos = "/home/opnfv/repos/"
    odl_test_repo = repos + "odl_test/"
    neutron_suite_dir = odl_test_repo + "csit/suites/openstack/neutron/"
    basic_suite_dir = odl_test_repo + "csit/suites/integration/basic/"
    logger = ft_logger.Logger("opendaylight").getLogger()

    @classmethod
    def copy_opnf_testcases(cls):
        opnfv_testcases_dir = (os.path.dirname(os.path.abspath(__file__)) +
                               "/custom_tests/neutron/")
        files = [opnfv_testcases_dir + "001__reachability.robot",
                 opnfv_testcases_dir + "040__delete_ports.robot",
                 opnfv_testcases_dir + "050__delete_subnets.robot",
                 opnfv_testcases_dir + "060__delete_networks.robot"]
        for f in files:
            try:
                shutil.copy(f, cls.neutron_suite_dir)
            except IOError as e:
                cls.logger.error(
                    "Cannot copy OPNFV's testcases to ODL directory", e)
                return False
        return True

    @classmethod
    def set_robotframework_vars(cls, odlusername="admin", odlpassword="admin"):
        odl_variables_files = cls.odl_test_repo + 'csit/variables/Variables.py'
        try:
            cls.logger.debug(cls.neutron_suite_dir + '__init__.robot')
            for line in fileinput.input(odl_variables_files,
                                        inplace=True):
                print re.sub("AUTH = .*",
                             ("AUTH = [u'" + odlusername + "', u'" +
                              odlpassword + "']"),
                             line.rstrip())
            return True
        except Exception as e:
            cls.logger.error("Cannot set ODL creds", e)
            return False

    @classmethod
    def run(cls, **kwargs):
        dirs = [cls.basic_suite_dir, cls.neutron_suite_dir]
        try:
            odlusername = kwargs['odlusername']
            odlpassword = kwargs['odlpassword']
            variables = ['KEYSTONE:' + kwargs['keystoneip'],
                         'NEUTRON:' + kwargs['neutronip'],
                         'OSUSERNAME:"' + kwargs['osusername'] + '"',
                         'OSTENANTNAME:"' + kwargs['ostenantname'] + '"',
                         'OSPASSWORD:"' + kwargs['ospassword'] + '"',
                         'ODL_SYSTEM_IP:' + kwargs['odlip'],
                         'PORT:' + kwargs['odlwebport'],
                         'RESTCONFPORT:' + kwargs['odlrestconfport']]
        except KeyError as e:
            cls.logger.error("Cannot run ODL testcases. Please check", e)
            return False
        res_dir = '/home/opnfv/functest/results/odl/'
        if (cls.copy_opnf_testcases() and
                cls.set_robotframework_vars(odlusername, odlpassword)):
            try:
                os.makedirs(res_dir)
            except OSError:
                pass
            stdout_file = res_dir + 'stdout.txt'
            with open(stdout_file, 'w') as stdout:
                result = run(*dirs, variable=variables,
                             output=res_dir + 'output.xml',
                             log=res_dir + 'log.html',
                             report=res_dir + 'report.html',
                             stdout=stdout)

            with open(stdout_file, 'r') as stdout:
                cls.logger.info("\n" + stdout.read())

            return result
        else:
            return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keystoneip',
                        help='Keystone IP',
                        default='127.0.0.1')
    parser.add_argument('-n', '--neutronip',
                        help='Neutron IP',
                        default='127.0.0.1')
    parser.add_argument('-a', '--osusername',
                        help='Username for OpenStack',
                        default='admin')
    parser.add_argument('-b', '--ostenantname',
                        help='Tenantname for OpenStack',
                        default='admin')
    parser.add_argument('-c', '--ospassword',
                        help='Password for OpenStack',
                        default='admin')
    parser.add_argument('-o', '--odlip',
                        help='OpenDaylight IP',
                        default='127.0.0.1')
    parser.add_argument('-w', '--odlwebport',
                        help='OpenDaylight Web Portal Port',
                        default='8080')
    parser.add_argument('-r', '--odlrestconfport',
                        help='OpenDaylight RESTConf Port',
                        default='8181')
    parser.add_argument('-d', '--odlusername',
                        help='Username for ODL',
                        default='admin')
    parser.add_argument('-e', '--odlpassword',
                        help='Password for ODL',
                        default='admin')
    args = vars(parser.parse_args())
    sys.exit(ODLTestCases.run(**args))
