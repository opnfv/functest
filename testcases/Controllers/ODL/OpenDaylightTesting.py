#!/usr/bin/python

import argparse
import fileinput
import os
import re
import shutil
import sys

from robot import run
from robot.api import ExecutionResult, ResultVisitor
from robot.errors import RobotError
from robot.utils.robottime import timestamp_to_secs

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils


class ODLResultVisitor(ResultVisitor):

    def __init__(self):
        self._data = []

    def visit_test(self, test):
        output = {}
        output['name'] = test.name
        output['parent'] = test.parent.name
        output['status'] = test.status
        output['startime'] = test.starttime
        output['endtime'] = test.endtime
        output['critical'] = test.critical
        output['text'] = test.message
        output['elapsedtime'] = test.elapsedtime
        self._data.append(output)

    def get_data(self):
        return self._data


class ODLTestCases:

    repos = "/home/opnfv/repos/"
    odl_test_repo = repos + "odl_test/"
    neutron_suite_dir = odl_test_repo + "csit/suites/openstack/neutron/"
    basic_suite_dir = odl_test_repo + "csit/suites/integration/basic/"
    res_dir = '/home/opnfv/functest/results/odl/'
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
                    "Cannot copy OPNFV's testcases to ODL directory: "
                    "%s" % e.strerror)
                return False
        return True

    @classmethod
    def set_robotframework_vars(cls, odlusername="admin", odlpassword="admin"):
        odl_variables_files = cls.odl_test_repo + 'csit/variables/Variables.py'
        try:
            for line in fileinput.input(odl_variables_files,
                                        inplace=True):
                print re.sub("AUTH = .*",
                             ("AUTH = [u'" + odlusername + "', u'" +
                              odlpassword + "']"),
                             line.rstrip())
            return True
        except Exception as e:
            cls.logger.error("Cannot set ODL creds: %s" % e.strerror)
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
            cls.logger.error("Cannot run ODL testcases. Please check "
                             "%s" % e.strerror)
            return False
        if (cls.copy_opnf_testcases() and
                cls.set_robotframework_vars(odlusername, odlpassword)):
            try:
                os.makedirs(cls.res_dir)
            except OSError:
                pass
            stdout_file = cls.res_dir + 'stdout.txt'
            with open(stdout_file, 'w') as stdout:
                run(*dirs, variable=variables,
                    output=cls.res_dir + 'output.xml',
                    log='NONE',
                    report='NONE',
                    stdout=stdout)
            with open(stdout_file, 'r') as stdout:
                cls.logger.info("\n" + stdout.read())
            cls.logger.info("ODL results was sucessfully generated")
            return True
        else:
            return False

    @classmethod
    def push_to_db(cls):
        try:
            result = ExecutionResult(cls.res_dir + 'output.xml')
            visitor = ODLResultVisitor()
            result.visit(visitor)
            start_time = timestamp_to_secs(result.suite.starttime)
            stop_time = timestamp_to_secs(result.suite.endtime)
            details = {}
            details['description'] = result.suite.name
            details['tests'] = visitor.get_data()
            if not ft_utils.push_results_to_db(
                    "functest", "odl", None, start_time, stop_time,
                    result.suite.status, details):
                cls.logger.error("Cannot push ODL results to DB")
                return False
            else:
                cls.logger.info("ODL results was sucessfully pushed to DB")
                return True
        except RobotError as e:
            cls.logger.error("Run tests before publishing: %s" % e.message)


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
    parser.add_argument('-p', '--pushtodb',
                        help='Push results to DB',
                        action='store_true')

    args = vars(parser.parse_args())
    if not ODLTestCases.run(**args):
        sys.exit(os.EX_SOFTWARE)
    if args['pushtodb']:
        sys.exit(not ODLTestCases.push_to_db())
    sys.exit(os.EX_OK)
