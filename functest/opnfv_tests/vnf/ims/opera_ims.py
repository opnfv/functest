#!/usr/bin/env python

# Copyright (c) 2017 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
import os

from opera import openo_connect

import functest.core.vnf_base as vnf_base
from functest.utils.constants import CONST
import functest.utils.functest_logger as ft_logger


class ImsVnf(vnf_base.VnfOnBoardingBase):

    def __init__(self, project='functest', case='opera_ims',
                 repo=CONST.dir_repo_opera, cmd=''):
        super(ImsVnf, self).__init__(project, case, repo, cmd)
        self.logger = ft_logger.Logger("opera_ims").getLogger()
        self.case_dir = os.path.join(CONST.dir_functest_test, 'vnf/ims/')
        self.data_dir = CONST.dir_ims_data
        self.test_dir = CONST.dir_repo_vims_test

    def prepare(self):
        pass

    def clean(self):
        pass

    def deploy_vnf(self):
        self.logger.info("Opera vIMS Deployment")
        try:
            openo_msb_ip = os.environ['OPENO_MSB_IP']
        except KeyError as e:
            self.logger.error(e)
            self.step_failure('OPENO_MSB_IP is not specified')
        else:
            openo_connect.create_service(openo_msb_ip,
                                         'functest_opera',
                                         'VNF for functest testing')

    def test_vnf(self):
        ellis_ip = openo_connect.get_ellis_ip()
        dns_ip = openo_connect.get_dns_ip()
        self.config_ellis(ellis_ip)
        self.run_clearwater_live_test(dns_ip, 'clearwater.local', 'signup')

    def main(self, **kwargs):
        self.logger.info("Start to run Opera vIMS VNF onboarding test")
        self.execute()
        self.logger.info("Opera vIMS VNF onboarding test finished")
        if self.criteria is "PASS":
            return self.EX_OK
        else:
            return self.EX_RUN_ERROR

    def run(self):
        kwargs = {}
        return self.main(**kwargs)


if __name__ == '__main__':
    test = ImsVnf()
    test.deploy_vnf()
    test.test_vnf()

