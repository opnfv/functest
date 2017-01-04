#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import os
import time

import inspect

import functest.utils.functest_constants as ft_constants
import functest.utils.functest_logger as ft_logger
import functest.utils.openstack_utils as os_utils
import functest.utils.functest_utils as ft_utils
import testcase_base as base


class VnfOnBoardingBase(base.TestcaseBase):

    EX_OK = os.EX_OK
    EX_RUN_ERROR = os.EX_SOFTWARE
    EX_PUSH_TO_DB_ERROR = os.EX_SOFTWARE - 1

    logger = ft_logger.Logger(__name__).getLogger()

    def __init__(self, project='functest', case='', repo='', cmd=''):
        super(VnfOnBoardingBase, self).__init__()
        self.repo = repo
        self.project_name = project
        self.case_name = case
        self.cmd = cmd
        self.details = {}
        self.data_dir = ft_constants.FUNCTEST_DATA_DIR
        self.details['orchestrator'] = {}
        self.details['vnf'] = {}
        self.details['test_vnf'] = {}

        try:
            self.tenant_name = self.case_name
            self.tenant_description = (
                ft_constants.getVnfTenantDescription(self.case_name))
            self.images = ft_constants.getVnfImages(self.case_name)
        except:
            raise Exception("Unknown VNF")

    def run(self, **kwargs):
        self.logger.error("Run must be implemented")
        return self.EX_RUN_ERROR

    def execute(self):
        self.start_time = time.time()
        # Prepare the test (Create Tenant, User, ...)
        self.logger.info("Create VNF Onboarding environment")
        self.prepare()

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
        except:
            self.logger.warn("Problem with the Orchestrator")

        # Deploy VNF
        try:
            self.logger.info("Deploy VNF " + self.case_name)
            res_deploy_vnf = self.deploy_vnf()
            vnf_ready_time = time.time()
            self.details['vnf']['status'] = res_deploy_vnf['status']
            self.details['vnf']['result'] = res_deploy_vnf['result']
            self.details['vnf']['duration'] = round(
                vnf_ready_time - orchestrator_ready_time, 1)
        except:
            raise Exception("Error during VNF deployment")

        # Test VNF
        try:
            self.logger.info("Test VNF")
            res_test_vnf = self.test_vnf()
            test_vnf_done_time = time.time()
            self.details['test_vnf']['status'] = res_test_vnf['status']
            self.details['test_vnf']['result'] = res_test_vnf['result']
            self.details['test_vnf']['duration'] = round(
                test_vnf_done_time - vnf_ready_time, 1)
        except:
            raise Exception("Error when running VNF tests")

        # Clean the system
        self.clean()
        self.stop_time = time.time()

        exit_code = self.parse_results()
        self.log_results()
        return exit_code

    # prepare state could consist in the creation of the resources
    # a dedicated user
    # a dedictaed tenant
    # dedicated images
    def prepare(self):
        self.creds = os_utils.get_credentials()
        self.keystone_client = os_utils.get_keystone_client()

        self.logger.info("Prepare OpenStack plateform(create tenant and user)")
        user_id = os_utils.get_user_id(self.keystone_client,
                                       self.creds['username'])
        if user_id == '':
            self.step_failure("Failed to get id of " +
                              self.creds['username'])

        tenant_id = os_utils.create_tenant(
            self.keystone_client, self.tenant_name, self.tenant_description)
        if not tenant_id:
            self.step_failure("Failed to create " +
                              self.tenant_name + " tenant")

        roles_name = ["admin", "Admin"]
        role_id = ''
        for role_name in roles_name:
            if role_id == '':
                role_id = os_utils.get_role_id(self.keystone_client, role_name)

        if role_id == '':
            self.logger.error("Failed to get id for %s role" % role_name)

        if not os_utils.add_role_user(self.keystone_client, user_id,
                                      role_id, tenant_id):
            self.logger.error("Failed to add %s on tenant" %
                              self.creds['username'])

        user_id = os_utils.create_user(self.keystone_client,
                                       self.tenant_name,
                                       self.tenant_name,
                                       None,
                                       tenant_id)
        if not user_id:
            self.logger.error("Failed to create %s user" % self.tenant_name)

        self.logger.info("Update OpenStack creds informations")
        self.creds.update({
            "username": self.tenant_name,
            "password": self.tenant_name,
            "tenant": self.tenant_name,
        })
        self.glance_client = os_utils.get_glance_client(self.creds)
        self.neutron_client = os_utils.get_neutron_client(self.creds)
        self.nova_client = os_utils.get_nova_client(self.creds)

        self.logger.info("Upload some OS images if it doesn't exist")

        temp_dir = os.path.join(self.data_dir, "tmp/")
        for image_name, image_url in self.images.iteritems():
            image_id = os_utils.get_image_id(self.glance_client, image_name)

            if image_id == '':
                self.logger.info("""%s image doesn't exist on glance repository. Try
                downloading this image and upload on glance !""" % image_name)
                image_id = os_utils.download_and_add_image_on_glance(
                    self.glance_client, image_name, image_url, temp_dir)

            if image_id == '':
                self.step_failure(
                    "Failed to find or upload required OS "
                    "image for this deployment")

        self.logger.info("Update security group quota for this tenant")

        if not os_utils.update_sg_quota(self.neutron_client,
                                        tenant_id, 50, 100):
            self.step_failure("Failed to update security group quota" +
                              " for tenant " + self.tenant_name)

    # orchestrator is not mandatory to dpeloy and test VNF
    def deploy_orchestrator(self, **kwargs):
        pass

    # TODO see how to use built-in exception from releng module
    def deploy_vnf(self):
        self.logger.error("VNF must be deployed")
        raise Exception("VNF not deployed")

    def test_vnf(self):
        self.logger.error("VNF must be tested")
        raise Exception("VNF not tested")

    def clean(self):
        self.logger.info("test cleaning")

        self.logger.info("Removing %s tenant .." % self.tenant_name)
        tenant_id = os_utils.get_tenant_id(self.keystone_client,
                                           self.tenant_name)
        if tenant_id == '':
            self.logger.error("Error : Failed to get id of %s tenant" %
                              self.tenant_name)
        else:
            if not os_utils.delete_tenant(self.keystone_client, tenant_id):
                self.logger.error("Error : Failed to remove %s tenant" %
                                  self.tenant_name)

        self.logger.info("Removing %s user .." % self.tenant_name)
        user_id = os_utils.get_user_id(
            self.keystone_client, self.tenant_name)
        if user_id == '':
            self.logger.error("Error : Failed to get id of %s user" %
                              self.tenant_name)
        else:
            if not os_utils.delete_user(self.keystone_client, user_id):
                self.logger.error("Error : Failed to remove %s user" %
                                  self.tenant_name)

    def parse_results(self):
        exit_code = self.EX_OK
        self.criteria = "PASS"
        self.logger.info(self.details)
        # The 2 VNF steps must be OK to get a PASS result
        if (self.details['vnf']['status'] is not "PASS" or
                self.details['test_vnf']['status'] is not "PASS"):
            exit_code = self.EX_RUN_ERROR
            self.criteria = "FAIL"
        return exit_code

    def log_results(self):
        ft_utils.logger_test_results(self.project_name,
                                     self.case_name,
                                     self.criteria,
                                     self.details)

    def step_failure(self, error_msg):
        part = inspect.stack()[1][3]
        self.details[part]['status'] = 'FAIL'
        self.details[part]['result'] = error_msg
        raise Exception(error_msg)
