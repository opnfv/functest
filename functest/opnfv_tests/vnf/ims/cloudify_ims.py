#!/usr/bin/env python

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""CloudifyIms testcase implementation."""

from __future__ import division

import logging
import os
import time
import yaml

from cloudify_rest_client.executions import Execution
import pkg_resources
import scp
import six

from functest.core import cloudify
from functest.opnfv_tests.vnf.ims import clearwater_ims_base
from functest.utils import config

__author__ = "Valentin Boucher <valentin.boucher@orange.com>"


class CloudifyIms(cloudify.Cloudify):
    """Clearwater vIMS deployed with Cloudify Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    filename_alt = ('/home/opnfv/functest/images/'
                    'ubuntu-14.04-server-cloudimg-amd64-disk1.img')

    flavor_alt_ram = 2048
    flavor_alt_vcpus = 2
    flavor_alt_disk = 25

    quota_security_group = 20
    quota_security_group_rule = 100
    quota_port = 50

    def __init__(self, **kwargs):
        """Initialize CloudifyIms testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cloudify_ims"
        super(CloudifyIms, self).__init__(**kwargs)

        # Retrieve the configuration
        try:
            self.config = getattr(
                config.CONF, 'vnf_{}_config'.format(self.case_name))
        except Exception:
            raise Exception("VNF config file not found")

        self.case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/ims')
        config_file = os.path.join(self.case_dir, self.config)
        self.orchestrator = dict(
            requirements=get_config("orchestrator.requirements", config_file),
        )
        self.details['orchestrator'] = dict(
            name=get_config("orchestrator.name", config_file),
            version=get_config("orchestrator.version", config_file),
            status='ERROR',
            result=''
        )
        self.__logger.debug("Orchestrator configuration %s", self.orchestrator)
        self.vnf = dict(
            descriptor=get_config("vnf.descriptor", config_file),
            inputs=get_config("vnf.inputs", config_file),
            requirements=get_config("vnf.requirements", config_file)
        )
        self.details['vnf'] = dict(
            descriptor_version=self.vnf['descriptor']['version'],
            name=get_config("vnf.name", config_file),
            version=get_config("vnf.version", config_file),
        )
        self.__logger.debug("VNF configuration: %s", self.vnf)

        self.details['test_vnf'] = dict(
            name=get_config("vnf_test_suite.name", config_file),
            version=get_config("vnf_test_suite.version", config_file)
        )

        self.image_alt = None
        self.flavor_alt = None

    def execute(self):
        assert super(CloudifyIms, self).execute() == 0
        # pylint: disable=too-many-locals,too-many-statements
        """
        Deploy Cloudify Manager.

        network, security group, fip, VM creation
        """
        start_time = time.time()
        self.orig_cloud.set_network_quotas(
            self.project.project.name,
            security_group=self.quota_security_group,
            security_group_rule=self.quota_security_group_rule,
            port=self.quota_port)
        self.__logger.info("Put OpenStack creds in manager")
        cfy_creds = dict(
            keystone_username=self.project.user.name,
            keystone_password=self.project.password,
            keystone_tenant_name=self.project.project.name,
            keystone_url=self.get_public_auth_url(self.orig_cloud),
            region=os.environ.get('OS_REGION_NAME', 'RegionOne'),
            user_domain_name=os.environ.get(
                'OS_USER_DOMAIN_NAME', 'Default'),
            project_domain_name=os.environ.get(
                'OS_PROJECT_DOMAIN_NAME', 'Default'))
        self.__logger.info("Set creds for cloudify manager %s", cfy_creds)
        secrets_list = self.cfy_client.secrets.list()
        for k, val in six.iteritems(cfy_creds):
            if not any(d.get('key', None) == k for d in secrets_list):
                self.cfy_client.secrets.create(k, val)
            else:
                self.cfy_client.secrets.update(k, val)

        duration = time.time() - start_time

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

        self.details['orchestrator'].update(status='PASS', duration=duration)

        self.vnf['inputs'].update(dict(
            external_network_name=self.ext_net.name,
            network_name=self.network.name,
            key_pair_name=self.keypair.name
        ))
        if (self.deploy_vnf() and self.test_vnf()):
            self.result = 100
            return 0
        self.result = 1/3 * 100
        return 1

    def deploy_vnf(self):
        """Deploy Clearwater IMS."""
        start_time = time.time()

        self.cloud.create_security_group_rule(
            'default', port_range_min=22, port_range_max=22,
            protocol='tcp', direction='ingress')

        self.__logger.info("Upload VNFD")
        descriptor = self.vnf['descriptor']
        self.cfy_client.blueprints.upload(
            descriptor.get('file_name'), descriptor.get('name'))

        self.image_alt = self.publish_image_alt()
        self.flavor_alt = self.create_flavor_alt()
        self.vnf['inputs'].update(dict(
            image_id=self.image_alt.id,
            flavor_id=self.flavor_alt.id,
        ))

        self.__logger.info("Create VNF Instance")
        self.cfy_client.deployments.create(
            descriptor.get('name'), descriptor.get('name'),
            self.vnf.get('inputs'))

        wait_for_execution(
            self.cfy_client,
            get_execution_id(self.cfy_client, descriptor.get('name')),
            self.__logger, timeout=300)

        self.__logger.info("Start the VNF Instance deployment")
        execution = self.cfy_client.executions.start(
            descriptor.get('name'), 'install')
        # Show execution log
        execution = wait_for_execution(
            self.cfy_client, execution, self.__logger, timeout=3600)

        duration = time.time() - start_time

        self.__logger.info(execution)
        if execution.status == 'terminated':
            self.details['vnf'].update(status='PASS', duration=duration)
            self.result += 1/3 * 100
            result = True
        else:
            self.details['vnf'].update(status='FAIL', duration=duration)
            result = False
        return result

    def test_vnf(self):
        """Run test on clearwater ims instance."""
        start_time = time.time()

        testing = clearwater_ims_base.ClearwaterOnBoardingBase(self.case_name)
        outputs = self.cfy_client.deployments.outputs.get(
            self.vnf['descriptor'].get('name'))['outputs']
        dns_ip = outputs['dns_ip']
        ellis_ip = outputs['ellis_ip']
        testing.config_ellis(ellis_ip)

        if not dns_ip:
            return False

        short_result = testing.run_clearwater_live_test(
            dns_ip=dns_ip,
            public_domain=self.vnf['inputs']["public_domain"])
        duration = time.time() - start_time
        self.__logger.info(short_result)
        self.details['test_vnf'].update(result=short_result,
                                        duration=duration)
        try:
            vnf_test_rate = short_result['passed'] / (
                short_result['total'] - short_result['skipped'])
            # orchestrator + vnf + test_vnf
            self.result += vnf_test_rate / 3 * 100
        except ZeroDivisionError:
            self.__logger.error("No test has been executed")
            self.details['test_vnf'].update(status='FAIL')
            return False
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot calculate results")
            self.details['test_vnf'].update(status='FAIL')
            return False
        return True if vnf_test_rate > 0 else False

    def clean(self):
        """Clean created objects/functions."""
        try:
            dep_name = self.vnf['descriptor'].get('name')
            # kill existing execution
            self.__logger.info('Deleting the current deployment')
            exec_list = self.cfy_client.executions.list(dep_name)
            for execution in exec_list:
                if execution['status'] == "started":
                    try:
                        self.cfy_client.executions.cancel(
                            execution['id'], force=True)
                    except Exception:  # pylint: disable=broad-except
                        self.__logger.warn("Can't cancel the current exec")

            execution = self.cfy_client.executions.start(
                dep_name,
                'uninstall',
                parameters=dict(ignore_failure=True),
                force=True)

            wait_for_execution(self.cfy_client, execution, self.__logger)
            self.cfy_client.deployments.delete(
                self.vnf['descriptor'].get('name'))
            self.cfy_client.blueprints.delete(
                self.vnf['descriptor'].get('name'))
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Some issue during the undeployment ..")

        super(CloudifyIms, self).clean()


# ----------------------------------------------------------
#
#               YAML UTILS
#
# -----------------------------------------------------------
def get_config(parameter, file_path):
    """
    Get config parameter.

    Returns the value of a given parameter in file.yaml
    parameter must be given in string format with dots
    Example: general.openstack.image_name
    """
    with open(file_path) as config_file:
        file_yaml = yaml.safe_load(config_file)
    config_file.close()
    value = file_yaml
    for element in parameter.split("."):
        value = value.get(element)
        if value is None:
            raise ValueError("The parameter %s is not defined in"
                             " reporting.yaml" % parameter)
    return value


def wait_for_execution(client, execution, logger, timeout=3600, ):
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
            execution_id=execution.id,
            _offset=offset,
            _size=batch_size,
            include_logs=True,
            sort='@timestamp').items

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
