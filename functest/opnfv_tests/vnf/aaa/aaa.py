#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import sys

import argparse

import functest.core.testcase as testcase
import functest.core.vnf as vnf


class AaaVnf(vnf.VnfOnBoarding):

    logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "aaa"
        super(AaaVnf, self).__init__(**kwargs)

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
        if self.result is "PASS":
            return self.EX_OK
        else:
            return self.EX_RUN_ERROR

    def run(self):
        kwargs = {}
        return self.main(**kwargs)


if __name__ == '__main__':
    logging.basicConfig()
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
