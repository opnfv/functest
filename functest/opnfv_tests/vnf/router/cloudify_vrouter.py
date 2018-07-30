#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

"""vrouter testcase implementation."""

import logging
import os
import time

from cloudify_rest_client.executions import Execution
import pkg_resources
import scp

from functest.core import cloudify
from functest.opnfv_tests.vnf.router import vrouter_base
from functest.opnfv_tests.vnf.router.utilvnf import Utilvnf
from functest.utils import config
from functest.utils import functest_utils


__author__ = "Shuya Nakama <shuya.nakama@okinawaopenlabs.org>"


class CloudifyVrouter(cloudify.Cloudify):
    # pylint: disable=too-many-instance-attributes
    """vrouter testcase deployed with Cloudify Orchestrator."""

    __logger = logging.getLogger(__name__)

    filename_alt = '/home/opnfv/functest/images/vyos-1.1.7.img'

    flavor_alt_ram = 2048
    flavor_alt_vcpus = 1
    flavor_alt_disk = 50

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "vyos_vrouter"
        super(CloudifyVrouter, self).__init__(**kwargs)

        # Retrieve the configuration
        try:
            self.config = getattr(
                config.CONF, 'vnf_{}_config'.format(self.case_name))
        except Exception:
            raise Exception("VNF config file not found")

        self.case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/router')
        config_file = os.path.join(self.case_dir, self.config)
        self.orchestrator = dict(
            requirements=functest_utils.get_parameter_from_yaml(
                "orchestrator.requirements", config_file),
        )
        self.details['orchestrator'] = dict(
            name=functest_utils.get_parameter_from_yaml(
                "orchestrator.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "orchestrator.version", config_file),
            status='ERROR',
            result=''
        )
        self.__logger.debug("Orchestrator configuration %s", self.orchestrator)
        self.__logger.debug("name = %s", __name__)
        self.vnf = dict(
            descriptor=functest_utils.get_parameter_from_yaml(
                "vnf.descriptor", config_file),
            inputs=functest_utils.get_parameter_from_yaml(
                "vnf.inputs", config_file),
            requirements=functest_utils.get_parameter_from_yaml(
                "vnf.requirements", config_file)
        )
        self.details['vnf'] = dict(
            descriptor_version=self.vnf['descriptor']['version'],
            name=functest_utils.get_parameter_from_yaml(
                "vnf.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "vnf.version", config_file),
        )
        self.__logger.debug("VNF configuration: %s", self.vnf)

        self.util = Utilvnf()
        self.util.set_credentials(self.cloud)
        credentials = {"cloud": self.cloud}
        self.util_info = {"credentials": credentials,
                          "vnf_data_dir": self.util.vnf_data_dir}

        self.details['test_vnf'] = dict(
            name=functest_utils.get_parameter_from_yaml(
                "vnf_test_suite.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "vnf_test_suite.version", config_file)
        )
        self.images = functest_utils.get_parameter_from_yaml(
            "tenant_images", config_file)
        self.__logger.info("Images needed for vrouter: %s", self.images)

        self.image_alt = None
        self.flavor_alt = None

    def execute(self):
        # pylint: disable=too-many-locals,too-many-statements
        """
        Deploy Cloudify Manager.
        network, security group, fip, VM creation
        """
        # network creation
        super(CloudifyVrouter, self).execute()
        start_time = time.time()
        self.__logger.info("Put private keypair in manager")
        scpc = scp.SCPClient(self.ssh.get_transport())
        scpc.put(self.key_filename, remote_path='~/cloudify_ims.pem')
        (_, stdout, stderr) = self.ssh.exec_command(
            "sudo cp ~/cloudify_ims.pem /etc/cloudify/ && "
            "sudo chmod 444 /etc/cloudify/cloudify_ims.pem && "
            "sudo yum install -y gcc python-devel python-cmd2 && "
            "cfy status")
        self.__logger.info("output:\n%s", stdout.read())
        self.__logger.info("error:\n%s", stderr.read())

        self.image_alt = self.publish_image_alt()
        self.flavor_alt = self.create_flavor_alt()

        duration = time.time() - start_time
        self.details['orchestrator'].update(status='PASS', duration=duration)

        self.vnf['inputs'].update(dict(
            external_network_name=self.ext_net.name))
        self.vnf['inputs'].update(dict(
            target_vnf_image_id=self.image_alt.id))
        self.vnf['inputs'].update(dict(
            reference_vnf_image_id=self.image_alt.id))
        self.vnf['inputs'].update(dict(
            target_vnf_flavor_id=self.flavor_alt.id))
        self.vnf['inputs'].update(dict(
            reference_vnf_flavor_id=self.flavor_alt.id))
        self.vnf['inputs'].update(dict(
            keystone_username=self.project.user.name))
        self.vnf['inputs'].update(dict(
            keystone_password=self.project.password))
        self.vnf['inputs'].update(dict(
            keystone_tenant_name=self.project.project.name))
        self.vnf['inputs'].update(dict(
            keystone_user_domain_name=os.environ.get(
                'OS_USER_DOMAIN_NAME', 'Default')))
        self.vnf['inputs'].update(dict(
            keystone_project_domain_name=os.environ.get(
                'OS_PROJECT_DOMAIN_NAME', 'Default')))
        self.vnf['inputs'].update(dict(
            region=os.environ.get('OS_REGION_NAME', 'RegionOne')))
        self.vnf['inputs'].update(dict(
            keystone_url=self.get_public_auth_url(self.orig_cloud)))

        if self.deploy_vnf() and self.test_vnf():
            self.result = 100
            return 0
        self.result = 1/3 * 100
        return 1

    def deploy_vnf(self):
        start_time = time.time()

        self.cloud.create_security_group_rule(
            'default', port_range_min=22, port_range_max=22,
            protocol='tcp', direction='ingress')

        self.__logger.info("Upload VNFD")
        descriptor = self.vnf['descriptor']
        self.util_info["cfy"] = self.cfy_client
        self.util_info["cfy_manager_ip"] = self.fip.floating_ip_address
        self.util_info["deployment_name"] = descriptor.get('name')

        self.cfy_client.blueprints.upload(
            descriptor.get('file_name'), descriptor.get('name'))

        self.__logger.info("Create VNF Instance")
        self.cfy_client.deployments.create(
            descriptor.get('name'), descriptor.get('name'),
            self.vnf.get('inputs'))

        wait_for_execution(
            self.cfy_client, get_execution_id(
                self.cfy_client, descriptor.get('name')),
            self.__logger, timeout=7200)

        self.__logger.info("Start the VNF Instance deployment")
        execution = self.cfy_client.executions.start(
            descriptor.get('name'), 'install')
        # Show execution log
        execution = wait_for_execution(
            self.cfy_client, execution, self.__logger)

        duration = time.time() - start_time

        self.__logger.info(execution)
        if execution.status == 'terminated':
            self.details['vnf'].update(status='PASS', duration=duration)
            result = True
        else:
            self.details['vnf'].update(status='FAIL', duration=duration)
            result = False
        return result

    def test_vnf(self):
        start_time = time.time()
        testing = vrouter_base.VrouterOnBoardingBase(
            self.case_name, self.util, self.util_info)
        result, test_result_data = testing.test_vnf()
        duration = time.time() - start_time
        if result:
            self.details['test_vnf'].update(
                status='PASS', result='OK', full_result=test_result_data,
                duration=duration)
        else:
            self.details['test_vnf'].update(
                status='FAIL', result='NG', full_result=test_result_data,
                duration=duration)
        return True

    def clean(self):
        try:
            dep_name = self.vnf['descriptor'].get('name')
            # kill existing execution
            self.__logger.info('Deleting the current deployment')
            exec_list = self.cfy_client.executions.list()
            for execution in exec_list:
                if execution['status'] == "started":
                    try:
                        self.cfy_client.executions.cancel(
                            execution['id'], force=True)
                    except Exception:  # pylint: disable=broad-except
                        self.__logger.warn("Can't cancel the current exec")

            execution = self.cfy_client.executions.start(
                dep_name, 'uninstall', parameters=dict(ignore_failure=True))

            wait_for_execution(self.cfy_client, execution, self.__logger)
            self.cfy_client.deployments.delete(
                self.vnf['descriptor'].get('name'))
            self.cfy_client.blueprints.delete(
                self.vnf['descriptor'].get('name'))
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Some issue during the undeployment ..")
        if self.image_alt:
            self.cloud.delete_image(self.image_alt)
        if self.flavor_alt:
            self.orig_cloud.delete_flavor(self.flavor_alt.id)
        super(CloudifyVrouter, self).clean()

def wait_for_execution(client, execution, logger, timeout=7200, ):
    """Wait for a workflow execution on Cloudify Manager."""
    # if execution already ended - return without waiting
    if execution.status in Execution.END_STATES:
        return execution

    if timeout is not None:
        deadline = time.time() + timeout

    # Poll for execution status and execution logs, until execution ends
    # and we receive an event of type in WORKFLOW_END_TYPES
    offset = 0
    batch_size = 50
    event_list = []
    execution_ended = False
    while True:
        event_list = client.events.list(
            execution_id=execution.id, _offset=offset, _size=batch_size,
            include_logs=True, sort='@timestamp').items

        offset = offset + len(event_list)
        for event in event_list:
            logger.debug(event.get('message'))

        if timeout is not None:
            if time.time() > deadline:
                raise RuntimeError(
                    'execution of operation {0} for deployment {1} '
                    'timed out'.format(execution.workflow_id,
                                       execution.deployment_id))
            else:
                # update the remaining timeout
                timeout = deadline - time.time()

        if not execution_ended:
            execution = client.executions.get(execution.id)
            execution_ended = execution.status in Execution.END_STATES

        if execution_ended:
            break

        time.sleep(5)

    return execution


def get_execution_id(client, deployment_id):
    """
    Get the execution id of a env preparation.
    network, security group, fip, VM creation
    """
    executions = client.executions.list(deployment_id=deployment_id)
    for execution in executions:
        if execution.workflow_id == 'create_deployment_environment':
            return execution
    raise RuntimeError('Failed to get create_deployment_environment '
                       'workflow execution.'
                       'Available executions: {0}'.format(executions))
