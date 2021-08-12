#!/usr/bin/env python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

"""Tempest testcases implementation."""

from __future__ import division

import json
import logging
import os
import re
import shutil
import subprocess
import time

import pkg_resources
from six.moves import configparser
from xtesting.core import testcase
import yaml

from functest.core import singlevm
from functest.opnfv_tests.openstack.rally import rally
from functest.utils import config
from functest.utils import env
from functest.utils import functest_utils

LOGGER = logging.getLogger(__name__)


class TempestCommon(singlevm.VmReady2):
    # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """TempestCommon testcases implementation class."""

    visibility = 'public'
    filename_alt = '/home/opnfv/functest/images/cirros-0.5.1-x86_64-disk.img'
    shared_network = True
    tempest_conf_yaml = pkg_resources.resource_filename(
        'functest',
        'opnfv_tests/openstack/tempest/custom_tests/tempest_conf.yaml')
    tempest_custom = pkg_resources.resource_filename(
        'functest',
        'opnfv_tests/openstack/tempest/custom_tests/test_list.txt')
    tempest_blacklist = pkg_resources.resource_filename(
        'functest',
        'opnfv_tests/openstack/tempest/custom_tests/blacklist.yaml')
    tempest_public_blacklist = pkg_resources.resource_filename(
        'functest',
        'opnfv_tests/openstack/tempest/custom_tests/public_blacklist.yaml')

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest'
        super().__init__(**kwargs)
        assert self.orig_cloud
        assert self.cloud
        assert self.project
        if self.orig_cloud.get_role("admin"):
            self.role_name = "admin"
        elif self.orig_cloud.get_role("Admin"):
            self.role_name = "Admin"
        else:
            raise Exception("Cannot detect neither admin nor Admin")
        self.orig_cloud.grant_role(
            self.role_name, user=self.project.user.id,
            project=self.project.project.id,
            domain=self.project.domain.id)
        self.orig_cloud.grant_role(
            self.role_name, user=self.project.user.id,
            domain=self.project.domain.id)
        self.deployment_id = None
        self.verifier_id = None
        self.verifier_repo_dir = None
        self.deployment_dir = None
        self.verification_id = None
        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), self.case_name)
        self.raw_list = os.path.join(self.res_dir, 'test_raw_list.txt')
        self.list = os.path.join(self.res_dir, 'test_list.txt')
        self.conf_file = None
        self.image_alt = None
        self.flavor_alt = None
        self.services = []
        try:
            self.services = kwargs['run']['args']['services']
        except Exception:  # pylint: disable=broad-except
            pass
        self.neutron_extensions = []
        try:
            self.neutron_extensions = kwargs['run']['args'][
                'neutron_extensions']
        except Exception:  # pylint: disable=broad-except
            pass
        self.deny_skipping = kwargs.get("deny_skipping", False)
        self.tests_count = kwargs.get("tests_count", 0)

    def check_services(self):
        """Check the mandatory services."""
        for service in self.services:
            try:
                self.cloud.search_services(service)[0]
            except Exception:  # pylint: disable=broad-except
                self.is_skipped = True
                break

    def check_extensions(self):
        """Check the mandatory network extensions."""
        extensions = self.cloud.get_network_extensions()
        for network_extension in self.neutron_extensions:
            if network_extension not in extensions:
                LOGGER.warning(
                    "Cannot find Neutron extension: %s", network_extension)
                self.is_skipped = True
                break

    def check_requirements(self):
        self.check_services()
        self.check_extensions()
        if self.is_skipped:
            self.project.clean()

    @staticmethod
    def read_file(filename):
        """Read file and return content as a stripped list."""
        with open(filename) as src:
            return [line.strip() for line in src.readlines()]

    @staticmethod
    def get_verifier_result(verif_id):
        """Retrieve verification results."""
        result = {
            'num_tests': 0,
            'num_success': 0,
            'num_failures': 0,
            'num_skipped': 0
        }
        cmd = ["rally", "verify", "show", "--uuid", verif_id]
        LOGGER.info("Showing result for a verification: '%s'.", cmd)
        with subprocess.Popen(
                cmd, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT) as proc:
            for line in proc.stdout:
                LOGGER.info(line.decode("utf-8").rstrip())
                new_line = line.decode("utf-8").replace(' ', '').split('|')
                if 'Tests' in new_line:
                    break
                if 'Testscount' in new_line:
                    result['num_tests'] = int(new_line[2])
                elif 'Success' in new_line:
                    result['num_success'] = int(new_line[2])
                elif 'Skipped' in new_line:
                    result['num_skipped'] = int(new_line[2])
                elif 'Failures' in new_line:
                    result['num_failures'] = int(new_line[2])
        return result

    @staticmethod
    def backup_tempest_config(conf_file, res_dir):
        """
        Copy config file to tempest results directory
        """
        if not os.path.exists(res_dir):
            os.makedirs(res_dir)
        shutil.copyfile(conf_file,
                        os.path.join(res_dir, 'tempest.conf'))

    @staticmethod
    def create_verifier():
        """Create new verifier"""
        LOGGER.info("Create verifier from existing repo...")
        cmd = ['rally', 'verify', 'delete-verifier',
               '--id', str(getattr(config.CONF, 'tempest_verifier_name')),
               '--force']
        try:
            output = subprocess.check_output(cmd)
            LOGGER.info("%s\n%s", " ".join(cmd), output.decode("utf-8"))
        except subprocess.CalledProcessError:
            pass

        cmd = ['rally', 'verify', 'create-verifier',
               '--source', str(getattr(config.CONF, 'dir_repo_tempest')),
               '--name', str(getattr(config.CONF, 'tempest_verifier_name')),
               '--type', 'tempest', '--system-wide']
        output = subprocess.check_output(cmd)
        LOGGER.info("%s\n%s", " ".join(cmd), output.decode("utf-8"))
        return TempestCommon.get_verifier_id()

    @staticmethod
    def get_verifier_id():
        """
        Returns verifier id for current Tempest
        """
        cmd = ("rally verify list-verifiers | awk '/" +
               getattr(config.CONF, 'tempest_verifier_name') +
               "/ {print $2}'")
        with subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL) as proc:
            verifier_uuid = proc.stdout.readline().rstrip()
        return verifier_uuid.decode("utf-8")

    @staticmethod
    def get_verifier_repo_dir(verifier_id):
        """
        Returns installed verifier repo directory for Tempest
        """
        return os.path.join(getattr(config.CONF, 'dir_rally_inst'),
                            'verification',
                            'verifier-{}'.format(verifier_id),
                            'repo')

    @staticmethod
    def get_verifier_deployment_dir(verifier_id, deployment_id):
        """
        Returns Rally deployment directory for current verifier
        """
        return os.path.join(getattr(config.CONF, 'dir_rally_inst'),
                            'verification',
                            'verifier-{}'.format(verifier_id),
                            'for-deployment-{}'.format(deployment_id))

    @staticmethod
    def update_tempest_conf_file(conf_file, rconfig):
        """Update defined paramters into tempest config file"""
        with open(TempestCommon.tempest_conf_yaml) as yfile:
            conf_yaml = yaml.safe_load(yfile)
        if conf_yaml:
            sections = rconfig.sections()
            for section in conf_yaml:
                if section not in sections:
                    rconfig.add_section(section)
                sub_conf = conf_yaml.get(section)
                for key, value in sub_conf.items():
                    rconfig.set(section, key, value)

        with open(conf_file, 'w') as config_file:
            rconfig.write(config_file)

    @staticmethod
    def configure_tempest_update_params(
            tempest_conf_file, image_id=None, flavor_id=None,
            compute_cnt=1, image_alt_id=None, flavor_alt_id=None,
            admin_role_name='admin', cidr='192.168.120.0/24',
            domain_id='default'):
        # pylint: disable=too-many-branches,too-many-arguments
        # pylint: disable=too-many-statements,too-many-locals
        """
        Add/update needed parameters into tempest.conf file
        """
        LOGGER.debug("Updating selected tempest.conf parameters...")
        rconfig = configparser.RawConfigParser()
        rconfig.read(tempest_conf_file)
        rconfig.set(
            'compute', 'volume_device_name', env.get('VOLUME_DEVICE_NAME'))
        if image_id is not None:
            rconfig.set('compute', 'image_ref', image_id)
        if image_alt_id is not None:
            rconfig.set('compute', 'image_ref_alt', image_alt_id)
        if flavor_id is not None:
            rconfig.set('compute', 'flavor_ref', flavor_id)
        if flavor_alt_id is not None:
            rconfig.set('compute', 'flavor_ref_alt', flavor_alt_id)
        if compute_cnt > 1:
            # enable multinode tests
            rconfig.set('compute', 'min_compute_nodes', compute_cnt)
            rconfig.set('compute-feature-enabled', 'live_migration', True)
        if os.environ.get('OS_REGION_NAME'):
            rconfig.set('identity', 'region', os.environ.get('OS_REGION_NAME'))
        rconfig.set('identity', 'admin_role', admin_role_name)
        rconfig.set('identity', 'default_domain_id', domain_id)
        if not rconfig.has_section('network'):
            rconfig.add_section('network')
        rconfig.set('network', 'default_network', cidr)
        rconfig.set('network', 'project_network_cidr', cidr)
        rconfig.set('network', 'project_networks_reachable', False)
        rconfig.set(
            'identity', 'v3_endpoint_type',
            os.environ.get('OS_INTERFACE', 'public'))

        sections = rconfig.sections()
        services_list = [
            'compute', 'volume', 'image', 'network', 'data-processing',
            'object-storage', 'orchestration']
        for service in services_list:
            if service not in sections:
                rconfig.add_section(service)
            rconfig.set(service, 'endpoint_type',
                        os.environ.get('OS_INTERFACE', 'public'))

        LOGGER.debug('Add/Update required params defined in tempest_conf.yaml '
                     'into tempest.conf file')
        TempestCommon.update_tempest_conf_file(tempest_conf_file, rconfig)

    @staticmethod
    def configure_verifier(deployment_dir):
        """
        Execute rally verify configure-verifier, which generates tempest.conf
        """
        cmd = ['rally', 'verify', 'configure-verifier', '--reconfigure',
               '--id', str(getattr(config.CONF, 'tempest_verifier_name'))]
        output = subprocess.check_output(cmd)
        LOGGER.info("%s\n%s", " ".join(cmd), output.decode("utf-8"))

        LOGGER.debug("Looking for tempest.conf file...")
        tempest_conf_file = os.path.join(deployment_dir, "tempest.conf")
        if not os.path.isfile(tempest_conf_file):
            LOGGER.error("Tempest configuration file %s NOT found.",
                         tempest_conf_file)
            return None
        return tempest_conf_file

    def generate_test_list(self, **kwargs):
        """Generate test list based on the test mode."""
        LOGGER.debug("Generating test case list...")
        self.backup_tempest_config(self.conf_file, '/etc')
        if kwargs.get('mode') == 'custom':
            if os.path.isfile(self.tempest_custom):
                shutil.copyfile(
                    self.tempest_custom, self.list)
            else:
                raise Exception("Tempest test list file %s NOT found."
                                % self.tempest_custom)
        else:
            testr_mode = kwargs.get(
                'mode', r'^tempest\.(api|scenario).*\[.*\bsmoke\b.*\]$')
            cmd = "(cd {0}; stestr list '{1}' >{2} 2>/dev/null)".format(
                self.verifier_repo_dir, testr_mode, self.list)
            output = subprocess.check_output(cmd, shell=True)
            LOGGER.info("%s\n%s", cmd, output.decode("utf-8"))
        os.remove('/etc/tempest.conf')

    def apply_tempest_blacklist(self, black_list):
        """Exclude blacklisted test cases."""
        LOGGER.debug("Applying tempest blacklist...")
        if os.path.exists(self.raw_list):
            os.remove(self.raw_list)
        os.rename(self.list, self.raw_list)
        cases_file = self.read_file(self.raw_list)
        with open(self.list, 'w') as result_file:
            black_tests = []
            try:
                deploy_scenario = env.get('DEPLOY_SCENARIO')
                if bool(deploy_scenario):
                    # if DEPLOY_SCENARIO is set we read the file
                    with open(black_list) as black_list_file:
                        black_list_yaml = yaml.safe_load(black_list_file)
                        black_list_file.close()
                        for item in black_list_yaml:
                            scenarios = item['scenarios']
                            in_it = rally.RallyBase.in_iterable_re
                            if in_it(deploy_scenario, scenarios):
                                tests = item['tests']
                                black_tests.extend(tests)
            except Exception:  # pylint: disable=broad-except
                black_tests = []
                LOGGER.debug("Tempest blacklist file does not exist.")

        for cases_line in cases_file:
            for black_tests_line in black_tests:
                if re.search(black_tests_line, cases_line):
                    break
            else:
                result_file.write(str(cases_line) + '\n')
        result_file.close()

    def run_verifier_tests(self, **kwargs):
        """Execute tempest test cases."""
        cmd = ["rally", "verify", "start", "--load-list",
               self.list]
        cmd.extend(kwargs.get('option', []))
        LOGGER.info("Starting Tempest test suite: '%s'.", cmd)

        with open(
                os.path.join(self.res_dir, "tempest.log"), 'w+') as f_stdout:

            with subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    bufsize=1) as proc:

                with proc.stdout:
                    for line in iter(proc.stdout.readline, b''):
                        if re.search(r"\} tempest\.", line.decode("utf-8")):
                            LOGGER.info(line.rstrip())
                        elif re.search(r'(?=\(UUID=(.*)\))',
                                       line.decode("utf-8")):
                            self.verification_id = re.search(
                                r'(?=\(UUID=(.*)\))',
                                line.decode("utf-8")).group(1)
                        f_stdout.write(line.decode("utf-8"))
                    proc.wait()

        if self.verification_id is None:
            raise Exception('Verification UUID not found')
        LOGGER.info('Verification UUID: %s', self.verification_id)

        shutil.copy(
            "{}/tempest.log".format(self.deployment_dir),
            "{}/tempest.debug.log".format(self.res_dir))

    def parse_verifier_result(self):
        """Parse and save test results."""
        stat = self.get_verifier_result(self.verification_id)
        try:
            num_executed = stat['num_tests'] - stat['num_skipped']
            try:
                self.result = 100 * stat['num_success'] / num_executed
            except ZeroDivisionError:
                self.result = 0
                if stat['num_tests'] > 0:
                    LOGGER.info("All tests have been skipped")
                else:
                    LOGGER.error("No test has been executed")
                    return

            with open(os.path.join(self.res_dir,
                                   "rally.log"), 'r') as logfile:
                output = logfile.read()

            success_testcases = []
            for match in re.findall(r'.*\{\d{1,2}\} (.*?) \.{3} success ',
                                    output):
                success_testcases.append(match)
            failed_testcases = []
            for match in re.findall(r'.*\{\d{1,2}\} (.*?) \.{3} fail',
                                    output):
                failed_testcases.append(match)
            skipped_testcases = []
            for match in re.findall(r'.*\{\d{1,2}\} (.*?) \.{3} skip(?::| )',
                                    output):
                skipped_testcases.append(match)

            self.details = {"tests_number": stat['num_tests'],
                            "success_number": stat['num_success'],
                            "skipped_number": stat['num_skipped'],
                            "failures_number": stat['num_failures'],
                            "success": success_testcases,
                            "skipped": skipped_testcases,
                            "failures": failed_testcases}
        except Exception:  # pylint: disable=broad-except
            self.result = 0

        LOGGER.info("Tempest %s success_rate is %s%%",
                    self.case_name, self.result)

    def update_rally_regex(self, rally_conf='/etc/rally/rally.conf'):
        """Set image name as tempest img_name_regex"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(rally_conf)
        if not rconfig.has_section('openstack'):
            rconfig.add_section('openstack')
        rconfig.set('openstack', 'img_name_regex', '^{}$'.format(
            self.image.name))
        with open(rally_conf, 'w') as config_file:
            rconfig.write(config_file)

    def update_default_role(self, rally_conf='/etc/rally/rally.conf'):
        """Detect and update the default role if required"""
        role = self.get_default_role(self.cloud)
        if not role:
            return
        rconfig = configparser.RawConfigParser()
        rconfig.read(rally_conf)
        if not rconfig.has_section('openstack'):
            rconfig.add_section('openstack')
        rconfig.set('openstack', 'swift_operator_role', role.name)
        with open(rally_conf, 'w') as config_file:
            rconfig.write(config_file)

    @staticmethod
    def clean_rally_conf(rally_conf='/etc/rally/rally.conf'):
        """Clean Rally config"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(rally_conf)
        if rconfig.has_option('openstack', 'img_name_regex'):
            rconfig.remove_option('openstack', 'img_name_regex')
        if rconfig.has_option('openstack', 'swift_operator_role'):
            rconfig.remove_option('openstack', 'swift_operator_role')
        with open(rally_conf, 'w') as config_file:
            rconfig.write(config_file)

    def update_auth_section(self):
        """Update auth section in tempest.conf"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        if not rconfig.has_section("auth"):
            rconfig.add_section("auth")
        if env.get("NEW_USER_ROLE").lower() != "member":
            tempest_roles = []
            if rconfig.has_option("auth", "tempest_roles"):
                tempest_roles = functest_utils.convert_ini_to_list(
                    rconfig.get("auth", "tempest_roles"))
            rconfig.set(
                'auth', 'tempest_roles',
                functest_utils.convert_list_to_ini(
                    [env.get("NEW_USER_ROLE")] + tempest_roles))
        if not json.loads(env.get("USE_DYNAMIC_CREDENTIALS").lower()):
            rconfig.set('auth', 'use_dynamic_credentials', False)
            account_file = os.path.join(
                getattr(config.CONF, 'dir_functest_data'), 'accounts.yaml')
            assert os.path.exists(
                account_file), "{} doesn't exist".format(account_file)
            rconfig.set('auth', 'test_accounts_file', account_file)
        if env.get('NO_TENANT_NETWORK').lower() == 'true':
            rconfig.set('auth', 'create_isolated_networks', False)
        with open(self.conf_file, 'w') as config_file:
            rconfig.write(config_file)

    def update_network_section(self):
        """Update network section in tempest.conf"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        if self.ext_net:
            if not rconfig.has_section('network'):
                rconfig.add_section('network')
            rconfig.set('network', 'public_network_id', self.ext_net.id)
            rconfig.set('network', 'floating_network_name', self.ext_net.name)
            rconfig.set('network-feature-enabled', 'floating_ips', True)
        else:
            if not rconfig.has_section('network-feature-enabled'):
                rconfig.add_section('network-feature-enabled')
            rconfig.set('network-feature-enabled', 'floating_ips', False)
        with open(self.conf_file, 'w') as config_file:
            rconfig.write(config_file)

    def update_compute_section(self):
        """Update compute section in tempest.conf"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        if not rconfig.has_section('compute'):
            rconfig.add_section('compute')
        rconfig.set(
            'compute', 'fixed_network_name',
            self.network.name if self.network else env.get("EXTERNAL_NETWORK"))
        with open(self.conf_file, 'w') as config_file:
            rconfig.write(config_file)

    def update_validation_section(self):
        """Update validation section in tempest.conf"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        if not rconfig.has_section('validation'):
            rconfig.add_section('validation')
        rconfig.set(
            'validation', 'connect_method',
            'floating' if self.ext_net else 'fixed')
        rconfig.set(
            'validation', 'network_for_ssh',
            self.network.name if self.network else env.get("EXTERNAL_NETWORK"))
        with open(self.conf_file, 'w') as config_file:
            rconfig.write(config_file)

    def update_scenario_section(self):
        """Update scenario section in tempest.conf"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        filename = getattr(
            config.CONF, '{}_image'.format(self.case_name), self.filename)
        if not rconfig.has_section('scenario'):
            rconfig.add_section('scenario')
        rconfig.set('scenario', 'img_file', filename)
        rconfig.set('scenario', 'img_disk_format', getattr(
            config.CONF, '{}_image_format'.format(self.case_name),
            self.image_format))
        extra_properties = self.extra_properties.copy()
        if env.get('IMAGE_PROPERTIES'):
            extra_properties.update(
                functest_utils.convert_ini_to_dict(
                    env.get('IMAGE_PROPERTIES')))
        extra_properties.update(
            getattr(config.CONF, '{}_extra_properties'.format(
                self.case_name), {}))
        rconfig.set(
            'scenario', 'img_properties',
            functest_utils.convert_dict_to_ini(extra_properties))
        with open(self.conf_file, 'w') as config_file:
            rconfig.write(config_file)

    def update_dashboard_section(self):
        """Update dashboard section in tempest.conf"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        if env.get('DASHBOARD_URL'):
            if not rconfig.has_section('dashboard'):
                rconfig.add_section('dashboard')
            rconfig.set('dashboard', 'dashboard_url', env.get('DASHBOARD_URL'))
        else:
            rconfig.set('service_available', 'horizon', False)
        with open(self.conf_file, 'w') as config_file:
            rconfig.write(config_file)

    def configure(self, **kwargs):  # pylint: disable=unused-argument
        """
        Create all openstack resources for tempest-based testcases and write
        tempest.conf.
        """
        if not os.path.exists(self.res_dir):
            os.makedirs(self.res_dir)
        self.deployment_id = rally.RallyBase.create_rally_deployment(
            environ=self.project.get_environ())
        if not self.deployment_id:
            raise Exception("Deployment create failed")
        self.verifier_id = self.create_verifier()
        if not self.verifier_id:
            raise Exception("Verifier create failed")
        self.verifier_repo_dir = self.get_verifier_repo_dir(
            self.verifier_id)
        self.deployment_dir = self.get_verifier_deployment_dir(
            self.verifier_id, self.deployment_id)

        compute_cnt = self.count_hypervisors() if self.count_hypervisors(
            ) <= 10 else 10
        self.image_alt = self.publish_image_alt()
        self.flavor_alt = self.create_flavor_alt()
        LOGGER.debug("flavor: %s", self.flavor_alt)

        self.conf_file = self.configure_verifier(self.deployment_dir)
        if not self.conf_file:
            raise Exception("Tempest verifier configuring failed")
        self.configure_tempest_update_params(
            self.conf_file,
            image_id=self.image.id,
            flavor_id=self.flavor.id,
            compute_cnt=compute_cnt,
            image_alt_id=self.image_alt.id,
            flavor_alt_id=self.flavor_alt.id,
            admin_role_name=self.role_name, cidr=self.cidr,
            domain_id=self.project.domain.id)
        self.update_auth_section()
        self.update_network_section()
        self.update_compute_section()
        self.update_validation_section()
        self.update_scenario_section()
        self.update_dashboard_section()
        self.backup_tempest_config(self.conf_file, self.res_dir)

    def run(self, **kwargs):
        self.start_time = time.time()
        try:
            assert super().run(
                **kwargs) == testcase.TestCase.EX_OK
            if not os.path.exists(self.res_dir):
                os.makedirs(self.res_dir)
            self.update_rally_regex()
            self.update_default_role()
            rally.RallyBase.update_rally_logs(self.res_dir)
            shutil.copy("/etc/rally/rally.conf", self.res_dir)
            self.configure(**kwargs)
            self.generate_test_list(**kwargs)
            self.apply_tempest_blacklist(TempestCommon.tempest_blacklist)
            if env.get('PUBLIC_ENDPOINT_ONLY').lower() == 'true':
                self.apply_tempest_blacklist(
                    TempestCommon.tempest_public_blacklist)
            self.run_verifier_tests(**kwargs)
            self.parse_verifier_result()
            rally.RallyBase.verify_report(
                os.path.join(self.res_dir, "tempest-report.html"),
                self.verification_id)
            rally.RallyBase.verify_report(
                os.path.join(self.res_dir, "tempest-report.xml"),
                self.verification_id, "junit-xml")
            res = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            LOGGER.exception('Error with run')
            self.result = 0
            res = testcase.TestCase.EX_RUN_ERROR
        self.stop_time = time.time()
        return res

    def clean(self):
        """
        Cleanup all OpenStack objects. Should be called on completion.
        """
        self.clean_rally_conf()
        rally.RallyBase.clean_rally_logs()
        if self.image_alt:
            self.cloud.delete_image(self.image_alt)
        if self.flavor_alt:
            self.orig_cloud.delete_flavor(self.flavor_alt.id)
        super().clean()

    def is_successful(self):
        """The overall result of the test."""
        skips = self.details.get("skipped_number", 0)
        if skips > 0 and self.deny_skipping:
            return testcase.TestCase.EX_TESTCASE_FAILED
        if self.tests_count and (
                self.details.get("tests_number", 0) != self.tests_count):
            return testcase.TestCase.EX_TESTCASE_FAILED
        return super().is_successful()


class TempestHeat(TempestCommon):
    """Tempest Heat testcase implementation class."""

    filename_alt = ('/home/opnfv/functest/images/'
                    'Fedora-Cloud-Base-30-1.2.x86_64.qcow2')
    flavor_alt_ram = 512
    flavor_alt_vcpus = 1
    flavor_alt_disk = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user2 = self.orig_cloud.create_user(
            name='{}-user2_{}'.format(self.case_name, self.project.guid),
            password=self.project.password,
            domain_id=self.project.domain.id)
        self.orig_cloud.grant_role(
            self.role_name, user=self.user2.id,
            project=self.project.project.id, domain=self.project.domain.id)
        if not self.orig_cloud.get_role("heat_stack_owner"):
            self.role = self.orig_cloud.create_role("heat_stack_owner")
        self.orig_cloud.grant_role(
            "heat_stack_owner", user=self.user2.id,
            project=self.project.project.id,
            domain=self.project.domain.id)

    def configure(self, **kwargs):
        assert self.user2
        super().configure(**kwargs)
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        if not rconfig.has_section('heat_plugin'):
            rconfig.add_section('heat_plugin')
        # It fails if region and domain ids are unset
        rconfig.set(
            'heat_plugin', 'region',
            os.environ.get('OS_REGION_NAME', 'RegionOne'))
        rconfig.set('heat_plugin', 'auth_url', os.environ["OS_AUTH_URL"])
        rconfig.set('heat_plugin', 'project_domain_id', self.project.domain.id)
        rconfig.set('heat_plugin', 'user_domain_id', self.project.domain.id)
        rconfig.set(
            'heat_plugin', 'project_domain_name', self.project.domain.name)
        rconfig.set(
            'heat_plugin', 'user_domain_name', self.project.domain.name)
        rconfig.set('heat_plugin', 'username', self.user2.name)
        rconfig.set('heat_plugin', 'password', self.project.password)
        rconfig.set('heat_plugin', 'project_name', self.project.project.name)
        rconfig.set('heat_plugin', 'admin_username', self.project.user.name)
        rconfig.set('heat_plugin', 'admin_password', self.project.password)
        rconfig.set(
            'heat_plugin', 'admin_project_name', self.project.project.name)
        rconfig.set('heat_plugin', 'image_ref', self.image_alt.id)
        rconfig.set('heat_plugin', 'instance_type', self.flavor_alt.id)
        rconfig.set('heat_plugin', 'minimal_image_ref', self.image.id)
        rconfig.set('heat_plugin', 'minimal_instance_type', self.flavor.id)
        if self.ext_net:
            rconfig.set(
                'heat_plugin', 'floating_network_name', self.ext_net.name)
        if self.network:
            rconfig.set('heat_plugin', 'fixed_network_name', self.network.name)
            rconfig.set('heat_plugin', 'fixed_subnet_name', self.subnet.name)
            rconfig.set('heat_plugin', 'network_for_ssh', self.network.name)
        else:
            LOGGER.warning(
                'No tenant network created. '
                'Trying EXTERNAL_NETWORK as a fallback')
            rconfig.set(
                'heat_plugin', 'fixed_network_name',
                env.get("EXTERNAL_NETWORK"))
            rconfig.set(
                'heat_plugin', 'network_for_ssh', env.get("EXTERNAL_NETWORK"))
        with open(self.conf_file, 'w') as config_file:
            rconfig.write(config_file)
        self.backup_tempest_config(self.conf_file, self.res_dir)

    def clean(self):
        """
        Cleanup all OpenStack objects. Should be called on completion.
        """
        super().clean()
        if self.user2:
            self.orig_cloud.delete_user(self.user2.id)
