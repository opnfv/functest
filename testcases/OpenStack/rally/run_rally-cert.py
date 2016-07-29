#!/usr/bin/env python
#
# Copyright (c) 2015 Orange
# guyrodrigue.koffi@orange.com
# morgan.richomme@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
# 0.1 (05/2015) initial commit
# 0.2 (28/09/2015) extract Tempest, format json result, add ceilometer suite
# 0.3 (19/10/2015) remove Tempest from run_rally
# and push result into test DB
#
""" tests configuration """

import argparse
import json
import os
import re
import subprocess
import time
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils
import functest.utils.openstack_utils as os_utils
import iniparse
import yaml


tests = ['authenticate', 'glance', 'cinder', 'heat', 'keystone',
         'neutron', 'nova', 'quotas', 'requests', 'vm', 'all']
parser = argparse.ArgumentParser()
parser.add_argument("test_name",
                    help="Module name to be tested. "
                         "Possible values are : "
                         "[ {d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} | "
                         "{d[5]} | {d[6]} | {d[7]} | {d[8]} | {d[9]} | "
                         "{d[10]} ] "
                         "The 'all' value "
                         "performs all possible test scenarios"
                         .format(d=tests))

parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
parser.add_argument("-s", "--smoke",
                    help="Smoke test mode",
                    action="store_true")
parser.add_argument("-v", "--verbose",
                    help="Print verbose info about the progress",
                    action="store_true")
parser.add_argument("-n", "--noclean",
                    help="Don't clean the created resources for this test.",
                    action="store_true")
parser.add_argument("-z", "--sanity",
                    help="Sanity test mode, execute only a subset of tests",
                    action="store_true")

args = parser.parse_args()

network_dict = {}

if args.verbose:
    RALLY_STDERR = subprocess.STDOUT
else:
    RALLY_STDERR = open(os.devnull, 'w')

""" logging configuration """
logger = ft_logger.Logger("run_rally").getLogger()

REPO_PATH = os.environ['repos_dir'] + '/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)


with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)
f.close()

HOME = os.environ['HOME'] + "/"
RALLY_DIR = REPO_PATH + functest_yaml.get("general").get(
    "directories").get("dir_rally")
TEMPLATE_DIR = RALLY_DIR + "scenario/templates"
SUPPORT_DIR = RALLY_DIR + "scenario/support"

FLAVOR_NAME = "m1.tiny"
USERS_AMOUNT = 2
TENANTS_AMOUNT = 3
ITERATIONS_AMOUNT = 10
CONCURRENCY = 4

RESULTS_DIR = functest_yaml.get("general").get("directories").get(
    "dir_rally_res")
TEMPEST_CONF_FILE = functest_yaml.get("general").get("directories").get(
    "dir_results") + '/tempest/tempest.conf'
TEST_DB = functest_yaml.get("results").get("test_db_url")

PRIVATE_NET_NAME = functest_yaml.get("rally").get("network_name")
PRIVATE_SUBNET_NAME = functest_yaml.get("rally").get("subnet_name")
PRIVATE_SUBNET_CIDR = functest_yaml.get("rally").get("subnet_cidr")
ROUTER_NAME = functest_yaml.get("rally").get("router_name")

GLANCE_IMAGE_NAME = functest_yaml.get("general").get("openstack").get(
    "image_name")
GLANCE_IMAGE_FILENAME = functest_yaml.get("general").get("openstack").get(
    "image_file_name")
GLANCE_IMAGE_FORMAT = functest_yaml.get("general").get("openstack").get(
    "image_disk_format")
GLANCE_IMAGE_PATH = functest_yaml.get("general").get("directories").get(
    "dir_functest_data") + "/" + GLANCE_IMAGE_FILENAME

CINDER_VOLUME_TYPE_NAME = "volume_test"


SUMMARY = []
neutron_client = None


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


def live_migration_supported():
    config = iniparse.ConfigParser()
    if (config.read(TEMPEST_CONF_FILE) and
            config.has_section('compute-feature-enabled') and
            config.has_option('compute-feature-enabled', 'live_migration')):
        return config.getboolean('compute-feature-enabled', 'live_migration')

    return False


def build_task_args(test_file_name):
    task_args = {'service_list': [test_file_name]}
    task_args['image_name'] = GLANCE_IMAGE_NAME
    task_args['flavor_name'] = FLAVOR_NAME
    task_args['glance_image_location'] = GLANCE_IMAGE_PATH
    task_args['tmpl_dir'] = TEMPLATE_DIR
    task_args['sup_dir'] = SUPPORT_DIR
    task_args['users_amount'] = USERS_AMOUNT
    task_args['tenants_amount'] = TENANTS_AMOUNT
    task_args['use_existing_users'] = False
    task_args['iterations'] = ITERATIONS_AMOUNT
    task_args['concurrency'] = CONCURRENCY

    if args.sanity:
        task_args['full_mode'] = False
        task_args['smoke'] = True
    else:
        task_args['full_mode'] = True
        task_args['smoke'] = args.smoke

    ext_net = os_utils.get_external_net(neutron_client)
    if ext_net:
        task_args['floating_network'] = str(ext_net)
    else:
        task_args['floating_network'] = ''

    net_id = network_dict['net_id']
    task_args['netid'] = str(net_id)
    task_args['live_migration'] = live_migration_supported()

    auth_url = os.getenv('OS_AUTH_URL')
    if auth_url is not None:
        task_args['request_url'] = auth_url.rsplit(":", 1)[0]
    else:
        task_args['request_url'] = ''

    return task_args


def get_output(proc, test_name):
    global SUMMARY
    result = ""
    nb_tests = 0
    overall_duration = 0.0
    success = 0.0
    nb_totals = 0

    while proc.poll() is None:
        line = proc.stdout.readline()
        if args.verbose:
            result += line
        else:
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
                logger.info('Percentage error: %s, %s' % (percentage, line))
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
    SUMMARY.append(scenario_summary)

    logger.debug("\n" + result)

    return result


def get_cmd_output(proc):
    result = ""

    while proc.poll() is None:
        line = proc.stdout.readline()
        result += line

    return result


def run_task(test_name):
    #
    # the "main" function of the script who launch rally for a task
    # :param test_name: name for the rally test
    # :return: void
    #
    global SUMMARY
    logger.info('Starting test scenario "{}" ...'.format(test_name))
    start_time = time.time()

    task_file = '{}task.yaml'.format(RALLY_DIR)
    if not os.path.exists(task_file):
        logger.error("Task file '%s' does not exist." % task_file)
        exit(-1)

    test_file_name = '{}opnfv-{}.yaml'.format(RALLY_DIR + "scenario/",
                                              test_name)
    if not os.path.exists(test_file_name):
        logger.error("The scenario '%s' does not exist." % test_file_name)
        exit(-1)

    logger.debug('Scenario fetched from : {}'.format(test_file_name))

    cmd_line = ("rally task start --abort-on-sla-failure " +
                "--task {} ".format(task_file) +
                "--task-args \"{}\" ".format(build_task_args(test_name)))
    logger.debug('running command line : {}'.format(cmd_line))

    p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE,
                         stderr=RALLY_STDERR, shell=True)
    output = get_output(p, test_name)
    task_id = get_task_id(output)
    logger.debug('task_id : {}'.format(task_id))

    if task_id is None:
        logger.error('Failed to retrieve task_id, validating task...')
        cmd_line = ("rally task validate " +
                    "--task {} ".format(task_file) +
                    "--task-args \"{}\" ".format(build_task_args(test_name)))
        logger.debug('running command line : {}'.format(cmd_line))
        p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        output = get_cmd_output(p)
        logger.error("Task validation result:" + "\n" + output)
        return

    # check for result directory and create it otherwise
    if not os.path.exists(RESULTS_DIR):
        logger.debug('%s does not exist, we create it.'.format(RESULTS_DIR))
        os.makedirs(RESULTS_DIR)

    # write html report file
    report_file_name = '{}opnfv-{}.html'.format(RESULTS_DIR, test_name)
    cmd_line = "rally task report {} --out {}".format(task_id,
                                                      report_file_name)

    logger.debug('running command line : {}'.format(cmd_line))
    os.popen(cmd_line)

    # get and save rally operation JSON result
    cmd_line = "rally task results %s" % task_id
    logger.debug('running command line : {}'.format(cmd_line))
    cmd = os.popen(cmd_line)
    json_results = cmd.read()
    with open('{}opnfv-{}.json'.format(RESULTS_DIR, test_name), 'w') as f:
        logger.debug('saving json file')
        f.write(json_results)

    with open('{}opnfv-{}.json'
              .format(RESULTS_DIR, test_name)) as json_file:
        json_data = json.load(json_file)

    """ parse JSON operation result """
    status = "FAIL"
    if task_succeed(json_results):
        logger.info('Test scenario: "{}" OK.'.format(test_name) + "\n")
        status = "PASS"
    else:
        logger.info('Test scenario: "{}" Failed.'.format(test_name) + "\n")

    # Push results in payload of testcase
    if args.report:
        stop_time = time.time()
        logger.debug("Push Rally detailed results into DB")
        functest_utils.push_results_to_db("functest",
                                          "Rally_details",
                                          logger,
                                          start_time,
                                          stop_time,
                                          status,
                                          json_data)


def main():
    global SUMMARY
    global network_dict
    global neutron_client

    nova_client = os_utils.get_nova_client()
    neutron_client = os_utils.get_neutron_client()
    glance_client = os_utils.get_glance_client()
    cinder_client = os_utils.get_cinder_client()

    start_time = time.time()

    # configure script
    if not (args.test_name in tests):
        logger.error('argument not valid')
        exit(-1)

    SUMMARY = []

    volume_types = os_utils.list_volume_types(cinder_client,
                                              private=False)
    if not volume_types:
        volume_type = os_utils.create_volume_type(
            cinder_client, CINDER_VOLUME_TYPE_NAME)
        if not volume_type:
            logger.error("Failed to create volume type...")
            exit(-1)
        else:
            logger.debug("Volume type '%s' created succesfully..."
                         % CINDER_VOLUME_TYPE_NAME)
    else:
        logger.debug("Using existing volume type(s)...")

    image_id = os_utils.get_image_id(glance_client, GLANCE_IMAGE_NAME)
    image_exists = False

    if image_id == '':
        logger.debug("Creating image '%s' from '%s'..." % (GLANCE_IMAGE_NAME,
                                                           GLANCE_IMAGE_PATH))
        image_id = os_utils.create_glance_image(glance_client,
                                                GLANCE_IMAGE_NAME,
                                                GLANCE_IMAGE_PATH)
        if not image_id:
            logger.error("Failed to create the Glance image...")
            exit(-1)
        else:
            logger.debug("Image '%s' with ID '%s' created succesfully ."
                         % (GLANCE_IMAGE_NAME, image_id))
    else:
        logger.debug("Using existing image '%s' with ID '%s'..."
                     % (GLANCE_IMAGE_NAME, image_id))
        image_exists = True

    logger.debug("Creating network '%s'..." % PRIVATE_NET_NAME)
    network_dict = os_utils.create_network_full(neutron_client,
                                                PRIVATE_NET_NAME,
                                                PRIVATE_SUBNET_NAME,
                                                ROUTER_NAME,
                                                PRIVATE_SUBNET_CIDR)
    if not network_dict:
        logger.error("Failed to create network...")
        exit(-1)
    else:
        if not os_utils.update_neutron_net(neutron_client,
                                           network_dict['net_id'],
                                           shared=True):
            logger.error("Failed to update network...")
            exit(-1)
        else:
            logger.debug("Network '%s' available..." % PRIVATE_NET_NAME)

    if args.test_name == "all":
        for test_name in tests:
            if not (test_name == 'all' or
                    test_name == 'vm'):
                run_task(test_name)
    else:
        logger.debug("Test name: " + args.test_name)
        run_task(args.test_name)

    report = ("\n"
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
    stop_time = time.time()

    # for each scenario we draw a row for the table
    total_duration = 0.0
    total_nb_tests = 0
    total_success = 0.0
    for s in SUMMARY:
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

    total_duration_str = time.strftime("%H:%M:%S", time.gmtime(total_duration))
    total_duration_str2 = "{0:<10}".format(total_duration_str)
    total_nb_tests_str = "{0:<13}".format(total_nb_tests)
    success_rate = "{:0.2f}".format(total_success / len(SUMMARY))
    success_rate_str = "{0:<10}".format(str(success_rate) + '%')
    report += "+===================+============+===============+===========+"
    report += "\n"
    report += ("| TOTAL:            | " + total_duration_str2 + " | " +
               total_nb_tests_str + " | " + success_rate_str + "|\n")
    report += "+===================+============+===============+===========+"
    report += "\n"

    logger.info("\n" + report)
    payload.append({'summary': {'duration': total_duration,
                                'nb tests': total_nb_tests,
                                'nb success': success_rate}})

    if args.sanity:
        case_name = "rally_sanity"
    else:
        case_name = "rally_full"

    # Evaluation of the success criteria
    status = functest_utils.check_success_rate(case_name, success_rate)

    exit_code = -1
    if status == "PASS":
        exit_code = 0

    if args.report:
        logger.debug("Pushing Rally summary into DB...")
        functest_utils.push_results_to_db("functest",
                                          case_name,
                                          logger,
                                          start_time,
                                          stop_time,
                                          status,
                                          payload)
    if args.noclean:
        exit(exit_code)

    if not image_exists:
        logger.debug("Deleting image '%s' with ID '%s'..."
                     % (GLANCE_IMAGE_NAME, image_id))
        if not os_utils.delete_glance_image(nova_client, image_id):
            logger.error("Error deleting the glance image")

    if not volume_types:
        logger.debug("Deleting volume type '%s'..."
                     % CINDER_VOLUME_TYPE_NAME)
        if not os_utils.delete_volume_type(cinder_client, volume_type):
            logger.error("Error in deleting volume type...")

    exit(exit_code)


if __name__ == '__main__':
    main()
