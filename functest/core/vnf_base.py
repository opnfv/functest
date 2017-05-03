#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import inspect
import time

import functest.core.testcase as base
from functest.utils.constants import CONST
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils


class VnfOnBoardingBase(base.TestCase):

    logger = ft_logger.Logger(__name__).getLogger()

    def __init__(self, **kwargs):
        super(VnfOnBoardingBase, self).__init__(**kwargs)
        self.repo = kwargs.get('repo', '')
        self.cmd = kwargs.get('cmd', '')
        self.details = {}
        self.result_dir = CONST.__getattribute__('dir_results')
        self.details_step_mapping = dict(
            deploy_orchestrator='orchestrator',
            deploy_vnf='vnf',
            test_vnf='test_vnf',
            prepare='prepare_env')
        self.details['prepare_env'] = {}
        self.details['orchestrator'] = {}
        self.details['vnf'] = {}
        self.details['test_vnf'] = {}
        self.images = {}
        try:
            self.tenant_name = CONST.__getattribute__(
                'vnf_{}_tenant_name'.format(self.case_name))
            self.tenant_description = CONST.__getattribute__(
                'vnf_{}_tenant_description'.format(self.case_name))
        except Exception:
            # raise Exception("Unknown VNF case=" + self.case_name)
            self.logger.error("Unknown VNF case={}".format(self.case_name))

        try:
            self.images = CONST.__getattribute__(
                'vnf_{}_tenant_images'.format(self.case_name))
        except Exception:
            self.logger.warn("No tenant image defined for this VNF")

    def execute(self):
        self.start_time = time.time()
        # Prepare the test (Create Tenant, User, ...)
        try:
            self.logger.info("Create VNF Onboarding environment")
            self.prepare()
        except Exception:
            self.logger.error("Error during VNF Onboarding environment" +
                              "creation", exc_info=True)
            return base.TestCase.EX_TESTCASE_FAILED

        # Deploy orchestrator
        try:
            self.logger.info("Deploy orchestrator (if necessary)")
            orchestrator_ready_time = time.time()
            res_orchestrator = self.deploy_orchestrator()
            # orchestrator is not mandatory
            if res_orchestrator is not None:
                self.details['orchestrator']['status'] = (
                    res_orchestrator['status'])
                self.details['orchestrator']['result'] = (
                    res_orchestrator['result'])
                self.details['orchestrator']['duration'] = round(
                    orchestrator_ready_time - self.start_time, 1)
        except Exception:
            self.logger.warn("Problem with the Orchestrator", exc_info=True)

        # Deploy VNF
        try:
            self.logger.info("Deploy VNF " + self.case_name)
            res_deploy_vnf = self.deploy_vnf()
            vnf_ready_time = time.time()
            self.details['vnf']['status'] = res_deploy_vnf['status']
            self.details['vnf']['result'] = res_deploy_vnf['result']
            self.details['vnf']['duration'] = round(
                vnf_ready_time - orchestrator_ready_time, 1)
        except Exception:
            self.logger.error("Error during VNF deployment", exc_info=True)
            return base.TestCase.EX_TESTCASE_FAILED

        # Test VNF
        try:
            self.logger.info("Test VNF")
            res_test_vnf = self.test_vnf()
            test_vnf_done_time = time.time()
            self.details['test_vnf']['status'] = res_test_vnf['status']
            self.details['test_vnf']['result'] = res_test_vnf['result']
            self.details['test_vnf']['duration'] = round(
                test_vnf_done_time - vnf_ready_time, 1)
        except Exception:
            self.logger.error("Error when running VNF tests", exc_info=True)
            return base.TestCase.EX_TESTCASE_FAILED

        # Clean the system
        self.clean()
        self.stop_time = time.time()

        exit_code = self.parse_results()
        self.log_results()
        return exit_code

    # prepare state could consist in the creation of the resources
    # a dedicated user
    # a dedicated tenant
    # dedicated images
    def prepare(self):
        self.creds = os_utils.get_credentials()
        self.keystone_client = os_utils.get_keystone_client()

        self.logger.info("Prepare OpenStack plateform(create tenant and user)")
        admin_user_id = os_utils.get_user_id(self.keystone_client,
                                             self.creds['username'])
        if not admin_user_id:
            self.step_failure("Failed to get id of {0}".format(
                self.creds['username']))

        tenant_id = os_utils.get_tenant_id(self.keystone_client,
                                           self.tenant_name)
        if not tenant_id:
            tenant_id = os_utils.create_tenant(self.keystone_client,
                                               self.tenant_name,
                                               self.tenant_description)
            if not tenant_id:
                self.step_failure("Failed to get or create {0} tenant".format(
                    self.tenant_name))
            roles_name = ["admin", "Admin"]
            role_id = ''
            for role_name in roles_name:
                if not role_id:
                    role_id = os_utils.get_role_id(self.keystone_client,
                                                   role_name)

            if not role_id:
                self.step_failure("Failed to get id for {0} role".format(
                    role_name))

            if not os_utils.add_role_user(self.keystone_client, admin_user_id,
                                          role_id, tenant_id):
                self.step_failure("Failed to add {0} on tenant".format(
                    self.creds['username']))

        user_id = os_utils.get_or_create_user(self.keystone_client,
                                              self.tenant_name,
                                              self.tenant_name,
                                              tenant_id)
        if not user_id:
            self.step_failure("Failed to get or create {0} user".format(
                              self.tenant_name))

        os_utils.add_role_user(self.keystone_client, user_id,
                               role_id, tenant_id)

        self.logger.info("Update OpenStack creds informations")
        self.admin_creds = self.creds.copy()
        self.admin_creds.update({
            "tenant": self.tenant_name
        })
        self.neutron_client = os_utils.get_neutron_client(self.admin_creds)
        self.nova_client = os_utils.get_nova_client(self.admin_creds)
        self.creds.update({
            "tenant": self.tenant_name,
            "username": self.tenant_name,
            "password": self.tenant_name,
        })

    # orchestrator is not mandatory to deploy and test VNF
    def deploy_orchestrator(self, **kwargs):
        pass

    # TODO see how to use built-in exception from releng module
    def deploy_vnf(self):
        self.logger.error("VNF must be deployed")
        raise Exception("VNF not deployed")

    def test_vnf(self):
        self.logger.error("VNF must be tested")
        raise Exception("VNF not tested")

    # clean before openstack clean run
    def clean(self):
        self.logger.info("test cleaning")

    def parse_results(self):
        exit_code = self.EX_OK
        self.result = "PASS"
        self.logger.info(self.details)
        # The 2 VNF steps must be OK to get a PASS result
        if (self.details['vnf']['status'] is not "PASS" or
                self.details['test_vnf']['status'] is not "PASS"):
            exit_code = self.EX_RUN_ERROR
            self.result = "FAIL"
        return exit_code

    def log_results(self):
        ft_utils.logger_test_results(self.project_name,
                                     self.case_name,
                                     self.result,
                                     self.details)

    def step_failure(self, error_msg):
        part = inspect.stack()[1][3]
        self.logger.error("Step {0} failed: {1}".format(part, error_msg))
        try:
            step_name = self.details_step_mapping[part]
            part_info = self.details[step_name]
        except KeyError:
            self.details[part] = {}
            part_info = self.details[part]
        part_info['status'] = 'FAIL'
        part_info['result'] = error_msg
        raise Exception(error_msg)
