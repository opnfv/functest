#!/usr/bin/env python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

"""Rally testcases implementation."""

from __future__ import division

import json
import logging
import os
import re
import subprocess
import time
import uuid

import pkg_resources
import yaml

from functest.core import testcase
from functest.energy import energy
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils.constants import CONST

from snaps.config.flavor import FlavorConfig
from snaps.config.image import ImageConfig
from snaps.config.network import NetworkConfig, SubnetConfig
from snaps.config.router import RouterConfig

from snaps.openstack.create_flavor import OpenStackFlavor
from snaps.openstack.tests import openstack_tests
from snaps.openstack.utils import deploy_utils

LOGGER = logging.getLogger(__name__)


class RallyBase(testcase.TestCase):
    """Base class form Rally testcases implementation."""

    TESTS = ['authenticate', 'glance', 'ceilometer', 'cinder', 'heat',
             'keystone', 'neutron', 'nova', 'quotas', 'vm', 'all']
    GLANCE_IMAGE_NAME = CONST.__getattribute__('openstack_image_name')
    GLANCE_IMAGE_FILENAME = CONST.__getattribute__('openstack_image_file_name')
    GLANCE_IMAGE_PATH = os.path.join(
        CONST.__getattribute__('dir_functest_images'),
        GLANCE_IMAGE_FILENAME)
    GLANCE_IMAGE_FORMAT = CONST.__getattribute__('openstack_image_disk_format')
    GLANCE_IMAGE_USERNAME = CONST.__getattribute__('openstack_image_username')
    GLANCE_IMAGE_EXTRA_PROPERTIES = {}
    if hasattr(CONST, 'openstack_extra_properties'):
        GLANCE_IMAGE_EXTRA_PROPERTIES = CONST.__getattribute__(
            'openstack_extra_properties')
    FLAVOR_NAME = CONST.__getattribute__('rally_flavor_name')
    FLAVOR_ALT_NAME = CONST.__getattribute__('rally_flavor_alt_name')
    FLAVOR_EXTRA_SPECS = None
    if hasattr(CONST, 'flavor_extra_specs'):
        FLAVOR_EXTRA_SPECS = CONST.__getattribute__('flavor_extra_specs')

    RALLY_DIR = pkg_resources.resource_filename(
        'functest', 'opnfv_tests/openstack/rally')
    RALLY_SCENARIO_DIR = pkg_resources.resource_filename(
        'functest', 'opnfv_tests/openstack/rally/scenario')
    TEMPLATE_DIR = pkg_resources.resource_filename(
        'functest', 'opnfv_tests/openstack/rally/scenario/templates')
    SUPPORT_DIR = pkg_resources.resource_filename(
        'functest', 'opnfv_tests/openstack/rally/scenario/support')
    USERS_AMOUNT = 2
    TENANTS_AMOUNT = 3
    ITERATIONS_AMOUNT = 10
    CONCURRENCY = 4
    RESULTS_DIR = os.path.join(CONST.__getattribute__('dir_results'), 'rally')
    BLACKLIST_FILE = os.path.join(RALLY_DIR, "blacklist.txt")
    TEMP_DIR = os.path.join(RALLY_DIR, "var")

    RALLY_PRIVATE_NET_NAME = CONST.__getattribute__('rally_network_name')
    RALLY_PRIVATE_SUBNET_NAME = CONST.__getattribute__('rally_subnet_name')
    RALLY_PRIVATE_SUBNET_CIDR = CONST.__getattribute__('rally_subnet_cidr')
    RALLY_ROUTER_NAME = CONST.__getattribute__('rally_router_name')

    def __init__(self, **kwargs):
        """Initialize RallyBase object."""
        super(RallyBase, self).__init__(**kwargs)
        if 'os_creds' in kwargs:
            self.os_creds = kwargs['os_creds']
        else:
            creds_override = None
            if hasattr(CONST, 'snaps_os_creds_override'):
                creds_override = CONST.__getattribute__(
                    'snaps_os_creds_override')

            self.os_creds = openstack_tests.get_credentials(
                os_env_file=CONST.__getattribute__('openstack_creds'),
                overrides=creds_override)

        self.guid = '-' + str(uuid.uuid4())

        self.creators = []
        self.mode = ''
        self.summary = []
        self.scenario_dir = ''
        self.image_name = None
        self.ext_net_name = None
        self.priv_net_id = None
        self.flavor_name = None
        self.flavor_alt_name = None
        self.smoke = None
        self.test_name = None
        self.start_time = None
        self.result = None
        self.details = None
        self.compute_cnt = 0

    def _build_task_args(self, test_file_name):
        task_args = {'service_list': [test_file_name]}
        task_args['image_name'] = self.image_name
        task_args['flavor_name'] = self.flavor_name
        task_args['flavor_alt_name'] = self.flavor_alt_name
        task_args['glance_image_location'] = self.GLANCE_IMAGE_PATH
        task_args['glance_image_format'] = self.GLANCE_IMAGE_FORMAT
        task_args['tmpl_dir'] = self.TEMPLATE_DIR
        task_args['sup_dir'] = self.SUPPORT_DIR
        task_args['users_amount'] = self.USERS_AMOUNT
        task_args['tenants_amount'] = self.TENANTS_AMOUNT
        task_args['use_existing_users'] = False
        task_args['iterations'] = self.ITERATIONS_AMOUNT
        task_args['concurrency'] = self.CONCURRENCY
        task_args['smoke'] = self.smoke

        ext_net = self.ext_net_name
        if ext_net:
            task_args['floating_network'] = str(ext_net)
        else:
            task_args['floating_network'] = ''

        net_id = self.priv_net_id
        if net_id:
            task_args['netid'] = str(net_id)
        else:
            task_args['netid'] = ''

        return task_args

    def _prepare_test_list(self, test_name):
        test_yaml_file_name = 'opnfv-{}.yaml'.format(test_name)
        scenario_file_name = os.path.join(self.RALLY_SCENARIO_DIR,
                                          test_yaml_file_name)

        if not os.path.exists(scenario_file_name):
            scenario_file_name = os.path.join(self.scenario_dir,
                                              test_yaml_file_name)

            if not os.path.exists(scenario_file_name):
                raise Exception("The scenario '%s' does not exist."
                                % scenario_file_name)

        LOGGER.debug('Scenario fetched from : %s', scenario_file_name)
        test_file_name = os.path.join(self.TEMP_DIR, test_yaml_file_name)

        if not os.path.exists(self.TEMP_DIR):
            os.makedirs(self.TEMP_DIR)

        self._apply_blacklist(scenario_file_name, test_file_name)
        return test_file_name

    @staticmethod
    def get_task_id(cmd_raw):
        """
        Get task id from command rally result.

        :param cmd_raw:
        :return: task_id as string
        """
        taskid_re = re.compile('^Task +(.*): started$')
        for line in cmd_raw.splitlines(True):
            line = line.strip()
            match = taskid_re.match(line)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def task_succeed(json_raw):
        """
        Parse JSON from rally JSON results.

        :param json_raw:
        :return: Bool
        """
        rally_report = json.loads(json_raw)
        for report in rally_report:
            if report is None or report.get('result') is None:
                return False

            for result in report.get('result'):
                if result is None or len(result.get('error')) > 0:
                    return False

        return True

    def _migration_supported(self):
        """Determine if migration is supported."""
        if self.compute_cnt > 1:
            return True

        return False

    @staticmethod
    def get_cmd_output(proc):
        """Get command stdout."""
        result = ""
        while proc.poll() is None:
            line = proc.stdout.readline()
            result += line
        return result

    @staticmethod
    def excl_scenario():
        """Exclude scenario."""
        black_tests = []
        try:
            with open(RallyBase.BLACKLIST_FILE, 'r') as black_list_file:
                black_list_yaml = yaml.safe_load(black_list_file)

            installer_type = CONST.__getattribute__('INSTALLER_TYPE')
            deploy_scenario = CONST.__getattribute__('DEPLOY_SCENARIO')
            if (bool(installer_type) and bool(deploy_scenario) and
                    'scenario' in black_list_yaml.keys()):
                for item in black_list_yaml['scenario']:
                    scenarios = item['scenarios']
                    installers = item['installers']
                    in_it = RallyBase.in_iterable_re
                    if (in_it(deploy_scenario, scenarios) and
                            in_it(installer_type, installers)):
                        tests = item['tests']
                        black_tests.extend(tests)
        except Exception:
            LOGGER.debug("Scenario exclusion not applied.")

        return black_tests

    @staticmethod
    def in_iterable_re(needle, haystack):
        """
        Check if given needle is in the iterable haystack, using regex.

        :param needle: string to be matched
        :param haystack: iterable of strings (optionally regex patterns)
        :return: True if needle is eqial to any of the elements in haystack,
                 or if a nonempty regex pattern in haystack is found in needle.
        """
        # match without regex
        if needle in haystack:
            return True

        for pattern in haystack:
            # match if regex pattern is set and found in the needle
            if pattern and re.search(pattern, needle) is not None:
                return True
        else:
            return False

    def excl_func(self):
        """Exclude functionalities."""
        black_tests = []
        func_list = []

        try:
            with open(RallyBase.BLACKLIST_FILE, 'r') as black_list_file:
                black_list_yaml = yaml.safe_load(black_list_file)

            if not self._migration_supported():
                func_list.append("no_migration")

            if 'functionality' in black_list_yaml.keys():
                for item in black_list_yaml['functionality']:
                    functions = item['functions']
                    for func in func_list:
                        if func in functions:
                            tests = item['tests']
                            black_tests.extend(tests)
        except Exception:  # pylint: disable=broad-except
            LOGGER.debug("Functionality exclusion not applied.")

        return black_tests

    def _apply_blacklist(self, case_file_name, result_file_name):
        """Apply blacklist."""
        LOGGER.debug("Applying blacklist...")
        cases_file = open(case_file_name, 'r')
        result_file = open(result_file_name, 'w')

        black_tests = list(set(self.excl_func() +
                               self.excl_scenario()))

        if black_tests:
            LOGGER.debug("Blacklisted tests: " + str(black_tests))

        include = True
        for cases_line in cases_file:
            if include:
                for black_tests_line in black_tests:
                    if re.search(black_tests_line,
                                 cases_line.strip().rstrip(':')):
                        include = False
                        break
                else:
                    result_file.write(str(cases_line))
            else:
                if cases_line.isspace():
                    include = True

        cases_file.close()
        result_file.close()

    @staticmethod
    def file_is_empty(file_name):
        """Determine is a file is empty."""
        try:
            if os.stat(file_name).st_size > 0:
                return False
        except Exception:  # pylint: disable=broad-except
            pass

        return True

    def _run_task(self, test_name):
        """Run a task."""
        LOGGER.info('Starting test scenario "%s" ...', test_name)

        task_file = os.path.join(self.RALLY_DIR, 'task.yaml')
        if not os.path.exists(task_file):
            LOGGER.error("Task file '%s' does not exist.", task_file)
            raise Exception("Task file '%s' does not exist.", task_file)

        file_name = self._prepare_test_list(test_name)
        if self.file_is_empty(file_name):
            LOGGER.info('No tests for scenario "%s"', test_name)
            return

        cmd = (["rally", "task", "start", "--abort-on-sla-failure", "--task",
                task_file, "--task-args",
                str(self._build_task_args(test_name))])
        LOGGER.debug('running command: %s', cmd)

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output = self._get_output(proc, test_name)
        task_id = self.get_task_id(output)
        LOGGER.debug('task_id : %s', task_id)

        if task_id is None:
            LOGGER.error('Failed to retrieve task_id, validating task...')
            cmd = (["rally", "task", "validate", "--task", task_file,
                    "--task-args", str(self._build_task_args(test_name))])
            LOGGER.debug('running command: %s', cmd)
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            output = self.get_cmd_output(proc)
            LOGGER.error("Task validation result:" + "\n" + output)
            return

        # check for result directory and create it otherwise
        if not os.path.exists(self.RESULTS_DIR):
            LOGGER.debug('%s does not exist, we create it.',
                         self.RESULTS_DIR)
            os.makedirs(self.RESULTS_DIR)

        # write html report file
        report_html_name = 'opnfv-{}.html'.format(test_name)
        report_html_dir = os.path.join(self.RESULTS_DIR, report_html_name)
        cmd = (["rally", "task", "report", task_id, "--out", report_html_dir])

        LOGGER.debug('running command: %s', cmd)
        subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

        # get and save rally operation JSON result
        cmd = (["rally", "task", "results", task_id])
        LOGGER.debug('running command: %s', cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        json_results = self.get_cmd_output(proc)
        report_json_name = 'opnfv-{}.json'.format(test_name)
        report_json_dir = os.path.join(self.RESULTS_DIR, report_json_name)
        with open(report_json_dir, 'w') as r_file:
            LOGGER.debug('saving json file')
            r_file.write(json_results)

        # parse JSON operation result
        if self.task_succeed(json_results):
            LOGGER.info('Test scenario: "{}" OK.'.format(test_name) + "\n")
        else:
            LOGGER.info('Test scenario: "{}" Failed.'.format(test_name) + "\n")

    def _get_output(self, proc, test_name):
        result = ""
        nb_tests = 0
        overall_duration = 0.0
        success = 0.0
        nb_totals = 0

        while proc.poll() is None:
            line = proc.stdout.readline()
            if ("Load duration" in line or
                    "started" in line or
                    "finished" in line or
                    " Preparing" in line or
                    "+-" in line or
                    "|" in line):
                result += line
            elif "test scenario" in line:
                result += "\n" + line
            elif "Full duration" in line:
                result += line + "\n\n"

            # parse output for summary report
            if ("| " in line and
                    "| action" not in line and
                    "| Starting" not in line and
                    "| Completed" not in line and
                    "| ITER" not in line and
                    "|   " not in line and
                    "| total" not in line):
                nb_tests += 1
            elif "| total" in line:
                percentage = ((line.split('|')[8]).strip(' ')).strip('%')
                try:
                    success += float(percentage)
                except ValueError:
                    LOGGER.info('Percentage error: %s, %s',
                                percentage, line)
                nb_totals += 1
            elif "Full duration" in line:
                duration = line.split(': ')[1]
                try:
                    overall_duration += float(duration)
                except ValueError:
                    LOGGER.info('Duration error: %s, %s', duration, line)

        overall_duration = "{:10.2f}".format(overall_duration)
        if nb_totals == 0:
            success_avg = 0
        else:
            success_avg = "{:0.2f}".format(success / nb_totals)

        scenario_summary = {'test_name': test_name,
                            'overall_duration': overall_duration,
                            'nb_tests': nb_tests,
                            'success': success_avg}
        self.summary.append(scenario_summary)

        LOGGER.debug("\n" + result)

        return result

    def _prepare_env(self):
        LOGGER.debug('Validating the test name...')
        if self.test_name not in self.TESTS:
            raise Exception("Test name '%s' is invalid" % self.test_name)

        network_name = self.RALLY_PRIVATE_NET_NAME + self.guid
        subnet_name = self.RALLY_PRIVATE_SUBNET_NAME + self.guid
        router_name = self.RALLY_ROUTER_NAME + self.guid
        self.image_name = self.GLANCE_IMAGE_NAME + self.guid
        self.flavor_name = self.FLAVOR_NAME + self.guid
        self.flavor_alt_name = self.FLAVOR_ALT_NAME + self.guid
        self.ext_net_name = snaps_utils.get_ext_net_name(self.os_creds)
        self.compute_cnt = snaps_utils.get_active_compute_cnt(self.os_creds)

        LOGGER.debug("Creating image '%s'...", self.image_name)
        image_creator = deploy_utils.create_image(
            self.os_creds, ImageConfig(
                name=self.image_name,
                image_file=self.GLANCE_IMAGE_PATH,
                img_format=self.GLANCE_IMAGE_FORMAT,
                image_user=self.GLANCE_IMAGE_USERNAME,
                public=True,
                extra_properties=self.GLANCE_IMAGE_EXTRA_PROPERTIES))
        if image_creator is None:
            raise Exception("Failed to create image")
        self.creators.append(image_creator)

        LOGGER.debug("Creating network '%s'...", network_name)
        network_creator = deploy_utils.create_network(
            self.os_creds, NetworkConfig(
                name=network_name,
                shared=True,
                subnet_settings=[SubnetConfig(
                    name=subnet_name,
                    cidr=self.RALLY_PRIVATE_SUBNET_CIDR)
                ]))
        if network_creator is None:
            raise Exception("Failed to create private network")
        self.priv_net_id = network_creator.get_network().id
        self.creators.append(network_creator)

        LOGGER.debug("Creating router '%s'...", router_name)
        router_creator = deploy_utils.create_router(
            self.os_creds, RouterConfig(
                name=router_name,
                external_gateway=self.ext_net_name,
                internal_subnets=[subnet_name]))
        if router_creator is None:
            raise Exception("Failed to create router")
        self.creators.append(router_creator)

        LOGGER.debug("Creating flavor '%s'...", self.flavor_name)
        flavor_creator = OpenStackFlavor(
            self.os_creds, FlavorConfig(
                name=self.flavor_name, ram=512, disk=1, vcpus=1,
                metadata=self.FLAVOR_EXTRA_SPECS))
        if flavor_creator is None or flavor_creator.create() is None:
            raise Exception("Failed to create flavor")
        self.creators.append(flavor_creator)

        LOGGER.debug("Creating flavor '%s'...", self.flavor_alt_name)
        flavor_alt_creator = OpenStackFlavor(
            self.os_creds, FlavorConfig(
                name=self.flavor_alt_name, ram=1024, disk=1, vcpus=1,
                metadata=self.FLAVOR_EXTRA_SPECS))
        if flavor_alt_creator is None or flavor_alt_creator.create() is None:
            raise Exception("Failed to create flavor")
        self.creators.append(flavor_alt_creator)

    def _run_tests(self):
        if self.test_name == 'all':
            for test in self.TESTS:
                if test == 'all' or test == 'vm':
                    continue
                self._run_task(test)
        else:
            self._run_task(self.test_name)

    def _generate_report(self):
        report = (
            "\n"
            "                                                              "
            "\n"
            "                     Rally Summary Report\n"
            "\n"
            "+===================+============+===============+===========+"
            "\n"
            "| Module            | Duration   | nb. Test Run  | Success   |"
            "\n"
            "+===================+============+===============+===========+"
            "\n")
        payload = []

        # for each scenario we draw a row for the table
        total_duration = 0.0
        total_nb_tests = 0
        total_success = 0.0
        for item in self.summary:
            name = "{0:<17}".format(item['test_name'])
            duration = float(item['overall_duration'])
            total_duration += duration
            duration = time.strftime("%M:%S", time.gmtime(duration))
            duration = "{0:<10}".format(duration)
            nb_tests = "{0:<13}".format(item['nb_tests'])
            total_nb_tests += int(item['nb_tests'])
            success = "{0:<10}".format(str(item['success']) + '%')
            total_success += float(item['success'])
            report += ("" +
                       "| " + name + " | " + duration + " | " +
                       nb_tests + " | " + success + "|\n" +
                       "+-------------------+------------"
                       "+---------------+-----------+\n")
            payload.append({'module': name,
                            'details': {'duration': item['overall_duration'],
                                        'nb tests': item['nb_tests'],
                                        'success': item['success']}})

        total_duration_str = time.strftime("%H:%M:%S",
                                           time.gmtime(total_duration))
        total_duration_str2 = "{0:<10}".format(total_duration_str)
        total_nb_tests_str = "{0:<13}".format(total_nb_tests)

        try:
            self.result = total_success / len(self.summary)
        except ZeroDivisionError:
            self.result = 100

        success_rate = "{:0.2f}".format(self.result)
        success_rate_str = "{0:<10}".format(str(success_rate) + '%')
        report += ("+===================+============"
                   "+===============+===========+")
        report += "\n"
        report += ("| TOTAL:            | " + total_duration_str2 + " | " +
                   total_nb_tests_str + " | " + success_rate_str + "|\n")
        report += ("+===================+============"
                   "+===============+===========+")
        report += "\n"

        LOGGER.info("\n" + report)
        payload.append({'summary': {'duration': total_duration,
                                    'nb tests': total_nb_tests,
                                    'nb success': success_rate}})

        self.details = payload

        LOGGER.info("Rally '%s' success_rate is %s%%",
                    self.case_name, success_rate)

    def _clean_up(self):
        for creator in reversed(self.creators):
            try:
                creator.clean()
            except Exception as e:
                LOGGER.error('Unexpected error cleaning - %s', e)

    @energy.enable_recording
    def run(self, **kwargs):
        """Run testcase."""
        self.start_time = time.time()
        try:
            conf_utils.create_rally_deployment()
            self._prepare_env()
            self._run_tests()
            self._generate_report()
            res = testcase.TestCase.EX_OK
        except Exception as exc:   # pylint: disable=broad-except
            LOGGER.error('Error with run: %s', exc)
            res = testcase.TestCase.EX_RUN_ERROR
        finally:
            self._clean_up()

        self.stop_time = time.time()
        return res


class RallySanity(RallyBase):
    """Rally sanity testcase implementation."""

    def __init__(self, **kwargs):
        """Initialize RallySanity object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "rally_sanity"
        super(RallySanity, self).__init__(**kwargs)
        self.mode = 'sanity'
        self.test_name = 'all'
        self.smoke = True
        self.scenario_dir = os.path.join(self.RALLY_SCENARIO_DIR, 'sanity')


class RallyFull(RallyBase):
    """Rally full testcase implementation."""

    def __init__(self, **kwargs):
        """Initialize RallyFull object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "rally_full"
        super(RallyFull, self).__init__(**kwargs)
        self.mode = 'full'
        self.test_name = 'all'
        self.smoke = False
        self.scenario_dir = os.path.join(self.RALLY_SCENARIO_DIR, 'full')
