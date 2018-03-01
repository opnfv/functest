#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the parent class of all VNF TestCases."""

import logging
import uuid

from snaps.config.user import UserConfig
from snaps.config.project import ProjectConfig
from snaps.openstack.create_user import OpenStackUser
from snaps.openstack.create_project import OpenStackProject
from snaps.openstack.utils import keystone_utils
from snaps.openstack.tests import openstack_tests

from xtesting.core import vnf
from functest.utils import constants

__author__ = ("Morgan Richomme <morgan.richomme@orange.com>, "
              "Valentin Boucher <valentin.boucher@orange.com>")


class VnfPreparationException(vnf.VnfPreparationException):
    """Raise when VNF preparation cannot be executed."""


class OrchestratorDeploymentException(vnf.OrchestratorDeploymentException):
    """Raise when orchestrator cannot be deployed."""


class VnfDeploymentException(vnf.VnfDeploymentException):
    """Raise when VNF cannot be deployed."""


class VnfTestException(vnf.VnfTestException):
    """Raise when VNF cannot be tested."""


class VnfOnBoarding(vnf.VnfOnBoarding):
    # pylint: disable=too-many-instance-attributes
    """Base model for OpenStack VNF test cases."""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        super(VnfOnBoarding, self).__init__(**kwargs)
        self.uuid = uuid.uuid4()
        self.user_name = "{}-{}".format(self.case_name, self.uuid)
        self.tenant_name = "{}-{}".format(self.case_name, self.uuid)
        self.snaps_creds = {}
        self.created_object = []
        self.os_project = None
        self.tenant_description = "Created by OPNFV Functest: {}".format(
            self.case_name)

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
            self.__logger.info(
                "Prepare VNF: %s, description: %s", self.case_name,
                self.tenant_description)
            snaps_creds = openstack_tests.get_credentials(
                os_env_file=constants.ENV_FILE)

            self.os_project = OpenStackProject(
                snaps_creds,
                ProjectConfig(
                    name=self.tenant_name,
                    description=self.tenant_description,
                    domain=snaps_creds.project_domain_name
                ))
            self.os_project.create()
            self.created_object.append(self.os_project)

            snaps_creds.project_domain_id = \
                self.os_project.get_project().domain_id
            snaps_creds.user_domain_id = \
                self.os_project.get_project().domain_id

            for role in ['admin', 'Admin']:
                if keystone_utils.get_role_by_name(
                        keystone_utils.keystone_client(snaps_creds), role):
                    admin_role = role
                    break

            user_creator = OpenStackUser(
                snaps_creds,
                UserConfig(
                    name=self.user_name,
                    password=str(uuid.uuid4()),
                    project_name=self.tenant_name,
                    domain_name=snaps_creds.user_domain_name,
                    roles={admin_role: self.tenant_name}))
            user_creator.create()
            self.created_object.append(user_creator)
            self.snaps_creds = user_creator.get_os_creds(self.tenant_name)

            return vnf.VnfOnBoarding.EX_OK
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
