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
import fileinput
import logging
import os
import re
import sys

import os_client_config
from six.moves import urllib
from xtesting.core import robotframework

from functest.utils import config
from functest.utils import env

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"


class ODLTests(robotframework.RobotFramework):
    """ODL test runner."""

    odl_test_repo = getattr(config.CONF, 'dir_repo_odl_test')
    neutron_suite_dir = os.path.join(
        odl_test_repo, "csit/suites/openstack/neutron")
    basic_suite_dir = os.path.join(
        odl_test_repo, "csit/suites/integration/basic")
    default_suites = [basic_suite_dir, neutron_suite_dir]
    odl_variables_file = os.path.join(
        odl_test_repo, 'csit/variables/Variables.robot')
    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        super(ODLTests, self).__init__(**kwargs)
        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), 'odl')
        self.xml_file = os.path.join(self.res_dir, 'output.xml')

    @classmethod
    def set_robotframework_vars(cls, odlusername="admin", odlpassword="admin"):
        """Set credentials in csit/variables/Variables.robot.

        Returns:
            True if credentials are set.
            False otherwise.
        """

        try:
            for line in fileinput.input(cls.odl_variables_file,
                                        inplace=True):
                print(re.sub("@{AUTH}.*",
                             "@{{AUTH}}           {}    {}".format(
                                 odlusername, odlpassword),
                             line.rstrip()))
            return True
        except Exception:  # pylint: disable=broad-except
            cls.__logger.exception("Cannot set ODL creds:")
            return False

    def run_suites(self, suites=None, **kwargs):
        """Run the test suites

        It has been designed to be called in any context.
        It requires the following keyword arguments:

           * odlusername,
           * odlpassword,
           * osauthurl,
           * neutronurl,
           * osusername,
           * osprojectname,
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
            keystoneurl = "{}://{}".format(
                urllib.parse.urlparse(osauthurl).scheme,
                urllib.parse.urlparse(osauthurl).netloc)
            variable = ['KEYSTONEURL:' + keystoneurl,
                        'NEUTRONURL:' + kwargs['neutronurl'],
                        'OS_AUTH_URL:"' + osauthurl + '"',
                        'OSUSERNAME:"' + kwargs['osusername'] + '"',
                        ('OSUSERDOMAINNAME:"' +
                         kwargs['osuserdomainname'] + '"'),
                        'OSTENANTNAME:"' + kwargs['osprojectname'] + '"',
                        ('OSPROJECTDOMAINNAME:"' +
                         kwargs['osprojectdomainname'] + '"'),
                        'OSPASSWORD:"' + kwargs['ospassword'] + '"',
                        'ODL_SYSTEM_IP:' + kwargs['odlip'],
                        'PORT:' + kwargs['odlwebport'],
                        'RESTCONFPORT:' + kwargs['odlrestconfport']]
        except KeyError:
            self.__logger.exception("Cannot run ODL testcases. Please check")
            return self.EX_RUN_ERROR
        if not os.path.isfile(self.odl_variables_file):
            self.__logger.info("Skip writting ODL creds")
        else:
            if not self.set_robotframework_vars(odlusername, odlpassword):
                return self.EX_RUN_ERROR
        return super(ODLTests, self).run(variable=variable, suites=suites)

    def run(self, **kwargs):
        """Run suites in OPNFV environment

        It basically checks env vars to call main() with the keywords
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
            cloud = os_client_config.make_shade()
            neutron_id = cloud.search_services('neutron')[0].id
            endpoint = cloud.search_endpoints(
                filters={
                    'interface': os.environ.get(
                        'OS_INTERFACE', 'public').replace('URL', ''),
                    'service_id': neutron_id})[0].url
            kwargs = {'neutronurl': endpoint}
            kwargs['odlip'] = env.get('SDN_CONTROLLER_IP')
            kwargs['odlwebport'] = '8080'
            kwargs['odlrestconfport'] = '8181'
            kwargs['odlusername'] = 'admin'
            kwargs['odlpassword'] = 'admin'
            installer_type = env.get('INSTALLER_TYPE')
            kwargs['osusername'] = os.environ['OS_USERNAME']
            kwargs['osuserdomainname'] = os.environ.get(
                'OS_USER_DOMAIN_NAME', 'Default')
            kwargs['osprojectname'] = os.environ['OS_PROJECT_NAME']
            kwargs['osprojectdomainname'] = os.environ.get(
                'OS_PROJECT_DOMAIN_NAME', 'Default')
            kwargs['osauthurl'] = os.environ['OS_AUTH_URL']
            kwargs['ospassword'] = os.environ['OS_PASSWORD']
            if installer_type == 'fuel':
                kwargs['odlwebport'] = '8282'
                kwargs['odlrestconfport'] = '8282'
            elif installer_type == 'apex' or installer_type == 'netvirt':
                kwargs['odlwebport'] = '8081'
                kwargs['odlrestconfport'] = '8081'
            elif installer_type == 'compass':
                kwargs['odlrestconfport'] = '8080'
            elif installer_type == 'daisy':
                kwargs['odlwebport'] = '8181'
                kwargs['odlrestconfport'] = '8087'
            assert kwargs['odlip']
        except KeyError as ex:
            self.__logger.error(
                "Cannot run ODL testcases. Please check env var: %s", str(ex))
            return self.EX_RUN_ERROR
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot run ODL testcases.")
            return self.EX_RUN_ERROR

        return self.run_suites(suites, **kwargs)


class ODLParser(object):  # pylint: disable=too-few-public-methods
    """Parser to run ODL test suites."""

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-n', '--neutronurl', help='Neutron Endpoint',
            default='http://127.0.0.1:9696')
        self.parser.add_argument(
            '-k', '--osauthurl', help='OS_AUTH_URL as defined by OpenStack',
            default='http://127.0.0.1:5000/v3')
        self.parser.add_argument(
            '-a', '--osusername', help='Username for OpenStack',
            default='admin')
        self.parser.add_argument(
            '-f', '--osuserdomainname', help='User domain name for OpenStack',
            default='Default')
        self.parser.add_argument(
            '-b', '--osprojectname', help='Projet name for OpenStack',
            default='admin')
        self.parser.add_argument(
            '-g', '--osprojectdomainname',
            help='Project domain name for OpenStack',
            default='Default')
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


def main():
    """Entry point"""
    logging.basicConfig()
    odl = ODLTests()
    parser = ODLParser()
    args = parser.parse_args(sys.argv[1:])
    try:
        result = odl.run_suites(ODLTests.default_suites, **args)
        if result != robotframework.RobotFramework.EX_OK:
            return result
        if args['pushtodb']:
            return odl.push_to_db()
        return result
    except Exception:  # pylint: disable=broad-except
        return robotframework.RobotFramework.EX_RUN_ERROR
