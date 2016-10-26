#!/usr/bin/python

import argparse
import fileinput
import os
import re
import sys
import urlparse

from robot import run
from robot.api import ExecutionResult, ResultVisitor
from robot.errors import RobotError
from robot.utils.robottime import timestamp_to_secs

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
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


class ODLTestCases:

    repos = "/home/opnfv/repos/"
    odl_test_repo = repos + "odl_test/"
    neutron_suite_dir = odl_test_repo + "csit/suites/openstack/neutron/"
    basic_suite_dir = odl_test_repo + "csit/suites/integration/basic/"
    res_dir = '/home/opnfv/functest/results/odl/'
    logger = ft_logger.Logger("opendaylight").getLogger()

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
                             "%s" % str(e))
            return False
        if cls.set_robotframework_vars(odlusername, odlpassword):
            try:
                os.makedirs(cls.res_dir)
            except OSError:
                pass
            stdout_file = cls.res_dir + 'stdout.txt'
            with open(stdout_file, 'w+') as stdout:
                run(*dirs, variable=variables,
                    output=cls.res_dir + 'output.xml',
                    log='NONE',
                    report='NONE',
                    stdout=stdout)
                stdout.seek(0, 0)
                cls.logger.info("\n" + stdout.read())
            cls.logger.info("ODL results were successfully generated")
            try:
                os.remove(stdout_file)
            except OSError:
                pass
            return True
        else:
            return False

    @classmethod
    def functest_run(cls):
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
            cls.logger.error("Cannot run ODL testcases. Please check env var: "
                             "%s" % str(e))
            return False

        return cls.run(**kwargs)

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
                    "functest", "odl", start_time, stop_time,
                    result.suite.status, details):
                cls.logger.error("Cannot push ODL results to DB")
                return False
            else:
                cls.logger.info("ODL results were successfully pushed to DB")
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
