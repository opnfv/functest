#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import os
import time

import keystoneclient.v2_0.client as ksclient
from neutronclient.v2_0 import client as ntclient

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
        self.details['orchestrator'] = {}
        self.details['vnf'] = {}
        self.details['test_vnf'] = {}

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
    # a dedicated network
    # dedicated images
    def prepare(self):
        ks_creds = os_utils.get_credentials("keystone")
        nv_creds = os_utils.get_credentials("nova")
        nt_creds = os_utils.get_credentials("neutron")

        self.logger.info("Prepare OpenStack plateform"
                         "(create tenant and user)")
        keystone = ksclient.Client(**ks_creds)

        user_id = os_utils.get_user_id(keystone, ks_creds['username'])
        if user_id == '':
            raise Exception("Keystone error to get id")

        try:
            vnf_tenant_name = self.case_name
            vnf_tenant_description = (
                ft_constants.getVnfTenantDescription(self.case_name))
            vnf_image = ft_constants.getVnfImage(self.case_name)
        except:
            raise Exception("Unknown VNF")

        # Create Tenant
        tenant_id = os_utils.create_tenant(
            keystone, vnf_tenant_name, vnf_tenant_description)
        if not tenant_id:
            raise Exception("Tenant creation Error")

        roles_name = ["admin", "Admin"]
        role_id = ''
        for role_name in roles_name:
            if role_id == '':
                role_id = os_utils.get_role_id(keystone, role_name)

        if role_id == '':
            self.logger.error("Error : Failed to get id for %s role" %
                              role_name)

        if not os_utils.add_role_user(keystone, user_id, role_id, tenant_id):
            self.logger.error("Error : Failed to add %s on tenant" %
                              ks_creds['username'])

        # Create User
        user_id = os_utils.create_user(
            keystone, vnf_tenant_name, vnf_tenant_name, None, tenant_id)
        if not user_id:
            self.logger.error("Error : Failed to create %s user" %
                              vnf_tenant_name)

        self.logger.info("Update OpenStack creds informations")
        ks_creds.update({
            "username": vnf_tenant_name,
            "password": vnf_tenant_name,
            "tenant_name": vnf_tenant_name,
        })

        nt_creds.update({
            "tenant_name": vnf_tenant_name,
        })

        nv_creds.update({
            "project_id": vnf_tenant_name,
        })

        # Manage images
        self.logger.info("Upload some OS images if it doesn't exist")
        glance = os_utils.get_glance_client()

        # TODO for the moment we consider 1 image
        # we may imagine several ones
        vnf_images = {}
        for img in vnf_images.keys():
            image_name = vnf_images[img]['image_name']
            # image_url = vnf_images[img]['image_url']

            image_id = os_utils.get_image_id(glance, image_name)

            if image_id == '':
                self.logger.info("""%s image doesn't exist on glance
                               repository. Try downloading this image
                               and upload on glance !""" % image_name)
            # TODO function in vims to be moved in utils
            #   image_id = download_and_add_image_on_glance(
            #       glance, image_name, image_url)
            image_id = 'todo'
            if image_id == '':
                raise Exception("Failed to find or upload required images")

        self.logger.info("Update security group quota for this tenant")
        neutron = ntclient.Client(**nt_creds)
        if not os_utils.update_sg_quota(neutron, tenant_id, 50, 100):
            raise Exception("Security group error ")

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
        vnf_tenant_name = self.case_name

        ks_creds = os_utils.get_credentials("keystone")

        keystone = ksclient.Client(**ks_creds)
        self.logger.info("Removing %s tenant .." % vnf_tenant_name)
        tenant_id = os_utils.get_tenant_id(keystone, vnf_tenant_name)
        if tenant_id == '':
            self.logger.error("Error : Failed to get id of %s tenant" %
                              vnf_tenant_name)
        else:
            if not os_utils.delete_tenant(keystone, tenant_id):
                self.logger.error("Error : Failed to remove %s tenant" %
                                  vnf_tenant_name)

        self.logger.info("Removing %s user .." % vnf_tenant_name)
        user_id = os_utils.get_user_id(
            keystone, vnf_tenant_name)
        if user_id == '':
            self.logger.error("Error : Failed to get id of %s user" %
                              vnf_tenant_name)
        else:
            if not os_utils.delete_user(keystone, user_id):
                self.logger.error("Error : Failed to remove %s user" %
                                  vnf_tenant_name)

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
