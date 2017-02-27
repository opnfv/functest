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
import time
import urlparse

from functest.core import testcase_base
from functest.utils.constants import CONST
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as openstack_utils


logger = ft_logger.Logger("onos").getLogger()


class OnosBase(testcase_base.TestcaseBase):
    ONOSCI_PATH = CONST.dir_repo_onos
    ONOS_SFC_IMAGE_NAME = CONST.onos_sfc_image_name
    ONOS_SFC_IMAGE_PATH = os.path.join(CONST.dir_functest_data,
                                       CONST.onos_sfc_image_filename)
    ONOS_SFC_PATH = os.path.join(CONST.dir_repo_functest,
                                 CONST.dir_onos_sfc)

    def __init__(self):
        super(OnosBase, self).__init__()


class Onos(OnosBase):
    def __init__(self, arg):
        super(Onos, self).__init__()
        self.case_name = 'onos'

    def set_Onos_ip(self):
        if (CONST.INSTALLER_TYPE and
                CONST.INSTALLER_TYPE.lower() == 'joid'):
            cmd = "env | grep SDN_CONTROLLER"
            cmd_output = os.popen(cmd).read()
            OC1 = re.search(r"\d+\.\d+\.\d+\.\d+", cmd_output).group()
        else:
            neutron_url = openstack_utils.get_endpoint(service_type='network')
            OC1 = urlparse.urlparse(neutron_url).hostname
        os.environ['OC1'] = OC1
        logger.debug("ONOS IP is %s" % OC1)

    def run_script(self, testname):
        """
        Run ONOS Test Script
        Parameters:
        testname: ONOS Testcase Name
        """
        cli_dir = os.path.join(self.ONOSCI_PATH, 'onos/TestON/bin/cli.py')
        cmd = [cli_dir, ' run ', testname]
        logger.debug("Run script: %s" % testname)
        ft_utils.execute_command_raise(
            cmd,
            error_msg=('Error when running ONOS script: %s'
                       % (testname)))

    def get_result(self):
        log_path = os.join(self.ONOSCI_PATH, 'onos/TestON/logs')
        cmd = 'grep -rnh Fail {0}'.format(log_path)
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        for line in p.stdout:
            logger.debug(line)
            if re.search("\s+[1-9]+\s+", line):
                logger.debug("Testcase Fails\n" + line)

        cmd = "grep -rnh 'Execution Time' {0}".format(log_path)
        Resultbuffer = os.popen(cmd).read()
        time1 = Resultbuffer[114:128]
        time2 = Resultbuffer[28:42]
        cmd = "grep -rnh 'Success Percentage' {0}".format(
            os.path.join(log_path, "FUNCvirNetNB_*"))
        Resultbuffer = os.popen(cmd).read()
        if Resultbuffer.find('100%') >= 0:
            result1 = 'Success'
        else:
            result1 = 'Failed'
        cmd = "grep -rnh 'Success Percentage' {0}".format(
            os.path.join(log_path, "FUNCvirNetNBL3*"))
        Resultbuffer = os.popen(cmd).read()
        if Resultbuffer.find('100%') >= 0:
            result2 = 'Success'
        else:
            result2 = 'Failed'
        status1 = []
        status2 = []
        cmd = "grep -rnh 'h3' {0}".format(
            os.path.join(log_path, "FUNCvirNetNB_*"))
        Resultbuffer = os.popen(cmd).read()
        pattern = re.compile("<h3>([^-]+) - ([^-]+) - (\S*)</h3>")
        # res = pattern.search(Resultbuffer).groups()
        res = pattern.findall(Resultbuffer)
        i = 0
        for index in range(len(res)):
            status1.append({'Case name:': res[i][0] + res[i][1],
                            'Case result': res[i][2]})
            i = i + 1
        cmd = "grep -rnh 'h3' {0}".format(
            os.path.join(log_path, "FUNCvirNetNBL3*"))
        Resultbuffer = os.popen(cmd).read()
        pattern = re.compile("<h3>([^-]+) - ([^-]+) - (\S*)</h3>")
        res = pattern.findall(Resultbuffer)
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
        except:
            logger.error("Unable to set ONOS criteria")

        self.criteria = status
        self.details = result

    def run(self):
        self.start_time = time.time()
        try:
            self.set_Onos_ip()
            self.run_script('FUNCvirNetNB')
            self.run_script('FUNCvirNetNBL3')
            self.parse_result()
            res = testcase_base.TestcaseBase.EX_OK
        except Exception as e:
            logger.error('Error with run: %s', e)
            res = testcase_base.TestcaseBase.EX_RUN_ERROR

        self.stop_time = time.time()
        return res


class OnosSfc(OnosBase):
    def __init__(self, arg):
        super(OnosSfc, self).__init__()
        self.case_name = 'onos_sfc'

    def get_ip(type):
        url = openstack_utils.get_endpoint(service_type=type)
        logger.debug('get_ip for %s: %s' % (type, url))
        return urlparse.urlparse(url).hostname

    def replace(self, before, after):
        file_dir = os.path.join(self.ONOS_SFC_PATH, "sfc_onos.py")
        cmd = ["sed -i 's/", before, "/", after, "/g' ", file_dir]
        ft_utils.execute_command_raise(
            cmd,
            error_msg=('Error with replacing %s with %s'
                       % (before, after)))

    def create_image(self):
        glance_client = openstack_utils.get_glance_client()
        image_id = openstack_utils.create_glance_image(
            glance_client,
            self.ONOS_SFC_IMAGE_NAME,
            self.ONOS_SFC_IMAGE_PATH)
        if image_id is None:
            raise Exception('Failed to create image')

        logger.debug("Image '%s' with ID=%s is created successfully."
                     % (self.ONOS_SFC_IMAGE_NAME, image_id))

    def set_sfc_conf(self):
        self.replace("keystone_ip", self.get_ip("keystone"))
        self.replace("neutron_ip", self.get_ip("neutron"))
        self.replace("nova_ip", self.get_ip("nova"))
        self.replace("glance_ip", self.get_ip("glance"))
        self.replace("console", CONST.OS_PASSWORD)
        neutron_client = openstack_utils.get_neutron_client()
        ext_net = openstack_utils.get_external_net(neutron_client)
        self.replace("admin_floating_net", ext_net)
        logger.debug("SFC configuration is modified")

    def sfc_test(self):
        cmd = ['python ', os.path.join(self.ONOS_SFC_PATH, 'sfc.py')]
        ft_utils.execute_command_raise(cmd,
                                       error_msg='Error with testing SFC')

    def run(self):
        self.start_time = time.time()
        try:
            self.create_image()
            self.set_sfc_conf()
            self.sfc_test()
            res = testcase_base.TestcaseBase.EX_OK
        except Exception as e:
            logger.error('Error with run: %s' % e)
            res = testcase_base.TestcaseBase.EX_RUN_ERROR

        self.stop_time = time.time()
        return res
