#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import time

import functest.core.testcase as base
from functest.utils.constants import CONST
import functest.utils.openstack_utils as os_utils

__author__ = ("Morgan Richomme <morgan.richomme@orange.com>, "
              "Valentin Boucher <valentin.boucher@orange.com>")


class VnfPreparationException(Exception):
    """Raise when VNF preparation cannot be executed."""


class OrchestratorDeploymentException(Exception):
    """Raise when orchestrator cannot be deployed."""


class VnfDeploymentException(Exception):
    """Raise when VNF cannot be deployed."""


class VnfTestException(Exception):
    """Raise when VNF cannot be tested."""


class VnfOnBoarding(base.TestCase):
    """Base model for VNF test cases."""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        super(VnfOnBoarding, self).__init__(**kwargs)
        self.result_dir = CONST.__getattribute__('dir_results')
        self.tenant_created = False
        self.user_created = False
        self.keystone_client = ''
        self.admin_creds = {}
        self.creds = {}
        self.tenant_name = CONST.__getattribute__(
            'vnf_{}_tenant_name'.format(self.case_name))
        self.tenant_description = CONST.__getattribute__(
            'vnf_{}_tenant_description'.format(self.case_name))

    def run(self, **kwargs):
        """
        Run of the VNF test case:

            * Deploy an orchestrator if needed (e.g. heat, cloudify, ONAP),
            * Deploy the VNF,
            * Perform tests on the VNF

          A VNF test case is successfull when the 3 steps are PASS
          If one of the step is FAIL, the test case is FAIL

          Returns:
            TestCase.EX_OK if result is 'PASS'.
            TestCase.EX_TESTCASE_FAILED otherwise.
        """
        self.start_time = time.time()

        try:
            self.prepare()
            res_deploy_orchestrator = self.deploy_orchestrator()
            res_deploy_vnf = self.deploy_vnf()
            res_test_vnf = self.test_vnf()
            self.stop_time = time.time()
            if (res_deploy_orchestrator and
                    res_deploy_vnf and
                    res_test_vnf):
                # Calculation with different weight depending on the steps TODO
                self.result = 100
                return base.TestCase.EX_OK
            else:
                self.result = 0
                return base.TestCase.EX_TESTCASE_FAILED
        except Exception as err:
            self.__logger.exception("Exception on VNF testing"
                                    ":%s, %s", err.__class__.__name__, err)
            return base.TestCase.EX_TESTCASE_FAILED

    def prepare(self):
        """
        Prepare the environment for VNF testing:

            * Creation of a user,
            * Creation of a tenant,
            * Allocation admin role to the user on this tenant

        Returns base.TestCase.EX_OK if preparation is successfull

        Raise VnfPreparationException in case of problem
        """
        try:
            self.__logger.info("Prepare VNF: %s", self.tenant_name)
            self.__logger.info("Description: %s", self.tenant_description)
            self.admin_creds = os_utils.get_credentials()
            self.keystone_client = os_utils.get_keystone_client()
            self.tenant_created = os_utils.get_or_create_tenant_for_vnf(
                self.keystone_client,
                self.tenant_name,
                self.tenant_description)
            self.user_created = os_utils.get_or_create_user_for_vnf(
                self.keystone_client,
                self.tenant_name)
            self.creds = self.admin_creds.copy()
            self.creds.update({
                "tenant": self.tenant_name,
                "username": self.tenant_name,
                "password": self.tenant_name
                })
            return base.TestCase.EX_OK
        except Exception as err:
            self.__logger.exception("Exception raised during VNF preparation"
                                    ":%s, %s", err.__class__.__name__, err)
            raise VnfPreparationException

    def deploy_orchestrator(self):
        """
        Deploy an orchestrator (optional).

        If function overwritten
        raise orchestratorDeploymentException if error during orchestrator
        deployment
        """
        self.__logger.info("Deploy orchestrator (if necessary)")
        return True

    def deploy_vnf(self):
        """
        Deploy the VNF

        This function MUST be implemented by vnf test cases.
        The details section MAY be updated in the vnf test cases.

        The deployment can be executed via a specific orchestrator
        or using nuild-in orchestrators such as:

            * heat, openbaton, cloudify (available on all scenario),
            * open-o (on open-o scenarios)

        Returns:
            True if the VNF is properly deployed
            False if the VNF is not deployed

        Raise VnfDeploymentException if error during VNF deployment
        """
        self.__logger.error("VNF must be deployed")
        raise VnfDeploymentException

    def test_vnf(self):
        """
        Test the VNF

        This function MUST be implemented by vnf test cases.
        The details section MAY be updated in the vnf test cases.

        Once a VNF is deployed, it is assumed that specific test suite can be
        run to validate the VNF.
        Please note that the same test suite can be used on several test case
        (e.g. clearwater test suite can be used whatever the orchestrator used
        for the deployment)

        Returns:
            True if VNF tests are PASS
            False if test suite is FAIL

        Raise VnfTestException if error during VNF test
        """
        self.__logger.error("VNF must be tested")
        raise VnfTestException

    def clean(self):
        """
        Clean VNF test case.

        It is up to the test providers to delete resources used for the tests.
        By default we clean:

            * the user,
            * the tenant
        """
        self.__logger.info("test cleaning")
        if self.tenant_created:
            os_utils.delete_tenant(self.keystone_client, self.tenant_name)
        if self.user_created:
            os_utils.delete_user(self.keystone_client, self.tenant_name)
