#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

import json
import os
import re
import subprocess
import time

import iniparse
import yaml

from functest.core import testcase
from functest.utils.constants import CONST
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils

logger = ft_logger.Logger('Rally').getLogger()


class RallyBase(testcase.TestCase):
    TESTS = ['authenticate', 'glance', 'cinder', 'heat', 'keystone',
             'neutron', 'nova', 'quotas', 'requests', 'vm', 'all']
    GLANCE_IMAGE_NAME = CONST.openstack_image_name
    GLANCE_IMAGE_FILENAME = CONST.openstack_image_file_name
    GLANCE_IMAGE_PATH = os.path.join(CONST.dir_functest_data,
                                     GLANCE_IMAGE_FILENAME)
    GLANCE_IMAGE_FORMAT = CONST.openstack_image_disk_format
    FLAVOR_NAME = "m1.tiny"

    RALLY_DIR = os.path.join(CONST.dir_repo_functest, CONST.dir_rally)
    RALLY_SCENARIO_DIR = os.path.join(RALLY_DIR, "scenario")
    TEMPLATE_DIR = os.path.join(RALLY_SCENARIO_DIR, "templates")
    SUPPORT_DIR = os.path.join(RALLY_SCENARIO_DIR, "support")
    USERS_AMOUNT = 2
    TENANTS_AMOUNT = 3
    ITERATIONS_AMOUNT = 10
    CONCURRENCY = 4
    RESULTS_DIR = os.path.join(CONST.dir_results, 'rally')
    TEMPEST_CONF_FILE = os.path.join(CONST.dir_results,
                                     'tempest/tempest.conf')
    BLACKLIST_FILE = os.path.join(RALLY_DIR, "blacklist.txt")
    TEMP_DIR = os.path.join(RALLY_DIR, "var")

    CINDER_VOLUME_TYPE_NAME = "volume_test"
    RALLY_PRIVATE_NET_NAME = CONST.rally_network_name
    RALLY_PRIVATE_SUBNET_NAME = CONST.rally_subnet_name
    RALLY_PRIVATE_SUBNET_CIDR = CONST.rally_subnet_cidr
    RALLY_ROUTER_NAME = CONST.rally_router_name

    def __init__(self):
        super(RallyBase, self).__init__()
        self.case_name =''
        self.mode = ''
        self.summary = []
        self.scenario_dir = ''
        self.nova_client = os_utils.get_nova_client()
        self.neutron_client = os_utils.get_neutron_client()
        self.cinder_client = os_utils.get_cinder_client()
        self.network_dict = {}
        self.volume_type = None
        self.smoke = None

    def _build_task_args(self, test_file_name):
        task_args = {'service_list': [test_file_name]}
        task_args['image_name'] = self.GLANCE_IMAGE_NAME
        task_args['flavor_name'] = self.FLAVOR_NAME
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

        ext_net = os_utils.get_external_net(self.neutron_client)
        if ext_net:
            task_args['floating_network'] = str(ext_net)
        else:
            task_args['floating_network'] = ''

        net_id = self.network_dict['net_id']
        if net_id:
            task_args['netid'] = str(net_id)
        else:
            task_args['netid'] = ''

        # get keystone auth endpoint
        task_args['request_url'] = CONST.OS_AUTH_URL or ''

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

        logger.debug('Scenario fetched from : {}'.format(scenario_file_name))
        test_file_name = os.path.join(self.TEMP_DIR, test_yaml_file_name)

        if not os.path.exists(self.TEMP_DIR):
            os.makedirs(self.TEMP_DIR)

        self.apply_blacklist(scenario_file_name, test_file_name)
        return test_file_name

    @staticmethod
    def get_task_id(cmd_raw):
        """
        get task id from command rally result
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
        Parse JSON from rally JSON results
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

    @staticmethod
    def live_migration_supported():
        config = iniparse.ConfigParser()
        if (config.read(RallyBase.TEMPEST_CONF_FILE) and
                config.has_section('compute-feature-enabled') and
                config.has_option('compute-feature-enabled',
                                  'live_migration')):
            return config.getboolean('compute-feature-enabled',
                                     'live_migration')

        return False

    @staticmethod
    def get_cmd_output(proc):
        result = ""
        while proc.poll() is None:
            line = proc.stdout.readline()
            result += line
        return result

    @staticmethod
    def excl_scenario():
        black_tests = []
        try:
            with open(RallyBase.BLACKLIST_FILE, 'r') as black_list_file:
                black_list_yaml = yaml.safe_load(black_list_file)

            installer_type = CONST.INSTALLER_TYPE
            deploy_scenario = CONST.DEPLOY_SCENARIO
            if (bool(installer_type) * bool(deploy_scenario)):
                if 'scenario' in black_list_yaml.keys():
                    for item in black_list_yaml['scenario']:
                        scenarios = item['scenarios']
                        installers = item['installers']
                        if (deploy_scenario in scenarios and
                                installer_type in installers):
                            tests = item['tests']
                            black_tests.extend(tests)
        except Exception:
            logger.debug("Scenario exclusion not applied.")

        return black_tests

    @staticmethod
    def excl_func():
        black_tests = []
        func_list = []

        try:
            with open(RallyBase.BLACKLIST_FILE, 'r') as black_list_file:
                black_list_yaml = yaml.safe_load(black_list_file)

            if not RallyBase.live_migration_supported():
                func_list.append("no_live_migration")

            if 'functionality' in black_list_yaml.keys():
                for item in black_list_yaml['functionality']:
                    functions = item['functions']
                    for func in func_list:
                        if func in functions:
                            tests = item['tests']
                            black_tests.extend(tests)
        except Exception:
            logger.debug("Functionality exclusion not applied.")

        return black_tests

    @staticmethod
    def apply_blacklist(case_file_name, result_file_name):
        logger.debug("Applying blacklist...")
        cases_file = open(case_file_name, 'r')
        result_file = open(result_file_name, 'w')

        black_tests = list(set(RallyBase.excl_func() +
                           RallyBase.excl_scenario()))

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
        try:
            if os.stat(file_name).st_size > 0:
                return False
        except:
            pass

        return True

    def _run_task(self, test_name):
        logger.info('Starting test scenario "{}" ...'.format(test_name))

        task_file = os.path.join(self.RALLY_DIR, 'task.yaml')
        if not os.path.exists(task_file):
            logger.error("Task file '%s' does not exist." % task_file)
            raise Exception("Task file '%s' does not exist." % task_file)

        file_name = self._prepare_test_list(test_name)
        if self.file_is_empty(file_name):
            logger.info('No tests for scenario "{}"'.format(test_name))
            return

        cmd_line = ("rally task start --abort-on-sla-failure "
                    "--task {0} "
                    "--task-args \"{1}\""
                    .format(task_file, self._build_task_args(test_name)))
        logger.debug('running command line: {}'.format(cmd_line))

        p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        output = self._get_output(p, test_name)
        task_id = self.get_task_id(output)
        logger.debug('task_id : {}'.format(task_id))

        if task_id is None:
            logger.error('Failed to retrieve task_id, validating task...')
            cmd_line = ("rally task validate "
                        "--task {0} "
                        "--task-args \"{1}\""
                        .format(task_file, self._build_task_args(test_name)))
            logger.debug('running command line: {}'.format(cmd_line))
            p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, shell=True)
            output = self.get_cmd_output(p)
            logger.error("Task validation result:" + "\n" + output)
            return

        # check for result directory and create it otherwise
        if not os.path.exists(self.RESULTS_DIR):
            logger.debug('{} does not exist, we create it.'
                         .format(self.RESULTS_DIR))
            os.makedirs(self.RESULTS_DIR)

        # write html report file
        report_html_name = 'opnfv-{}.html'.format(test_name)
        report_html_dir = os.path.join(self.RESULTS_DIR, report_html_name)
        cmd_line = "rally task report {} --out {}".format(task_id,
                                                          report_html_dir)

        logger.debug('running command line: {}'.format(cmd_line))
        os.popen(cmd_line)

        # get and save rally operation JSON result
        cmd_line = "rally task results %s" % task_id
        logger.debug('running command line: {}'.format(cmd_line))
        cmd = os.popen(cmd_line)
        json_results = cmd.read()
        report_json_name = 'opnfv-{}.json'.format(test_name)
        report_json_dir = os.path.join(self.RESULTS_DIR, report_json_name)
        with open(report_json_dir, 'w') as f:
            logger.debug('saving json file')
            f.write(json_results)

        """ parse JSON operation result """
        if self.task_succeed(json_results):
            logger.info('Test scenario: "{}" OK.'.format(test_name) + "\n")
        else:
            logger.info('Test scenario: "{}" Failed.'.format(test_name) + "\n")

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
                    logger.info('Percentage error: %s, %s' %
                                (percentage, line))
                nb_totals += 1
            elif "Full duration" in line:
                duration = line.split(': ')[1]
                try:
                    overall_duration += float(duration)
                except ValueError:
                    logger.info('Duration error: %s, %s' % (duration, line))

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

        logger.debug("\n" + result)

        return result

    def _prepare_env(self):
        logger.debug('Validating the test name...')
        if not (self.test_name in self.TESTS):
            raise Exception("Test name '%s' is invalid" % self.test_name)

        volume_types = os_utils.list_volume_types(self.cinder_client,
                                                  private=False)
        if volume_types:
            logger.debug("Using existing volume type(s)...")
        else:
            logger.debug('Creating volume type...')
            self.volume_type = os_utils.create_volume_type(
                self.cinder_client, self.CINDER_VOLUME_TYPE_NAME)
            if self.volume_type is None:
                raise Exception("Failed to create volume type '%s'" %
                                self.CINDER_VOLUME_TYPE_NAME)
            logger.debug("Volume type '%s' is created succesfully." %
                         self.CINDER_VOLUME_TYPE_NAME)

        logger.debug('Getting or creating image...')
        self.image_exists, self.image_id = os_utils.get_or_create_image(
            self.GLANCE_IMAGE_NAME,
            self.GLANCE_IMAGE_PATH,
            self.GLANCE_IMAGE_FORMAT)
        if self.image_id is None:
            raise Exception("Failed to get or create image '%s'" %
                            self.GLANCE_IMAGE_NAME)

        logger.debug("Creating network '%s'..." % self.RALLY_PRIVATE_NET_NAME)
        self.network_dict = os_utils.create_shared_network_full(
            self.RALLY_PRIVATE_NET_NAME,
            self.RALLY_PRIVATE_SUBNET_NAME,
            self.RALLY_ROUTER_NAME,
            self.RALLY_PRIVATE_SUBNET_CIDR)
        if self.network_dict is None:
            raise Exception("Failed to create shared network '%s'" %
                            self.RALLY_PRIVATE_NET_NAME)

    def _run_tests(self):
        if self.test_name == 'all':
            for test in self.TESTS:
                if (test == 'all' or test == 'vm'):
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
        for s in self.summary:
            name = "{0:<17}".format(s['test_name'])
            duration = float(s['overall_duration'])
            total_duration += duration
            duration = time.strftime("%M:%S", time.gmtime(duration))
            duration = "{0:<10}".format(duration)
            nb_tests = "{0:<13}".format(s['nb_tests'])
            total_nb_tests += int(s['nb_tests'])
            success = "{0:<10}".format(str(s['success']) + '%')
            total_success += float(s['success'])
            report += ("" +
                       "| " + name + " | " + duration + " | " +
                       nb_tests + " | " + success + "|\n" +
                       "+-------------------+------------"
                       "+---------------+-----------+\n")
            payload.append({'module': name,
                            'details': {'duration': s['overall_duration'],
                                        'nb tests': s['nb_tests'],
                                        'success': s['success']}})

        total_duration_str = time.strftime("%H:%M:%S",
                                           time.gmtime(total_duration))
        total_duration_str2 = "{0:<10}".format(total_duration_str)
        total_nb_tests_str = "{0:<13}".format(total_nb_tests)

        if len(self.summary):
            success_rate = total_success / len(self.summary)
        else:
            success_rate = 100
        success_rate = "{:0.2f}".format(success_rate)
        success_rate_str = "{0:<10}".format(str(success_rate) + '%')
        report += ("+===================+============"
                   "+===============+===========+")
        report += "\n"
        report += ("| TOTAL:            | " + total_duration_str2 + " | " +
                   total_nb_tests_str + " | " + success_rate_str + "|\n")
        report += ("+===================+============"
                   "+===============+===========+")
        report += "\n"

        logger.info("\n" + report)
        payload.append({'summary': {'duration': total_duration,
                                    'nb tests': total_nb_tests,
                                    'nb success': success_rate}})

        self.criteria = ft_utils.check_success_rate(
            self.case_name, success_rate)
        self.details = payload

        logger.info("Rally '%s' success_rate is %s%%, is marked as %s"
                    % (self.case_name, success_rate, self.criteria))

    def _clean_up(self):
        if self.volume_type:
            logger.debug("Deleting volume type '%s'..." % self.volume_type)
            os_utils.delete_volume_type(self.cinder_client, self.volume_type)

        if not self.image_exists:
            logger.debug("Deleting image '%s' with ID '%s'..."
                         % (self.GLANCE_IMAGE_NAME, self.image_id))
            if not os_utils.delete_glance_image(self.nova_client,
                                                self.image_id):
                logger.error("Error deleting the glance image")

    def run(self):
        self.start_time = time.time()
        try:
            self._prepare_env()
            self._run_tests()
            self._generate_report()
            self._clean_up()
            res = testcase.TestCase.EX_OK
        except Exception as e:
            logger.error('Error with run: %s' % e)
            res = testcase.TestCase.EX_RUN_ERROR

        self.stop_time = time.time()
        return res


class RallySanity(RallyBase):
    def __init__(self):
        super(RallySanity, self).__init__()
        self.case_name = 'rally_sanity'
        self.mode = 'sanity'
        self.test_name = 'all'
        self.smoke = True
        self.scenario_dir = os.path.join(self.RALLY_SCENARIO_DIR, 'sanity')


class RallyFull(RallyBase):
    def __init__(self):
        super(RallyFull, self).__init__()
        self.case_name = 'rally_full'
        self.mode = 'full'
        self.test_name = 'all'
        self.smoke = False
        self.scenario_dir = os.path.join(self.RALLY_SCENARIO_DIR, 'full')
