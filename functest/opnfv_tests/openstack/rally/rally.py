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
import shutil
import subprocess
import time

import pkg_resources
import prettytable
from ruamel.yaml import YAML
from six.moves import configparser
from xtesting.core import testcase
from xtesting.energy import energy
import yaml

from functest.core import singlevm
from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils import config
from functest.utils import env

LOGGER = logging.getLogger(__name__)


class RallyBase(singlevm.VmReady2):
    """Base class form Rally testcases implementation."""

    # pylint: disable=too-many-instance-attributes
    TESTS = ['authenticate', 'glance', 'cinder', 'gnocchi', 'heat',
             'keystone', 'neutron', 'nova', 'quotas']

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
    BLACKLIST_FILE = os.path.join(RALLY_DIR, "blacklist.txt")
    TEMP_DIR = os.path.join(RALLY_DIR, "var")

    visibility = 'public'
    shared_network = True

    def __init__(self, **kwargs):
        """Initialize RallyBase object."""
        super(RallyBase, self).__init__(**kwargs)
        assert self.orig_cloud
        assert self.project
        if self.orig_cloud.get_role("admin"):
            role_name = "admin"
        elif self.orig_cloud.get_role("Admin"):
            role_name = "Admin"
        else:
            raise Exception("Cannot detect neither admin nor Admin")
        self.orig_cloud.grant_role(
            role_name, user=self.project.user.id,
            project=self.project.project.id,
            domain=self.project.domain.id)
        self.results_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), self.case_name)
        self.task_file = os.path.join(self.RALLY_DIR, 'task.yaml')
        self.creators = []
        self.summary = []
        self.scenario_dir = ''
        self.smoke = None
        self.test_name = None
        self.start_time = None
        self.result = None
        self.details = None
        self.compute_cnt = 0
        self.flavor_alt = None
        self.tests = []
        self.run_cmd = ''
        self.network_extensions = []

    def _build_task_args(self, test_file_name):
        """Build arguments for the Rally task."""
        task_args = {'service_list': [test_file_name]}
        task_args['image_name'] = str(self.image.name)
        task_args['flavor_name'] = str(self.flavor.name)
        task_args['flavor_alt_name'] = str(self.flavor_alt.name)
        task_args['glance_image_location'] = str(self.filename)
        task_args['glance_image_format'] = str(self.image_format)
        task_args['tmpl_dir'] = str(self.TEMPLATE_DIR)
        task_args['sup_dir'] = str(self.SUPPORT_DIR)
        task_args['users_amount'] = self.USERS_AMOUNT
        task_args['tenants_amount'] = self.TENANTS_AMOUNT
        task_args['use_existing_users'] = False
        task_args['iterations'] = self.ITERATIONS_AMOUNT
        task_args['concurrency'] = self.CONCURRENCY
        task_args['smoke'] = self.smoke

        if self.ext_net:
            task_args['floating_network'] = str(self.ext_net.name)
        else:
            task_args['floating_network'] = ''

        if self.network:
            task_args['netid'] = str(self.network.id)
        else:
            task_args['netid'] = ''

        return task_args

    def _prepare_test_list(self, test_name):
        """Build the list of test cases to be executed."""
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

        self.apply_blacklist(scenario_file_name, test_file_name)
        return test_file_name

    @staticmethod
    def update_keystone_default_role(rally_conf='/etc/rally/rally.conf'):
        """Set keystone_default_role in rally.conf"""
        if env.get("NEW_USER_ROLE").lower() != "member":
            rconfig = configparser.RawConfigParser()
            rconfig.read(rally_conf)
            if not rconfig.has_section('openstack'):
                rconfig.add_section('openstack')
            rconfig.set(
                'openstack', 'keystone_default_role', env.get("NEW_USER_ROLE"))
            with open(rally_conf, 'wb') as config_file:
                rconfig.write(config_file)

    @staticmethod
    def clean_rally_conf(rally_conf='/etc/rally/rally.conf'):
        """Clean Rally config"""
        if env.get("NEW_USER_ROLE").lower() != "member":
            rconfig = configparser.RawConfigParser()
            rconfig.read(rally_conf)
            if rconfig.has_option('openstack', 'keystone_default_role'):
                rconfig.remove_option('openstack', 'keystone_default_role')
            with open(rally_conf, 'wb') as config_file:
                rconfig.write(config_file)

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
        tasks = rally_report.get('tasks')
        if tasks:
            for task in tasks:
                if task.get('status') != 'finished' or \
                   task.get('pass_sla') is not True:
                    return False
        else:
            return False
        return True

    def _migration_supported(self):
        """Determine if migration is supported."""
        if self.compute_cnt > 1:
            return True
        return False

    def _network_trunk_supported(self):
        """Determine if network trunk service is available"""
        if 'trunk' in self.network_extensions:
            return True
        return False

    @staticmethod
    def excl_scenario():
        """Exclude scenario."""
        black_tests = []
        try:
            with open(RallyBase.BLACKLIST_FILE, 'r') as black_list_file:
                black_list_yaml = yaml.safe_load(black_list_file)

            deploy_scenario = env.get('DEPLOY_SCENARIO')
            if (bool(deploy_scenario) and
                    'scenario' in black_list_yaml.keys()):
                for item in black_list_yaml['scenario']:
                    scenarios = item['scenarios']
                    in_it = RallyBase.in_iterable_re
                    if in_it(deploy_scenario, scenarios):
                        tests = item['tests']
                        black_tests.extend(tests)
        except Exception:  # pylint: disable=broad-except
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
            if not self._network_trunk_supported():
                func_list.append("no_net_trunk_service")

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

    def apply_blacklist(self, case_file_name, result_file_name):
        """Apply blacklist."""
        LOGGER.debug("Applying blacklist...")
        cases_file = open(case_file_name, 'r')
        result_file = open(result_file_name, 'w')

        black_tests = list(set(self.excl_func() +
                               self.excl_scenario()))

        if black_tests:
            LOGGER.debug("Blacklisted tests: %s", str(black_tests))

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

    def _save_results(self, test_name, task_id):
        """ Generate and save task execution results"""
        # check for result directory and create it otherwise
        if not os.path.exists(self.results_dir):
            LOGGER.debug('%s does not exist, we create it.',
                         self.results_dir)
            os.makedirs(self.results_dir)

        # put detailed result to log
        cmd = (["rally", "task", "detailed", "--uuid", task_id])
        LOGGER.debug('running command: %s', cmd)
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        LOGGER.info("%s\n%s", " ".join(cmd), output)

        # save report as JSON
        report_json_name = '{}.json'.format(test_name)
        report_json_dir = os.path.join(self.results_dir, report_json_name)
        cmd = (["rally", "task", "report", "--json", "--uuid", task_id,
                "--out", report_json_dir])
        LOGGER.debug('running command: %s', cmd)
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        LOGGER.info("%s\n%s", " ".join(cmd), output)

        # save report as HTML
        report_html_name = '{}.html'.format(test_name)
        report_html_dir = os.path.join(self.results_dir, report_html_name)
        cmd = (["rally", "task", "report", "--html", "--uuid", task_id,
                "--out", report_html_dir])
        LOGGER.debug('running command: %s', cmd)
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        LOGGER.info("%s\n%s", " ".join(cmd), output)

        json_results = open(report_json_dir).read()
        self._append_summary(json_results, test_name)

        # parse JSON operation result
        if self.task_succeed(json_results):
            LOGGER.info('Test scenario: "%s" OK.', test_name)
        else:
            LOGGER.info('Test scenario: "%s" Failed.', test_name)

    def run_task(self, test_name):
        """Run a task."""
        LOGGER.info('Starting test scenario "%s" ...', test_name)
        LOGGER.debug('running command: %s', self.run_cmd)
        proc = subprocess.Popen(self.run_cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output = proc.communicate()[0]

        task_id = self.get_task_id(output)
        LOGGER.debug('task_id : %s', task_id)
        if task_id is None:
            LOGGER.error("Failed to retrieve task_id")
            LOGGER.error("Result:\n%s", output)
            raise Exception("Failed to retrieve task id")
        self._save_results(test_name, task_id)

    def _append_summary(self, json_raw, test_name):
        """Update statistics summary info."""
        nb_tests = 0
        nb_success = 0
        overall_duration = 0.0

        rally_report = json.loads(json_raw)
        for task in rally_report.get('tasks'):
            for subtask in task.get('subtasks'):
                for workload in subtask.get('workloads'):
                    if workload.get('full_duration'):
                        overall_duration += workload.get('full_duration')

                    if workload.get('data'):
                        nb_tests += len(workload.get('data'))

                    for result in workload.get('data'):
                        if not result.get('error'):
                            nb_success += 1

        scenario_summary = {'test_name': test_name,
                            'overall_duration': overall_duration,
                            'nb_tests': nb_tests,
                            'nb_success': nb_success,
                            'task_status': self.task_succeed(json_raw)}
        self.summary.append(scenario_summary)

    def prepare_run(self):
        """Prepare resources needed by test scenarios."""
        assert self.cloud
        LOGGER.debug('Validating the test name...')
        if self.test_name == 'all':
            self.tests = self.TESTS
        elif self.test_name in self.TESTS:
            self.tests = [self.test_name]
        else:
            raise Exception("Test name '%s' is invalid" % self.test_name)

        if not os.path.exists(self.task_file):
            LOGGER.error("Task file '%s' does not exist.", self.task_file)
            raise Exception("Task file '{}' does not exist.".
                            format(self.task_file))

        self.update_keystone_default_role()
        self.compute_cnt = len(self.cloud.list_hypervisors())
        self.network_extensions = self.cloud.get_network_extensions()
        self.flavor_alt = self.create_flavor_alt()
        LOGGER.debug("flavor: %s", self.flavor_alt)

    def prepare_task(self, test_name):
        """Prepare resources for test run."""
        file_name = self._prepare_test_list(test_name)
        if self.file_is_empty(file_name):
            LOGGER.info('No tests for scenario "%s"', test_name)
            return False
        self.run_cmd = (["rally", "task", "start", "--abort-on-sla-failure",
                         "--task", self.task_file, "--task-args",
                         str(self._build_task_args(test_name))])
        return True

    def run_tests(self):
        """Execute tests."""
        for test in self.tests:
            if self.prepare_task(test):
                self.run_task(test)

    def _generate_report(self):
        """Generate test execution summary report."""
        total_duration = 0.0
        total_nb_tests = 0
        total_nb_success = 0
        nb_modules = 0
        payload = []

        res_table = prettytable.PrettyTable(
            padding_width=2,
            field_names=['Module', 'Duration', 'nb. Test Run', 'Success'])
        res_table.align['Module'] = "l"
        res_table.align['Duration'] = "r"
        res_table.align['Success'] = "r"

        # for each scenario we draw a row for the table
        for item in self.summary:
            if item['task_status'] is True:
                nb_modules += 1
            total_duration += item['overall_duration']
            total_nb_tests += item['nb_tests']
            total_nb_success += item['nb_success']
            try:
                success_avg = 100 * item['nb_success'] / item['nb_tests']
            except ZeroDivisionError:
                success_avg = 0
            success_str = str("{:0.2f}".format(success_avg)) + '%'
            duration_str = time.strftime("%H:%M:%S",
                                         time.gmtime(item['overall_duration']))
            res_table.add_row([item['test_name'], duration_str,
                               item['nb_tests'], success_str])
            payload.append({'module': item['test_name'],
                            'details': {'duration': item['overall_duration'],
                                        'nb tests': item['nb_tests'],
                                        'success': success_str}})

        total_duration_str = time.strftime("%H:%M:%S",
                                           time.gmtime(total_duration))
        try:
            self.result = 100 * total_nb_success / total_nb_tests
        except ZeroDivisionError:
            self.result = 100
        success_rate = "{:0.2f}".format(self.result)
        success_rate_str = str(success_rate) + '%'
        res_table.add_row(["", "", "", ""])
        res_table.add_row(["TOTAL:", total_duration_str, total_nb_tests,
                           success_rate_str])

        LOGGER.info("Rally Summary Report:\n\n%s\n", res_table.get_string())
        LOGGER.info("Rally '%s' success_rate is %s%% in %s/%s modules",
                    self.case_name, success_rate, nb_modules,
                    len(self.summary))
        payload.append({'summary': {'duration': total_duration,
                                    'nb tests': total_nb_tests,
                                    'nb success': success_rate}})
        self.details = payload

    def clean(self):
        """Cleanup of OpenStack resources. Should be called on completion."""
        self.clean_rally_conf()
        if self.flavor_alt:
            self.orig_cloud.delete_flavor(self.flavor_alt.id)
        super(RallyBase, self).clean()

    def is_successful(self):
        """The overall result of the test."""
        for item in self.summary:
            if item['task_status'] is False:
                return testcase.TestCase.EX_TESTCASE_FAILED

        return super(RallyBase, self).is_successful()

    @energy.enable_recording
    def run(self, **kwargs):
        """Run testcase."""
        self.start_time = time.time()
        try:
            assert super(RallyBase, self).run(
                **kwargs) == testcase.TestCase.EX_OK
            environ = dict(
                os.environ,
                OS_USERNAME=self.project.user.name,
                OS_PROJECT_NAME=self.project.project.name,
                OS_PROJECT_ID=self.project.project.id,
                OS_PASSWORD=self.project.password)
            conf_utils.create_rally_deployment(environ=environ)
            self.prepare_run()
            self.run_tests()
            self._generate_report()
            res = testcase.TestCase.EX_OK
        except Exception as exc:   # pylint: disable=broad-except
            LOGGER.error('Error with run: %s', exc)
            self.result = 0
            res = testcase.TestCase.EX_RUN_ERROR
        self.stop_time = time.time()
        return res


class RallySanity(RallyBase):
    """Rally sanity testcase implementation."""

    def __init__(self, **kwargs):
        """Initialize RallySanity object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "rally_sanity"
        super(RallySanity, self).__init__(**kwargs)
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
        self.test_name = 'all'
        self.smoke = False
        self.scenario_dir = os.path.join(self.RALLY_SCENARIO_DIR, 'full')


class RallyJobs(RallyBase):
    """Rally OpenStack CI testcase implementation."""

    TESTS = ["neutron"]

    def __init__(self, **kwargs):
        """Initialize RallyJobs object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "rally_jobs"
        super(RallyJobs, self).__init__(**kwargs)
        self.test_name = 'all'
        self.task_file = os.path.join(self.RALLY_DIR, 'rally_jobs.yaml')
        self.task_yaml = None

    def prepare_run(self):
        """Create resources needed by test scenarios."""
        super(RallyJobs, self).prepare_run()
        with open(os.path.join(self.RALLY_DIR,
                               'rally_jobs.yaml'), 'r') as task_file:
            self.task_yaml = yaml.safe_load(task_file)

        if not all(task in self.task_yaml for task in self.tests):
            raise Exception("Test '%s' not in '%s'" %
                            (self.test_name, self.tests))

    def apply_blacklist(self, case_file_name, result_file_name):
        # pylint: disable=too-many-branches
        """Apply blacklist."""
        LOGGER.debug("Applying blacklist...")
        black_tests = list(set(self.excl_func() +
                               self.excl_scenario()))
        if black_tests:
            LOGGER.debug("Blacklisted tests: %s", str(black_tests))

        template = YAML(typ='jinja2')
        with open(case_file_name, 'r') as fname:
            cases = template.load(fname)
        if cases.get("version", 1) == 1:
            # scenarios in dictionary
            for name in cases.keys():
                if self.in_iterable_re(name, black_tests):
                    cases.pop(name)
        else:
            # workloads in subtasks
            for sind, subtask in enumerate(cases.get('subtasks', [])):
                idx = []
                for wind, workload in enumerate(subtask.get('workloads', [])):
                    scenario = workload.get('scenario', {})
                    for name in scenario.keys():
                        if self.in_iterable_re(name, black_tests):
                            idx.append(wind)
                            break
                for wind in reversed(idx):
                    cases['subtasks'][sind]['workloads'].pop(wind)
            # scenarios in subtasks
            idx = []
            for sind, subtask in enumerate(cases.get('subtasks', [])):
                scenario = subtask.get('scenario', {})
                for name in scenario.keys():
                    if self.in_iterable_re(name, black_tests):
                        idx.append(sind)
                        break
            for sind in reversed(idx):
                cases['subtasks'].pop(sind)

        with open(result_file_name, 'w') as fname:
            template.dump(cases, fname)

    def prepare_task(self, test_name):
        """Prepare resources for test run."""
        inst_dir = getattr(config.CONF, 'dir_rally_inst')
        try:
            shutil.rmtree(os.path.join(inst_dir, 'plugins'))
            shutil.rmtree(os.path.join(inst_dir, 'extra'))
        except Exception:  # pylint: disable=broad-except
            pass
        jobs_dir = os.path.join(
            getattr(config.CONF, 'dir_rally_data'), test_name, 'rally-jobs')
        shutil.copytree(os.path.join(jobs_dir, 'plugins'),
                        os.path.join(inst_dir, 'plugins'))
        shutil.copytree(os.path.join(jobs_dir, 'extra'),
                        os.path.join(inst_dir, 'extra'))

        task_name = self.task_yaml.get(test_name).get("task")
        task = os.path.join(jobs_dir, task_name)
        if not os.path.exists(task):
            raise Exception("The scenario '%s' does not exist." % task)
        LOGGER.debug('Scenario fetched from : %s', task)

        if not os.path.exists(self.TEMP_DIR):
            os.makedirs(self.TEMP_DIR)
        task_file_name = os.path.join(self.TEMP_DIR, task_name)
        self.apply_blacklist(task, task_file_name)
        self.run_cmd = (["rally", "task", "start", "--task", task_file_name])
        return True
