#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging

import functest.core.vnf as vnf


class AaaVnf(vnf.VnfOnBoarding):
    """AAA VNF sample"""

    logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "aaa"
        super(AaaVnf, self).__init__(**kwargs)

    def deploy_orchestrator(self):
        self.logger.info("No VNFM needed to deploy a free radius here")
        return True

    def deploy_vnf(self):
        self.logger.info("Freeradius VNF deployment")
        # find a way to deploy freeradius and tester (heat,manual, ..)
        deploy_vnf = {'status': 'PASS', 'version': 'xxxx'}
        self.details['deploy_vnf'] = deploy_vnf
        return True

    def test_vnf(self):
        self.logger.info("Run test towards freeradius")
        # once the freeradius is deployed..make some tests
        test_vnf = {'status': 'PASS', 'version': 'xxxx'}
        self.details['test_vnf'] = test_vnf
        return True
