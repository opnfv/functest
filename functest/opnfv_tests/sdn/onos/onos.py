#!/usr/bin/env python

# Copyright (c) 2017 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import os
import re
import subprocess
import shutil
import time
import urlparse

from functest.core import testcase
from functest.utils.constants import CONST
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as openstack_utils


class OnosBase(testcase.TestCase):
    onos_repo_path = CONST.__getattribute__('dir_repo_onos')
    onos_sfc_image_name = CONST.__getattribute__('onos_sfc_image_name')
    onos_sfc_image_path = os.path.join(
        CONST.__getattribute__('images_data'),
        CONST.__getattribute__('onos_sfc_image_file_name'))
    onos_sfc_path = os.path.join(CONST.__getattribute__('dir_repo_functest'),
                                 CONST.__getattribute__('dir_onos_sfc'))
    installer_type = CONST.__getattribute__('INSTALLER_TYPE')
    logger = ft_logger.Logger(__name__).getLogger()

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "onos_base"
        super(OnosBase, self).__init__(**kwargs)

    def run(self):
        self.start_time = time.time()
        try:
            self._run()
            res = testcase.TestCase.EX_OK
        except Exception as e:
            self.logger.error('Error with run: %s', e)
            res = testcase.TestCase.EX_RUN_ERROR

        self.stop_time = time.time()
        return res

    def _run(self):
        raise NotImplementedError('_run is not implemented')


class Onos(OnosBase):
    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "onos"
        super(Onos, self).__init__(**kwargs)
        self.log_path = os.path.join(self.onos_repo_path, 'TestON/logs')

    def set_onos_ip(self):
        if (self.installer_type and
                self.installer_type.lower() == 'joid'):
            sdn_controller_env = os.getenv('SDN_CONTROLLER')
            OC1 = re.search(r"\d+\.\d+\.\d+\.\d+", sdn_controller_env).group()
        else:
            neutron_url = openstack_utils.get_endpoint(service_type='network')
            OC1 = urlparse.urlparse(neutron_url).hostname
        os.environ['OC1'] = OC1
        self.logger.debug("ONOS IP is %s", OC1)

    def run_onos_script(self, testname):
        cli_dir = os.path.join(self.onos_repo_path, 'TestON/bin/cli.py')
        cmd = '{0} run {1}'.format(cli_dir, testname)
        self.logger.debug("Run script: %s", testname)
        ft_utils.execute_command_raise(
            cmd,
            error_msg=('Error when running ONOS script: %s'
                       % (testname)))

    def clean_existing_logs(self):
        log_dir = [f for f in os.listdir(self.log_path)]
        for log in log_dir:
            try:
                if os.path.isdir(log):
                    shutil.rmtree(log)
                elif os.path.isfile(log):
                    os.remove(log)
            except OSError as e:
                self.logger.error('Error with deleting file %s: %s',
                                  log, e.strerror)

    def get_result(self):
        cmd = 'grep -rnh Fail {0}'.format(self.log_path)
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        for line in p.stdout:
            self.logger.debug(line)
            if re.search("\s+[1-9]+\s+", line):
                self.logger.debug("Testcase Fails\n" + line)

        cmd = "grep -rnh 'Execution Time' {0}".format(self.log_path)
        result_buffer = os.popen(cmd).read()
        time1 = result_buffer[114:128]
        time2 = result_buffer[28:42]
        cmd = "grep -rnh 'Success Percentage' {0}".format(
            os.path.join(self.log_path, "FUNCvirNetNB_*"))
        result_buffer = os.popen(cmd).read()
        if result_buffer.find('100%') >= 0:
            result1 = 'Success'
        else:
            result1 = 'Failed'
        cmd = "grep -rnh 'Success Percentage' {0}".format(
            os.path.join(self.log_path, "FUNCvirNetNBL3*"))
        result_buffer = os.popen(cmd).read()
        if result_buffer.find('100%') >= 0:
            result2 = 'Success'
        else:
            result2 = 'Failed'
        status1 = []
        status2 = []
        cmd = "grep -rnh 'h3' {0}".format(
            os.path.join(self.log_path, "FUNCvirNetNB_*"))
        result_buffer = os.popen(cmd).read()
        pattern = re.compile("<h3>([^-]+) - ([^-]+) - (\S*)</h3>")
        # res = pattern.search(result_buffer).groups()
        res = pattern.findall(result_buffer)
        i = 0
        for index in range(len(res)):
            status1.append({'Case name:': res[i][0] + res[i][1],
                            'Case result': res[i][2]})
            i = i + 1
        cmd = "grep -rnh 'h3' {0}".format(
            os.path.join(self.log_path, "FUNCvirNetNBL3*"))
        result_buffer = os.popen(cmd).read()
        pattern = re.compile("<h3>([^-]+) - ([^-]+) - (\S*)</h3>")
        res = pattern.findall(result_buffer)
        i = 0
        for index in range(len(res)):
            status2.append({'Case name:': res[i][0] + res[i][1],
                            'Case result': res[i][2]})
            i = i + 1
        payload = {'FUNCvirNet': {'duration': time1,
                                  'result': result1,
                                  'status': status1},
                   'FUNCvirNetL3': {'duration': time2,
                                    'result': result2,
                                    'status': status2}}
        return payload

    def parse_result(self):
        result = self.get_result()
        status = "FAIL"
        try:
            if (result['FUNCvirNet']['result'] == "Success" and
                    result['FUNCvirNetL3']['result'] == "Success"):
                status = "PASS"
        except Exception:
            self.logger.error("Unable to set ONOS result")

        self.result = status
        self.details = result

    def _run(self):
        self.clean_existing_logs()
        self.set_onos_ip()
        self.run_onos_script('FUNCvirNetNB')
        self.run_onos_script('FUNCvirNetNBL3')
        self.parse_result()


class OnosSfc(OnosBase):
    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "onos_sfc"
        super(OnosSfc, self).__init__(**kwargs)

    def get_ip(self, type):
        url = openstack_utils.get_endpoint(service_type=type)
        self.logger.debug('get_ip for %s: %s', type, url)
        return urlparse.urlparse(url).hostname

    def update_sfc_onos_file(self, before, after):
        file_dir = os.path.join(self.onos_sfc_path, "sfc_onos.py")
        cmd = "sed -i 's/{0}/{1}/g' {2}".format(before,
                                                after,
                                                file_dir)
        ft_utils.execute_command_raise(
            cmd,
            error_msg=('Error with replacing %s with %s'
                       % (before, after)))

    def create_image(self):
        self.logger.warn('inside create_image')
        glance_client = openstack_utils.get_glance_client()
        image_id = openstack_utils.create_glance_image(
            glance_client,
            self.onos_sfc_image_name,
            self.onos_sfc_image_path)
        if image_id is None:
            raise Exception('Failed to create image')

        self.logger.debug("Image '%s' with ID=%s is created successfully.",
                          self.onos_sfc_image_name, image_id)

    def set_sfc_conf(self):
        self.update_sfc_onos_file("keystone_ip", self.get_ip("keystone"))
        self.update_sfc_onos_file("neutron_ip", self.get_ip("neutron"))
        self.update_sfc_onos_file("nova_ip", self.get_ip("nova"))
        self.update_sfc_onos_file("glance_ip", self.get_ip("glance"))
        self.update_sfc_onos_file("console",
                                  CONST.__getattribute__('OS_PASSWORD'))
        neutron_client = openstack_utils.get_neutron_client()
        ext_net = openstack_utils.get_external_net(neutron_client)
        self.update_sfc_onos_file("admin_floating_net", ext_net)
        self.logger.debug("SFC configuration is modified")

    def sfc_test(self):
        cmd = 'python {0}'.format(os.path.join(self.onos_sfc_path, 'sfc.py'))
        ft_utils.execute_command_raise(cmd,
                                       error_msg='Error with testing SFC')

    def _run(self):
        self.create_image()
        self.set_sfc_conf()
        self.sfc_test()
