#!/usr/bin/env python

# Copyright (c) 2017 Cable Television Laboratories, Inc. and others.
#
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import logging

from snaps.openstack.tests.create_flavor_tests import (
    CreateFlavorTests)
from snaps.openstack.tests.create_image_tests import (
    CreateImageSuccessTests, CreateImageNegativeTests,
    CreateMultiPartImageTests)
from snaps.openstack.tests.create_instance_tests import (
    CreateInstanceSingleNetworkTests, CreateInstanceOnComputeHost,
    CreateInstanceSimpleTests, InstanceSecurityGroupTests,
    CreateInstancePortManipulationTests, SimpleHealthCheck,
    CreateInstanceFromThreePartImage, CreateInstanceTwoNetTests)
from snaps.openstack.tests.create_keypairs_tests import (
    CreateKeypairsTests, CreateKeypairsCleanupTests)
from snaps.openstack.tests.create_network_tests import (
    CreateNetworkSuccessTests)
from snaps.openstack.tests.create_project_tests import (
    CreateProjectSuccessTests, CreateProjectUserTests)
from snaps.openstack.tests.create_router_tests import (
    CreateRouterSuccessTests, CreateRouterNegativeTests)
from snaps.openstack.tests.create_security_group_tests import (
    CreateSecurityGroupTests)
from snaps.openstack.tests.create_stack_tests import (
    CreateStackSuccessTests, CreateStackNegativeTests)
from snaps.openstack.tests.create_user_tests import (
    CreateUserSuccessTests)
from snaps.openstack.tests.os_source_file_test import (
    OSComponentTestCase, OSIntegrationTestCase)
from snaps.openstack.utils.tests.glance_utils_tests import (
    GlanceSmokeTests, GlanceUtilsTests)
from snaps.openstack.utils.tests.heat_utils_tests import HeatSmokeTests
from snaps.openstack.utils.tests.keystone_utils_tests import (
    KeystoneSmokeTests, KeystoneUtilsTests)
from snaps.openstack.utils.tests.neutron_utils_tests import (
    NeutronSmokeTests, NeutronUtilsNetworkTests, NeutronUtilsSubnetTests,
    NeutronUtilsRouterTests, NeutronUtilsSecurityGroupTests,
    NeutronUtilsFloatingIpTests)
from snaps.openstack.utils.tests.nova_utils_tests import (
    NovaSmokeTests, NovaUtilsKeypairTests, NovaUtilsFlavorTests,
    NovaUtilsInstanceTests)
from snaps.provisioning.tests.ansible_utils_tests import (
    AnsibleProvisioningTests)


def add_openstack_client_tests(suite, os_creds, ext_net_name,
                               use_keystone=True, log_level=logging.INFO):
    """
    Adds tests written to exercise OpenStack client retrieval
    :param suite: the unittest.TestSuite object to which to add the tests
    :param os_creds: and instance of OSCreds that holds the credentials
                     required by OpenStack
    :param ext_net_name: the name of an external network on the cloud under
                         test
    :param use_keystone: when True, tests requiring direct access to Keystone
                         are added as these need to be running on a host that
                         has access to the cloud's private network
    :param log_level: the logging level
    :return: None as the tests will be adding to the 'suite' parameter object
    """
    # Basic connection tests
    suite.addTest(
        OSComponentTestCase.parameterize(
            GlanceSmokeTests, os_creds=os_creds, ext_net_name=ext_net_name,
            log_level=log_level))

    if use_keystone:
        suite.addTest(
            OSComponentTestCase.parameterize(
                KeystoneSmokeTests, os_creds=os_creds,
                ext_net_name=ext_net_name, log_level=log_level))

    suite.addTest(
        OSComponentTestCase.parameterize(
            NeutronSmokeTests, os_creds=os_creds, ext_net_name=ext_net_name,
            log_level=log_level))
    suite.addTest(
        OSComponentTestCase.parameterize(
            NovaSmokeTests, os_creds=os_creds, ext_net_name=ext_net_name,
            log_level=log_level))
    suite.addTest(
        OSComponentTestCase.parameterize(
            HeatSmokeTests, os_creds=os_creds, ext_net_name=ext_net_name,
            log_level=log_level))


def add_openstack_api_tests(suite, os_creds, ext_net_name, use_keystone=True,
                            image_metadata=None, log_level=logging.INFO):
    """
    Adds tests written to exercise all existing OpenStack APIs
    :param suite: the unittest.TestSuite object to which to add the tests
    :param os_creds: Instance of OSCreds that holds the credentials
                     required by OpenStack
    :param ext_net_name: the name of an external network on the cloud under
                         test
    :param use_keystone: when True, tests requiring direct access to Keystone
                         are added as these need to be running on a host that
                         has access to the cloud's private network
    :param image_metadata: dict() object containing metadata for creating an
                           image with custom config
                           (see YAML files in examples/image-metadata)
    :param log_level: the logging level
    :return: None as the tests will be adding to the 'suite' parameter object
    """
    # Tests the OpenStack API calls
    if use_keystone:
        suite.addTest(OSComponentTestCase.parameterize(
            KeystoneUtilsTests, os_creds=os_creds, ext_net_name=ext_net_name,
            log_level=log_level))
        suite.addTest(OSComponentTestCase.parameterize(
            CreateUserSuccessTests, os_creds=os_creds,
            ext_net_name=ext_net_name, log_level=log_level))
        suite.addTest(OSComponentTestCase.parameterize(
            CreateProjectSuccessTests, os_creds=os_creds,
            ext_net_name=ext_net_name, log_level=log_level))
        suite.addTest(OSComponentTestCase.parameterize(
            CreateProjectUserTests, os_creds=os_creds,
            ext_net_name=ext_net_name, log_level=log_level))

    suite.addTest(OSComponentTestCase.parameterize(
        GlanceUtilsTests, os_creds=os_creds, ext_net_name=ext_net_name,
        image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSComponentTestCase.parameterize(
        NeutronUtilsNetworkTests, os_creds=os_creds, ext_net_name=ext_net_name,
        log_level=log_level))
    suite.addTest(OSComponentTestCase.parameterize(
        NeutronUtilsSubnetTests, os_creds=os_creds, ext_net_name=ext_net_name,
        log_level=log_level))
    suite.addTest(OSComponentTestCase.parameterize(
        NeutronUtilsRouterTests, os_creds=os_creds, ext_net_name=ext_net_name,
        log_level=log_level))
    suite.addTest(OSComponentTestCase.parameterize(
        NeutronUtilsSecurityGroupTests, os_creds=os_creds,
        ext_net_name=ext_net_name, log_level=log_level))
    suite.addTest(OSComponentTestCase.parameterize(
        NeutronUtilsFloatingIpTests, os_creds=os_creds,
        ext_net_name=ext_net_name, log_level=log_level))
    suite.addTest(OSComponentTestCase.parameterize(
        NovaUtilsKeypairTests, os_creds=os_creds, ext_net_name=ext_net_name,
        log_level=log_level))
    suite.addTest(OSComponentTestCase.parameterize(
        NovaUtilsFlavorTests, os_creds=os_creds, ext_net_name=ext_net_name,
        log_level=log_level))
    suite.addTest(OSComponentTestCase.parameterize(
        NovaUtilsInstanceTests, os_creds=os_creds, ext_net_name=ext_net_name,
        log_level=log_level, image_metadata=image_metadata))
    suite.addTest(OSComponentTestCase.parameterize(
        CreateFlavorTests, os_creds=os_creds, ext_net_name=ext_net_name,
        log_level=log_level))


def add_openstack_integration_tests(suite, os_creds, ext_net_name,
                                    use_keystone=True, flavor_metadata=None,
                                    image_metadata=None, use_floating_ips=True,
                                    log_level=logging.INFO):
    """
    Adds tests written to exercise all long-running OpenStack integration tests
    meaning they will be creating VM instances and potentially performing some
    SSH functions through floatingIPs
    :param suite: the unittest.TestSuite object to which to add the tests
    :param os_creds: and instance of OSCreds that holds the credentials
                     required by OpenStack
    :param ext_net_name: the name of an external network on the cloud under
                         test
    :param use_keystone: when True, tests requiring direct access to Keystone
                         are added as these need to be running on a host that
                         has access to the cloud's private network
    :param image_metadata: dict() object containing metadata for creating an
                           image with custom config
                           (see YAML files in examples/image-metadata)
    :param flavor_metadata: dict() object containing the metadata required by
                            your flavor based on your configuration:
                            (i.e. {'hw:mem_page_size': 'large'})
    :param use_floating_ips: when true, all tests requiring Floating IPs will
                             be added to the suite
    :param log_level: the logging level
    :return: None as the tests will be adding to the 'suite' parameter object
    """
    # Tests the OpenStack API calls via a creator. If use_keystone, objects
    # will be created with a custom user and project

    # Creator Object tests
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateSecurityGroupTests, os_creds=os_creds, ext_net_name=ext_net_name,
        use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateImageSuccessTests, os_creds=os_creds, ext_net_name=ext_net_name,
        use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateImageNegativeTests, os_creds=os_creds, ext_net_name=ext_net_name,
        use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateMultiPartImageTests, os_creds=os_creds,
        ext_net_name=ext_net_name, use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateKeypairsTests, os_creds=os_creds, ext_net_name=ext_net_name,
        use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateKeypairsCleanupTests, os_creds=os_creds,
        ext_net_name=ext_net_name,
        use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateNetworkSuccessTests, os_creds=os_creds,
        ext_net_name=ext_net_name, use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateRouterSuccessTests, os_creds=os_creds, ext_net_name=ext_net_name,
        use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateRouterNegativeTests, os_creds=os_creds,
        ext_net_name=ext_net_name, use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))

    # VM Instances
    suite.addTest(OSIntegrationTestCase.parameterize(
        SimpleHealthCheck, os_creds=os_creds, ext_net_name=ext_net_name,
        use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateInstanceTwoNetTests, os_creds=os_creds,
        ext_net_name=ext_net_name, use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateInstanceSimpleTests, os_creds=os_creds,
        ext_net_name=ext_net_name, use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateInstancePortManipulationTests, os_creds=os_creds,
        ext_net_name=ext_net_name, use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        InstanceSecurityGroupTests, os_creds=os_creds,
        ext_net_name=ext_net_name, use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateInstanceOnComputeHost, os_creds=os_creds,
        ext_net_name=ext_net_name, use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateInstanceFromThreePartImage, os_creds=os_creds,
        ext_net_name=ext_net_name, use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateStackSuccessTests, os_creds=os_creds, ext_net_name=ext_net_name,
        use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))
    suite.addTest(OSIntegrationTestCase.parameterize(
        CreateStackNegativeTests, os_creds=os_creds, ext_net_name=ext_net_name,
        use_keystone=use_keystone,
        flavor_metadata=flavor_metadata, image_metadata=image_metadata,
        log_level=log_level))

    if use_floating_ips:
        suite.addTest(OSIntegrationTestCase.parameterize(
            CreateInstanceSingleNetworkTests, os_creds=os_creds,
            ext_net_name=ext_net_name, use_keystone=use_keystone,
            flavor_metadata=flavor_metadata, image_metadata=image_metadata,
            log_level=log_level))
        suite.addTest(OSIntegrationTestCase.parameterize(
            AnsibleProvisioningTests, os_creds=os_creds,
            ext_net_name=ext_net_name, use_keystone=use_keystone,
            flavor_metadata=flavor_metadata, image_metadata=image_metadata,
            log_level=log_level))
