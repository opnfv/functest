#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the parent class of all VNF TestCases."""

import logging
import time
import uuid

import functest.core.testcase as base
from functest.utils.constants import CONST
from snaps.config.user import UserConfig
from snaps.config.project import ProjectConfig
from snaps.openstack.create_user import OpenStackUser
from snaps.openstack.create_project import OpenStackProject
from snaps.openstack.tests import openstack_tests

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
        self.tenant_name = CONST.__getattribute__(
            'vnf_{}_tenant_name'.format(self.case_name))
        self.snaps_creds = {}
        self.created_object = []
        self.os_project = None

    def run(self, **kwargs):
        """
        Run of the VNF test case:

            * Deploy an orchestrator if needed (e.g. heat, cloudify, ONAP,...),
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
            if (self.deploy_orchestrator() and
                    self.deploy_vnf() and
                    self.test_vnf()):
                self.stop_time = time.time()
                # Calculation with different weight depending on the steps TODO
                self.result = 100
                return base.TestCase.EX_OK
            else:
                self.result = 0
                self.stop_time = time.time()
                return base.TestCase.EX_TESTCASE_FAILED
        except Exception:  # pylint: disable=broad-except
            self.stop_time = time.time()
            self.__logger.exception("Exception on VNF testing")
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
            tenant_description = CONST.__getattribute__(
                'vnf_{}_tenant_description'.format(self.case_name))
            self.__logger.info("Prepare VNF: %s, description: %s",
                               self.tenant_name, tenant_description)
            snaps_creds = openstack_tests.get_credentials(
                os_env_file=CONST.__getattribute__('creds'))

            project_creator = OpenStackProject(
                snaps_creds,
                ProjectConfig(
                    name=self.tenant_name,
                    description=tenant_description
                ))
            project_creator.create()
            self.created_object.append(project_creator)
            self.os_project = project_creator

            user_creator = OpenStackUser(
                snaps_creds,
                UserConfig(
                    name=self.tenant_name,
                    password=str(uuid.uuid4()),
                    roles={'admin': self.tenant_name}))

            user_creator.create()
            self.created_object.append(user_creator)

            self.snaps_creds = user_creator.get_os_creds(self.tenant_name)

            return base.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Exception raised during VNF preparation")
            raise VnfPreparationException

    def deploy_orchestrator(self):
        """
        Deploy an orchestrator (optional).

        If this method is overriden then raise orchestratorDeploymentException
        if error during orchestrator deployment
        """
        self.__logger.info("Deploy orchestrator (if necessary)")
        return True

    def deploy_vnf(self):
        """
        Deploy the VNF

        This function MUST be implemented by vnf test cases.
        The details section MAY be updated in the vnf test cases.

        The deployment can be executed via a specific orchestrator
        or using build-in orchestrators such as heat, OpenBaton, cloudify,
        juju, onap, ...

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
        self.__logger.info('Removing the VNF resources ..')
        for creator in reversed(self.created_object):
            try:
                creator.clean()
            except Exception as exc:  # pylint: disable=broad-except
                self.__logger.error('Unexpected error cleaning - %s', exc)
