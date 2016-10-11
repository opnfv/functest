#!/usr/bin/python

import argparse
import fileinput
import os
import re
import shutil
import sys
import urlparse

from robot import run
from robot.api import ExecutionResult, ResultVisitor
from robot.errors import RobotError
from robot.utils.robottime import timestamp_to_secs

import functest.core.TestCasesBase as TestCasesBase
import functest.utils.functest_logger as ft_logger
import functest.utils.openstack_utils as op_utils


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


class ODLTestCases(TestCasesBase.TestCasesBase):

    repos = "/home/opnfv/repos/"
    odl_test_repo = repos + "odl_test/"
    neutron_suite_dir = odl_test_repo + "csit/suites/openstack/neutron/"
    basic_suite_dir = odl_test_repo + "csit/suites/integration/basic/"
    res_dir = '/home/opnfv/functest/results/odl/'
    logger = ft_logger.Logger("opendaylight").getLogger()

    def __init__(self):
        self.case_name = "odl"

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
                    "%s" % str(e))
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
            cls.logger.error("Cannot set ODL creds: %s" % str(e))
            return False

    def parse_results(self):
        result = ExecutionResult(self.res_dir + 'output.xml')
        visitor = ODLResultVisitor()
        result.visit(visitor)
        self.criteria = result.suite.status
        self.start_time = timestamp_to_secs(result.suite.starttime)
        self.stop_time = timestamp_to_secs(result.suite.endtime)
        self.details = {}
        self.details['description'] = result.suite.name
        self.details['tests'] = visitor.get_data()

    def main(self, **kwargs):
        dirs = [self.basic_suite_dir, self.neutron_suite_dir]
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
            self.logger.error("Cannot run ODL testcases. Please check "
                              "%s" % str(e))
            return False
        if (self.copy_opnf_testcases() and
                self.set_robotframework_vars(odlusername, odlpassword)):
            try:
                os.makedirs(self.res_dir)
            except OSError:
                pass
            stdout_file = self.res_dir + 'stdout.txt'
            with open(stdout_file, 'w+') as stdout:
                run(*dirs, variable=variables,
                    output=self.res_dir + 'output.xml',
                    log='NONE',
                    report='NONE',
                    stdout=stdout)
                stdout.seek(0, 0)
                self.logger.info("\n" + stdout.read())
            self.logger.info("ODL results were successfully generated")
            try:
                self.parse_results()
                self.logger.info("ODL results were successfully parsed")
            except RobotError as e:
                self.logger.error("Run tests before publishing: %s" %
                                  e.message)
                return self.EX_RUN_ERROR
            try:
                os.remove(stdout_file)
            except OSError:
                pass
            return self.EX_OK
        else:
            return self.EX_RUN_ERROR

    def run(self):
        kclient = op_utils.get_keystone_client()
        keystone_url = kclient.service_catalog.url_for(
            service_type='identity', endpoint_type='publicURL')
        neutron_url = kclient.service_catalog.url_for(
            service_type='network', endpoint_type='publicURL')
        kwargs = {'keystoneip': urlparse.urlparse(keystone_url).hostname}
        kwargs['neutronip'] = urlparse.urlparse(neutron_url).hostname
        kwargs['odlip'] = kwargs['neutronip']
        kwargs['odlwebport'] = '8080'
        kwargs['odlrestconfport'] = '8181'
        kwargs['odlusername'] = 'admin'
        kwargs['odlpassword'] = 'admin'
        try:
            installer_type = os.environ['INSTALLER_TYPE']
            kwargs['osusername'] = os.environ['OS_USERNAME']
            kwargs['ostenantname'] = os.environ['OS_TENANT_NAME']
            kwargs['ospassword'] = os.environ['OS_PASSWORD']
            if installer_type == 'fuel':
                kwargs['odlwebport'] = '8282'
            elif installer_type == 'apex':
                kwargs['odlip'] = os.environ['SDN_CONTROLLER_IP']
                kwargs['odlwebport'] = '8181'
            elif installer_type == 'joid':
                kwargs['odlip'] = os.environ['SDN_CONTROLLER']
            elif installer_type == 'compass':
                kwargs['odlwebport'] = '8181'
            else:
                kwargs['odlip'] = os.environ['SDN_CONTROLLER_IP']
        except KeyError as e:
            self.logger.error("Cannot run ODL testcases. "
                              "Please check env var: "
                              "%s" % str(e))
            return self.EX_RUN_ERROR

        return self.main(**kwargs)

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
    odl = ODLTestCases()
    result = odl.main(**args)
    if result != TestCasesBase.TestCasesBase.EX_OK:
        sys.exit(result)
    if args['pushtodb']:
        sys.exit(odl.push_to_db())
