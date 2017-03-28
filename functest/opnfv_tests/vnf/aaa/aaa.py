#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import sys

import argparse

import functest.core.testcase as testcase
import functest.core.vnf_base as vnf_base
import functest.utils.functest_logger as ft_logger


class AaaVnf(vnf_base.VnfOnBoardingBase):

    logger = ft_logger.Logger("VNF AAA").getLogger()

    def __init__(self):
        super(AaaVnf, self).__init__(case_name="aaa")

    def deploy_orchestrator(self):
        self.logger.info("No VNFM needed to deploy a free radius here")
        return None

# TODO see how to use build in exception form releng module
    def deploy_vnf(self):
        self.logger.info("Freeradius VNF deployment")
        # TODO apt-get update + config tuning
        deploy_vnf = {}
        deploy_vnf['status'] = "PASS"
        deploy_vnf['result'] = {}
        return deploy_vnf

    def test_vnf(self):
        self.logger.info("Run test towards freeradius")
        # TODO:  once the freeradius is deployed..make some tests
        test_vnf = {}
        test_vnf['status'] = "PASS"
        test_vnf['result'] = {}
        return test_vnf

    def main(self, **kwargs):
        self.logger.info("AAA VNF onboarding")
        self.execute()
        if self.criteria is "PASS":
            return self.EX_OK
        else:
            return self.EX_RUN_ERROR

    def run(self):
        kwargs = {}
        return self.main(**kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = vars(parser.parse_args())
    aaa_vnf = AaaVnf()
    try:
        result = aaa_vnf.main(**args)
        if result != testcase.TestCase.EX_OK:
            sys.exit(result)
        if args['pushtodb']:
            sys.exit(aaa_vnf.push_to_db())
    except Exception:
        sys.exit(testcase.TestCase.EX_RUN_ERROR)
