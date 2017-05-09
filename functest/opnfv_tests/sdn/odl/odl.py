#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define classes required to run ODL suites.

It has been designed for any context. But helpers are given for
running test suites in OPNFV environment.

Example:
        $ python odl.py
"""

from __future__ import division

import argparse
import errno
import fileinput
import logging
import os
import re
import sys
import urlparse

import robot.api
from robot.errors import RobotError
import robot.run
from robot.utils.robottime import timestamp_to_secs

from functest.core import testcase
import functest.utils.openstack_utils as op_utils

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"


class ODLResultVisitor(robot.api.ResultVisitor):
    """Visitor to get result details."""

    def __init__(self):
        self._data = []

    def visit_test(self, test):
        output = {}
        output['name'] = test.name
        output['parent'] = test.parent.name
        output['status'] = test.status
        output['starttime'] = test.starttime
        output['endtime'] = test.endtime
        output['critical'] = test.critical
        output['text'] = test.message
        output['elapsedtime'] = test.elapsedtime
        self._data.append(output)

    def get_data(self):
        """Get the details of the result."""
        return self._data


class ODLTests(testcase.TestCase):
    """ODL test runner."""

    repos = "/home/opnfv/repos/"
    odl_test_repo = os.path.join(repos, "odl_test")
    neutron_suite_dir = os.path.join(odl_test_repo,
                                     "csit/suites/openstack/neutron")
    basic_suite_dir = os.path.join(odl_test_repo,
                                   "csit/suites/integration/basic")
    default_suites = [basic_suite_dir, neutron_suite_dir]
    res_dir = '/home/opnfv/functest/results/odl/'
    __logger = logging.getLogger(__name__)

    @classmethod
    def set_robotframework_vars(cls, odlusername="admin", odlpassword="admin"):
        """Set credentials in csit/variables/Variables.py.

        Returns:
            True if credentials are set.
            False otherwise.
        """
        odl_variables_files = os.path.join(cls.odl_test_repo,
                                           'csit/variables/Variables.py')
        try:
            for line in fileinput.input(odl_variables_files,
                                        inplace=True):
                print re.sub("AUTH = .*",
                             ("AUTH = [u'" + odlusername + "', u'" +
                              odlpassword + "']"),
                             line.rstrip())
            return True
        except Exception as ex:  # pylint: disable=broad-except
            cls.__logger.error("Cannot set ODL creds: %s", str(ex))
            return False

    def parse_results(self):
        """Parse output.xml and get the details in it."""
        xml_file = os.path.join(self.res_dir, 'output.xml')
        result = robot.api.ExecutionResult(xml_file)
        visitor = ODLResultVisitor()
        result.visit(visitor)
        try:
            self.result = 100 * (
                result.suite.statistics.all.passed /
                result.suite.statistics.all.total)
        except ZeroDivisionError:
            self.__logger.error("No test has been ran")
        self.start_time = timestamp_to_secs(result.suite.starttime)
        self.stop_time = timestamp_to_secs(result.suite.endtime)
        self.details = {}
        self.details['description'] = result.suite.name
        self.details['tests'] = visitor.get_data()

    def main(self, suites=None, **kwargs):
        """Run the test suites

        It has been designed to be called in any context.
        It requires the following keyword arguments:

           * odlusername,
           * odlpassword,
           * osauthurl,
           * neutronip,
           * osusername,
           * ostenantname,
           * ospassword,
           * odlip,
           * odlwebport,
           * odlrestconfport.

        Here are the steps:
           * set all RobotFramework_variables,
           * create the output directories if required,
           * get the results in output.xml,
           * delete temporary files.

        Args:
            kwargs: Arbitrary keyword arguments.

        Returns:
            EX_OK if all suites ran well.
            EX_RUN_ERROR otherwise.
        """
        try:
            if not suites:
                suites = self.default_suites
            odlusername = kwargs['odlusername']
            odlpassword = kwargs['odlpassword']
            osauthurl = kwargs['osauthurl']
            keystoneip = urlparse.urlparse(osauthurl).hostname
            variables = ['KEYSTONE:' + keystoneip,
                         'NEUTRON:' + kwargs['neutronip'],
                         'OS_AUTH_URL:"' + osauthurl + '"',
                         'OSUSERNAME:"' + kwargs['osusername'] + '"',
                         'OSTENANTNAME:"' + kwargs['ostenantname'] + '"',
                         'OSPASSWORD:"' + kwargs['ospassword'] + '"',
                         'ODL_SYSTEM_IP:' + kwargs['odlip'],
                         'PORT:' + kwargs['odlwebport'],
                         'RESTCONFPORT:' + kwargs['odlrestconfport']]
        except KeyError as ex:
            self.__logger.error("Cannot run ODL testcases. Please check "
                                "%s", str(ex))
            return self.EX_RUN_ERROR
        if self.set_robotframework_vars(odlusername, odlpassword):
            try:
                os.makedirs(self.res_dir)
            except OSError as ex:
                if ex.errno != errno.EEXIST:
                    self.__logger.exception(
                        "Cannot create %s", self.res_dir)
                    return self.EX_RUN_ERROR
            stdout_file = os.path.join(self.res_dir, 'stdout.txt')
            output_dir = os.path.join(self.res_dir, 'output.xml')
            with open(stdout_file, 'w+') as stdout:
                robot.run(*suites, variable=variables,
                          output=output_dir,
                          log='NONE',
                          report='NONE',
                          stdout=stdout)
                stdout.seek(0, 0)
                self.__logger.info("\n" + stdout.read())
            self.__logger.info("ODL results were successfully generated")
            try:
                self.parse_results()
                self.__logger.info("ODL results were successfully parsed")
            except RobotError as ex:
                self.__logger.error("Run tests before publishing: %s",
                                    ex.message)
                return self.EX_RUN_ERROR
            try:
                os.remove(stdout_file)
            except OSError:
                self.__logger.warning("Cannot remove %s", stdout_file)
            return self.EX_OK
        else:
            return self.EX_RUN_ERROR

    def run(self, **kwargs):
        """Run suites in OPNFV environment

        It basically check env vars to call main() with the keywords
        required.

        Args:
            kwargs: Arbitrary keyword arguments.

        Returns:
            EX_OK if all suites ran well.
            EX_RUN_ERROR otherwise.
        """
        try:
            suites = self.default_suites
            try:
                suites = kwargs["suites"]
            except KeyError:
                pass
            neutron_url = op_utils.get_endpoint(service_type='network')
            kwargs = {'neutronip': urlparse.urlparse(neutron_url).hostname}
            kwargs['odlip'] = kwargs['neutronip']
            kwargs['odlwebport'] = '8080'
            kwargs['odlrestconfport'] = '8181'
            kwargs['odlusername'] = 'admin'
            kwargs['odlpassword'] = 'admin'
            installer_type = None
            if 'INSTALLER_TYPE' in os.environ:
                installer_type = os.environ['INSTALLER_TYPE']
            kwargs['osusername'] = os.environ['OS_USERNAME']
            kwargs['ostenantname'] = os.environ['OS_TENANT_NAME']
            kwargs['osauthurl'] = os.environ['OS_AUTH_URL']
            kwargs['ospassword'] = os.environ['OS_PASSWORD']
            if installer_type == 'fuel':
                kwargs['odlwebport'] = '8282'
            elif installer_type == 'apex' or installer_type == 'netvirt':
                kwargs['odlip'] = os.environ['SDN_CONTROLLER_IP']
                kwargs['odlwebport'] = '8081'
                kwargs['odlrestconfport'] = '8081'
            elif installer_type == 'joid':
                kwargs['odlip'] = os.environ['SDN_CONTROLLER']
            elif installer_type == 'compass':
                kwargs['odlwebport'] = '8181'
            else:
                kwargs['odlip'] = os.environ['SDN_CONTROLLER_IP']
        except KeyError as ex:
            self.__logger.error("Cannot run ODL testcases. "
                                "Please check env var: "
                                "%s", str(ex))
            return self.EX_RUN_ERROR
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot run ODL testcases.")
            return self.EX_RUN_ERROR

        return self.main(suites, **kwargs)


class ODLParser(object):  # pylint: disable=too-few-public-methods
    """Parser to run ODL test suites."""

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-n', '--neutronip', help='Neutron IP',
            default='127.0.0.1')
        self.parser.add_argument(
            '-k', '--osauthurl', help='OS_AUTH_URL as defined by OpenStack',
            default='http://127.0.0.1:5000/v2.0')
        self.parser.add_argument(
            '-a', '--osusername', help='Username for OpenStack',
            default='admin')
        self.parser.add_argument(
            '-b', '--ostenantname', help='Tenantname for OpenStack',
            default='admin')
        self.parser.add_argument(
            '-c', '--ospassword', help='Password for OpenStack',
            default='admin')
        self.parser.add_argument(
            '-o', '--odlip', help='OpenDaylight IP',
            default='127.0.0.1')
        self.parser.add_argument(
            '-w', '--odlwebport', help='OpenDaylight Web Portal Port',
            default='8080')
        self.parser.add_argument(
            '-r', '--odlrestconfport', help='OpenDaylight RESTConf Port',
            default='8181')
        self.parser.add_argument(
            '-d', '--odlusername', help='Username for ODL',
            default='admin')
        self.parser.add_argument(
            '-e', '--odlpassword', help='Password for ODL',
            default='admin')
        self.parser.add_argument(
            '-p', '--pushtodb', help='Push results to DB',
            action='store_true')

    def parse_args(self, argv=None):
        """Parse arguments.

        It can call sys.exit if arguments are incorrect.

        Returns:
            the arguments from cmdline
        """
        if not argv:
            argv = []
        return vars(self.parser.parse_args(argv))


if __name__ == '__main__':
    logging.basicConfig()
    ODL = ODLTests()
    PARSER = ODLParser()
    ARGS = PARSER.parse_args(sys.argv[1:])
    try:
        RESULT = ODL.main(ODLTests.default_suites, **ARGS)
        if RESULT != testcase.TestCase.EX_OK:
            sys.exit(RESULT)
        if ARGS['pushtodb']:
            sys.exit(ODL.push_to_db())
    except Exception:  # pylint: disable=broad-except
        sys.exit(testcase.TestCase.EX_RUN_ERROR)
