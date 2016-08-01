#!/usr/bin/env python
#
# Description:
#    Runs tempest and pushes the results to the DB
#
# Authors:
#    morgan.richomme@orange.com
#    jose.lausuch@ericsson.com
#    viktor.tikkanen@nokia.com
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import ConfigParser
import argparse
import os
import re
import shutil
import subprocess
import sys
import time

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
import yaml


modes = ['full', 'smoke', 'baremetal', 'compute', 'data_processing',
         'identity', 'image', 'network', 'object_storage', 'orchestration',
         'telemetry', 'volume', 'custom', 'defcore', 'feature_multisite']

""" tests configuration """
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug",
                    help="Debug mode",
                    action="store_true")
parser.add_argument("-s", "--serial",
                    help="Run tests in one thread",
                    action="store_true")
parser.add_argument("-m", "--mode",
                    help="Tempest test mode [smoke, all]",
                    default="smoke")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
parser.add_argument("-n", "--noclean",
                    help="Don't clean the created resources for this test.",
                    action="store_true")

args = parser.parse_args()

""" logging configuration """
logger = ft_logger.Logger("run_tempest").getLogger()

REPO_PATH = os.environ['repos_dir'] + '/functest/'

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)
f.close()
TEST_DB = functest_yaml.get("results").get("test_db_url")

MODE = "smoke"
GLANCE_IMAGE_NAME = functest_yaml.get("general").get(
    "openstack").get("image_name")
GLANCE_IMAGE_FILENAME = functest_yaml.get("general").get(
    "openstack").get("image_file_name")
GLANCE_IMAGE_FORMAT = functest_yaml.get("general").get(
    "openstack").get("image_disk_format")
GLANCE_IMAGE_PATH = functest_yaml.get("general").get("directories").get(
    "dir_functest_data") + "/" + GLANCE_IMAGE_FILENAME
PRIVATE_NET_NAME = functest_yaml.get("tempest").get("private_net_name")
PRIVATE_SUBNET_NAME = functest_yaml.get("tempest").get("private_subnet_name")
PRIVATE_SUBNET_CIDR = functest_yaml.get("tempest").get("private_subnet_cidr")
ROUTER_NAME = functest_yaml.get("tempest").get("router_name")
TENANT_NAME = functest_yaml.get("tempest").get("identity").get("tenant_name")
TENANT_DESCRIPTION = functest_yaml.get("tempest").get("identity").get(
    "tenant_description")
USER_NAME = functest_yaml.get("tempest").get("identity").get("user_name")
USER_PASSWORD = functest_yaml.get("tempest").get("identity").get(
    "user_password")
DEPLOYMENT_MAME = functest_yaml.get("rally").get("deployment_name")
RALLY_INSTALLATION_DIR = functest_yaml.get("general").get("directories").get(
    "dir_rally_inst")
RESULTS_DIR = functest_yaml.get("general").get("directories").get(
    "dir_results")
TEMPEST_RESULTS_DIR = RESULTS_DIR + '/tempest'
TEST_LIST_DIR = functest_yaml.get("general").get("directories").get(
    "dir_tempest_cases")
TEMPEST_CUSTOM = REPO_PATH + TEST_LIST_DIR + 'test_list.txt'
TEMPEST_BLACKLIST = REPO_PATH + TEST_LIST_DIR + 'blacklist.txt'
TEMPEST_DEFCORE = REPO_PATH + TEST_LIST_DIR + 'defcore_req.txt'
TEMPEST_RAW_LIST = TEMPEST_RESULTS_DIR + '/test_raw_list.txt'
TEMPEST_LIST = TEMPEST_RESULTS_DIR + '/test_list.txt'


def get_info(file_result):
    test_run = ""
    duration = ""
    test_failed = ""

    p = subprocess.Popen('cat tempest.log',
                         shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        # print line,
        if (len(test_run) < 1):
            test_run = re.findall("[0-9]*\.[0-9]*s", line)
        if (len(duration) < 1):
            duration = re.findall("[0-9]*\ tests", line)
        regexp = r"(failures=[0-9]+)"
        if (len(test_failed) < 1):
            test_failed = re.findall(regexp, line)

    logger.debug("test_run:" + test_run)
    logger.debug("duration:" + duration)


def create_tempest_resources():
    keystone_client = os_utils.get_keystone_client()
    neutron_client = os_utils.get_neutron_client()
    glance_client = os_utils.get_glance_client()

    logger.debug("Creating tenant and user for Tempest suite")
    tenant_id = os_utils.create_tenant(keystone_client,
                                       TENANT_NAME,
                                       TENANT_DESCRIPTION)
    if tenant_id == '':
        logger.error("Error : Failed to create %s tenant" % TENANT_NAME)

    user_id = os_utils.create_user(keystone_client, USER_NAME, USER_PASSWORD,
                                   None, tenant_id)
    if user_id == '':
        logger.error("Error : Failed to create %s user" % USER_NAME)

    logger.debug("Creating private network for Tempest suite")
    network_dic = os_utils.create_network_full(neutron_client,
                                               PRIVATE_NET_NAME,
                                               PRIVATE_SUBNET_NAME,
                                               ROUTER_NAME,
                                               PRIVATE_SUBNET_CIDR)
    if network_dic:
        if not os_utils.update_neutron_net(neutron_client,
                                           network_dic['net_id'],
                                           shared=True):
            logger.error("Failed to update private network...")
            exit(-1)
        else:
            logger.debug("Network '%s' is available..." % PRIVATE_NET_NAME)
    else:
        logger.error("Private network creation failed")
        exit(-1)

    logger.debug("Creating image for Tempest suite")
    # Check if the given image exists
    image_id = os_utils.get_image_id(glance_client, GLANCE_IMAGE_NAME)
    if image_id != '':
        logger.info("Using existing image '%s'..." % GLANCE_IMAGE_NAME)
    else:
        logger.info("Creating image '%s' from '%s'..." % (GLANCE_IMAGE_NAME,
                                                          GLANCE_IMAGE_PATH))
        image_id = os_utils.create_glance_image(glance_client,
                                                GLANCE_IMAGE_NAME,
                                                GLANCE_IMAGE_PATH)
        if not image_id:
            logger.error("Failed to create a Glance image...")
            exit(-1)
        logger.debug("Image '%s' with ID=%s created successfully."
                     % (GLANCE_IMAGE_NAME, image_id))


def configure_tempest(deployment_dir):
    """
    Add/update needed parameters into tempest.conf file generated by Rally
    """

    logger.debug("Generating tempest.conf file...")
    cmd = "rally verify genconfig"
    ft_utils.execute_command(cmd, logger)

    logger.debug("Finding tempest.conf file...")
    tempest_conf_file = deployment_dir + "/tempest.conf"
    if not os.path.isfile(tempest_conf_file):
        logger.error("Tempest configuration file %s NOT found."
                     % tempest_conf_file)
        exit(-1)

    logger.debug("Updating selected tempest.conf parameters...")
    config = ConfigParser.RawConfigParser()
    config.read(tempest_conf_file)
    config.set('compute', 'fixed_network_name', PRIVATE_NET_NAME)
    config.set('identity', 'tenant_name', TENANT_NAME)
    config.set('identity', 'username', USER_NAME)
    config.set('identity', 'password', USER_PASSWORD)

    if os.getenv('OS_ENDPOINT_TYPE') is not None:
        services_list = ['compute', 'volume', 'image', 'network',
                         'data-processing', 'object-storage', 'orchestration']
        sections = config.sections()
        for service in services_list:
            if service not in sections:
                config.add_section(service)
            config.set(service, 'endpoint_type',
                       os.environ.get("OS_ENDPOINT_TYPE"))

    with open(tempest_conf_file, 'wb') as config_file:
        config.write(config_file)

    # Copy tempest.conf to /home/opnfv/functest/results/tempest/
    shutil.copyfile(tempest_conf_file, TEMPEST_RESULTS_DIR + '/tempest.conf')
    return True


def configure_tempest_feature(deployment_dir, mode):
    """
    Add/update needed parameters into tempest.conf file generated by Rally
    """

    logger.debug("Finding tempest.conf file...")
    tempest_conf_file = deployment_dir + "/tempest.conf"
    if not os.path.isfile(tempest_conf_file):
        logger.error("Tempest configuration file %s NOT found."
                     % tempest_conf_file)
        exit(-1)

    logger.debug("Updating selected tempest.conf parameters...")
    config = ConfigParser.RawConfigParser()
    config.read(tempest_conf_file)
    if mode == 'feature_multisite':
        config.set('service_available', 'kingbird', 'true')
        cmd = "openstack endpoint show kingbird | grep publicurl |\
               awk '{print $4}' | awk -F '/' '{print $4}'"
        kingbird_api_version = os.popen(cmd).read()
        if os.environ.get("INSTALLER_TYPE") == 'fuel':
            # For MOS based setup, the service is accessible
            # via bind host
            kingbird_conf_path = "/etc/kingbird/kingbird.conf"
            installer_type = os.getenv('INSTALLER_TYPE', 'Unknown')
            installer_ip = os.getenv('INSTALLER_IP', 'Unknown')
            installer_username = ft_utils.get_parameter_from_yaml(
                "multisite." + installer_type +
                "_environment.installer_username")
            installer_password = ft_utils.get_parameter_from_yaml(
                "multisite." + installer_type +
                "_environment.installer_password")

            ssh_options = "-o UserKnownHostsFile=/dev/null -o \
                StrictHostKeyChecking=no"

            # Get the controller IP from the fuel node
            cmd = 'sshpass -p %s ssh 2>/dev/null %s %s@%s \
                    \'fuel node --env 1| grep controller | grep "True\|  1" \
                    | awk -F\| "{print \$5}"\'' % (installer_password,
                                                   ssh_options,
                                                   installer_username,
                                                   installer_ip)
            multisite_controller_ip = \
                "".join(os.popen(cmd).read().split())

            # Login to controller and get bind host details
            cmd = 'sshpass -p %s ssh 2>/dev/null  %s %s@%s "ssh %s \\" \
                grep -e "^bind_" %s  \\""' % (installer_password,
                                              ssh_options,
                                              installer_username,
                                              installer_ip,
                                              multisite_controller_ip,
                                              kingbird_conf_path)
            bind_details = os.popen(cmd).read()
            bind_details = "".join(bind_details.split())
            # Extract port number from the bind details
            bind_port = re.findall(r"\D(\d{4})", bind_details)[0]
            # Extract ip address from the bind details
            bind_host = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
                                   bind_details)[0]
            kingbird_endpoint_url = "http://" + bind_host + ":" + bind_port + \
                                    "/"
        else:
            cmd = "openstack endpoint show kingbird | grep publicurl |\
                   awk '{print $4}' | awk -F '/' '{print $3}'"
            kingbird_endpoint_url = os.popen(cmd).read()

        try:
            config.add_section("kingbird")
        except Exception:
            logger.info('kingbird section exist')
        config.set('kingbird', 'endpoint_type', 'publicURL')
        config.set('kingbird', 'TIME_TO_SYNC', '20')
        config.set('kingbird', 'endpoint_url', kingbird_endpoint_url)
        config.set('kingbird', 'api_version', kingbird_api_version)
    with open(tempest_conf_file, 'wb') as config_file:
        config.write(config_file)

    # Copy tempest.conf to /home/opnfv/functest/results/tempest/
    shutil.copyfile(tempest_conf_file, TEMPEST_RESULTS_DIR + '/tempest.conf')
    return True


def read_file(filename):
    with open(filename) as src:
        return [line.strip() for line in src.readlines()]


def generate_test_list(deployment_dir, mode):
    logger.debug("Generating test case list...")
    if mode == 'defcore':
        shutil.copyfile(TEMPEST_DEFCORE, TEMPEST_RAW_LIST)
    elif mode == 'custom':
        if os.path.isfile(TEMPEST_CUSTOM):
            shutil.copyfile(TEMPEST_CUSTOM, TEMPEST_RAW_LIST)
        else:
            logger.error("Tempest test list file %s NOT found."
                         % TEMPEST_CUSTOM)
            exit(-1)
    else:
        if mode == 'smoke':
            testr_mode = "smoke"
        elif mode == 'feature_multisite':
            testr_mode = " | grep -i kingbird "
        elif mode == 'full':
            testr_mode = ""
        else:
            testr_mode = 'tempest.api.' + mode
        cmd = ("cd " + deployment_dir + ";" + "testr list-tests " +
               testr_mode + ">" + TEMPEST_RAW_LIST + ";cd")
        ft_utils.execute_command(cmd, logger)


def apply_tempest_blacklist():
    logger.debug("Applying tempest blacklist...")
    cases_file = read_file(TEMPEST_RAW_LIST)
    result_file = open(TEMPEST_LIST, 'w')
    black_tests = []
    try:
        installer_type = os.getenv('INSTALLER_TYPE')
        deploy_scenario = os.getenv('DEPLOY_SCENARIO')
        if (bool(installer_type) * bool(deploy_scenario)):
            # if INSTALLER_TYPE and DEPLOY_SCENARIO are set we read the file
            black_list_file = open(TEMPEST_BLACKLIST)
            black_list_yaml = yaml.safe_load(black_list_file)
            black_list_file.close()
            for item in black_list_yaml:
                scenarios = item['scenarios']
                installers = item['installers']
                if (deploy_scenario in scenarios and
                        installer_type in installers):
                    tests = item['tests']
                    for test in tests:
                        black_tests.append(test)
                    break
    except:
        black_tests = []
        logger.debug("Tempest blacklist file does not exist.")

    for line in cases_file:
        if line not in black_tests:
            result_file.write(str(line) + '\n')
    result_file.close()


def run_tempest(OPTION):
    #
    # the "main" function of the script which launches Rally to run Tempest
    # :param option: tempest option (smoke, ..)
    # :return: void
    #
    logger.info("Starting Tempest test suite: '%s'." % OPTION)
    start_time = time.time()
    stop_time = start_time
    cmd_line = "rally verify start " + OPTION + " --system-wide"

    header = ("Tempest environment:\n"
              "  Installer: %s\n  Scenario: %s\n  Node: %s\n  Date: %s\n" %
              (os.getenv('INSTALLER_TYPE', 'Unknown'),
               os.getenv('DEPLOY_SCENARIO', 'Unknown'),
               os.getenv('NODE_NAME', 'Unknown'),
               time.strftime("%a %b %d %H:%M:%S %Z %Y")))

    f_stdout = open(TEMPEST_RESULTS_DIR + "/tempest.log", 'w+')
    f_stderr = open(TEMPEST_RESULTS_DIR + "/tempest-error.log", 'w+')
    f_env = open(TEMPEST_RESULTS_DIR + "/environment.log", 'w+')
    f_env.write(header)

    # subprocess.call(cmd_line, shell=True, stdout=f_stdout, stderr=f_stderr)
    p = subprocess.Popen(
        cmd_line, shell=True,
        stdout=subprocess.PIPE,
        stderr=f_stderr,
        bufsize=1)

    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            if re.search("\} tempest\.", line):
                logger.info(line.replace('\n', ''))
            f_stdout.write(line)
    p.wait()

    f_stdout.close()
    f_stderr.close()
    f_env.close()

    cmd_line = "rally verify show"
    output = ""
    p = subprocess.Popen(
        cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.stdout:
        if re.search("Tests\:", line):
            break
        output += line
    logger.info(output)

    cmd_line = "rally verify list"
    cmd = os.popen(cmd_line)
    output = (((cmd.read()).splitlines()[-2]).replace(" ", "")).split("|")
    # Format:
    # | UUID | Deployment UUID | smoke | tests | failures | Created at |
    # Duration | Status  |
    num_tests = output[4]
    num_failures = output[5]
    time_start = output[6]
    duration = output[7]
    # Compute duration (lets assume it does not take more than 60 min)
    dur_min = int(duration.split(':')[1])
    dur_sec_float = float(duration.split(':')[2])
    dur_sec_int = int(round(dur_sec_float, 0))
    dur_sec_int = dur_sec_int + 60 * dur_min
    stop_time = time.time()

    status = "FAIL"
    try:
        diff = (int(num_tests) - int(num_failures))
        success_rate = 100 * diff / int(num_tests)
    except:
        success_rate = 0

    # For Tempest we assume that the success rate is above 90%
    if "smoke" in args.mode:
        case_name = "tempest_smoke_serial"
        # Note criteria hardcoded...TODO read it from testcases.yaml
        success_criteria = 100
        if success_rate >= success_criteria:
            status = "PASS"
        else:
            logger.info("Tempest success rate: %s%%. The success criteria to "
                        "pass this test is %s%%. Marking the test as FAILED." %
                        (success_rate, success_criteria))
    else:
        case_name = "tempest_full_parallel"
        # Note criteria hardcoded...TODO read it from testcases.yaml
        success_criteria = 80
        if success_rate >= success_criteria:
            status = "PASS"
        else:
            logger.info("Tempest success rate: %s%%. The success criteria to "
                        "pass this test is %s%%. Marking the test as FAILED." %
                        (success_rate, success_criteria))

    # Push results in payload of testcase
    if args.report:
        # add the test in error in the details sections
        # should be possible to do it during the test
        logger.debug("Pushing tempest results into DB...")
        with open(TEMPEST_RESULTS_DIR + "/tempest.log", 'r') as myfile:
            output = myfile.read()
        error_logs = ""

        for match in re.findall('(.*?)[. ]*FAILED', output):
            error_logs += match

        # Generate json results for DB
        json_results = {"timestart": time_start, "duration": dur_sec_int,
                        "tests": int(num_tests), "failures": int(num_failures),
                        "errors": error_logs}
        logger.info("Results: " + str(json_results))
        # split Tempest smoke and full

        try:
            ft_utils.push_results_to_db("functest",
                                        case_name,
                                        None,
                                        start_time,
                                        stop_time,
                                        status,
                                        json_results)
        except:
            logger.error("Error pushing results into Database '%s'"
                         % sys.exc_info()[0])

    if status == "PASS":
        return 0
    else:
        return -1


def main():
    global MODE

    if not (args.mode in modes):
        logger.error("Tempest mode not valid. "
                     "Possible values are:\n" + str(modes))
        exit(-1)

    if not os.path.exists(TEMPEST_RESULTS_DIR):
        os.makedirs(TEMPEST_RESULTS_DIR)

    deployment_dir = ft_utils.get_deployment_dir(logger)
    configure_tempest(deployment_dir)
    configure_tempest_feature(deployment_dir, args.mode)
    create_tempest_resources()
    generate_test_list(deployment_dir, args.mode)
    apply_tempest_blacklist()

    MODE = "--tests-file " + TEMPEST_LIST
    if args.serial:
        MODE += " --concur 1"

    ret_val = run_tempest(MODE)
    if ret_val != 0:
        sys.exit(-1)

    sys.exit(0)


if __name__ == '__main__':
    main()
