#!/usr/bin/env python

# Copyright (c) 2017 Orange, IXIA and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""CloudifyImsPerf testcase implementation."""

import logging
import os
import time

import json
import yaml
import paramiko
import dns.resolver
from jinja2 import Environment, FileSystemLoader

from functest.energy import energy
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.opnfv_tests.vnf.ims import cloudify_ims
from functest.opnfv_tests.vnf.ims.ixia.utils import IxChassisUtils
from functest.opnfv_tests.vnf.ims.ixia.utils import IxLoadUtils
from functest.opnfv_tests.vnf.ims.ixia.utils import IxRestUtils
from functest.utils.constants import CONST

from snaps.config.flavor import FlavorConfig
from snaps.config.image import ImageConfig
from snaps.config.network import NetworkConfig, PortConfig, SubnetConfig
from snaps.config.router import RouterConfig
from snaps.config.security_group import (
    Direction, Protocol, SecurityGroupConfig, SecurityGroupRuleConfig)
from snaps.config.vm_inst import FloatingIpConfig, VmInstanceConfig
from snaps.openstack.create_flavor import OpenStackFlavor
from snaps.openstack.create_instance import OpenStackVmInstance
from snaps.openstack.create_network import OpenStackNetwork
from snaps.openstack.create_router import OpenStackRouter
from snaps.openstack.create_security_group import OpenStackSecurityGroup


__author__ = "Valentin Boucher <valentin.boucher@orange.com>"


class CloudifyImsPerf(cloudify_ims.CloudifyIms):
    """Clearwater vIMS deployed with Cloudify Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        """Initialize CloudifyIms testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cloudify_ims_perf"
        super(CloudifyImsPerf, self).__init__(**kwargs)

        # Retrieve the configuration
        try:
            self.config = getattr(
                CONST, 'vnf_{}_config'.format(self.case_name))
        except Exception:
            raise Exception("VNF config file not found")

        self.snaps_creds = ''
        self.created_object = []

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

        self.test = dict(
            version=get_config("vnf_test_suite.version", config_file),
            inputs=get_config("vnf_test_suite.inputs", config_file),
            requirements=get_config("vnf_test_suite.requirements", config_file)
        )

        self.details['test_vnf'] = dict(
            name=get_config("vnf_test_suite.name", config_file),
            version=get_config("vnf_test_suite.version", config_file),
            requirements=get_config("vnf_test_suite.requirements", config_file)
        )
        self.images = get_config("tenant_images", config_file)
        self.__logger.info("Images needed for vIMS: %s", self.images)

    def test_vnf(self):
        """Run IXIA Stress test on clearwater ims instance."""
        start_time = time.time()

        cfy_client = self.orchestrator['object']

        outputs = cfy_client.deployments.outputs.get(
            self.vnf['descriptor'].get('name'))['outputs']
        dns_ip = outputs['dns_ip']
        ellis_ip = outputs['ellis_ip']

        self.__logger.info("Creating full IXIA network ...")
        subnet_settings = SubnetConfig(name='ixia_management_subnet',
                                       cidr='10.10.10.0/24')
        network_settings = NetworkConfig(name='ixia_management_network',
                                         subnet_settings=[subnet_settings])
        network_creator = OpenStackNetwork(self.snaps_creds, network_settings)
        network_creator.create()
        self.created_object.append(network_creator)
        ext_net_name = snaps_utils.get_ext_net_name(self.snaps_creds)
        router_creator = OpenStackRouter(
            self.snaps_creds,
            RouterConfig(
                name='ixia_management_router',
                external_gateway=ext_net_name,
                internal_subnets=[subnet_settings.name]))
        router_creator.create()
        self.created_object.append(router_creator)

        # security group creation
        self.__logger.info("Creating security groups for IXIA VMs")
        sg_rules = list()
        sg_rules.append(
            SecurityGroupRuleConfig(sec_grp_name="ixia_management",
                                    direction=Direction.ingress,
                                    protocol=Protocol.tcp, port_range_min=1,
                                    port_range_max=65535))
        sg_rules.append(
            SecurityGroupRuleConfig(sec_grp_name="ixia_management",
                                    direction=Direction.ingress,
                                    protocol=Protocol.udp, port_range_min=1,
                                    port_range_max=65535))
        sg_rules.append(
            SecurityGroupRuleConfig(sec_grp_name="ixia_management",
                                    direction=Direction.ingress,
                                    protocol=Protocol.icmp))

        ixia_managment_sg_settings = SecurityGroupConfig(
            name="ixia_management", rule_settings=sg_rules)
        securit_group_creator = OpenStackSecurityGroup(
            self.snaps_creds,
            ixia_managment_sg_settings)

        securit_group_creator.create()
        self.created_object.append(securit_group_creator)

        sg_rules = list()
        sg_rules.append(
            SecurityGroupRuleConfig(sec_grp_name="ixia_ssh_http",
                                    direction=Direction.ingress,
                                    protocol=Protocol.tcp, port_range_min=1,
                                    port_range_max=65535))

        ixia_ssh_http_sg_settings = SecurityGroupConfig(
            name="ixia_ssh_http", rule_settings=sg_rules)
        securit_group_creator = OpenStackSecurityGroup(
            self.snaps_creds,
            ixia_ssh_http_sg_settings)

        securit_group_creator.create()
        self.created_object.append(securit_group_creator)

        chassis_flavor_settings = FlavorConfig(
            name="ixia_vChassis",
            ram=4096,
            disk=40,
            vcpus=2)
        flavor_creator = OpenStackFlavor(self.snaps_creds,
                                         chassis_flavor_settings)
        flavor_creator.create()
        self.created_object.append(flavor_creator)

        card_flavor_settings = FlavorConfig(
            name="ixia_vCard",
            ram=4096,
            disk=4,
            vcpus=2)
        flavor_creator = OpenStackFlavor(self.snaps_creds,
                                         card_flavor_settings)
        flavor_creator.create()
        self.created_object.append(flavor_creator)

        load_flavor_settings = FlavorConfig(
            name="ixia_vLoad",
            ram=8192,
            disk=100,
            vcpus=4)
        flavor_creator = OpenStackFlavor(self.snaps_creds,
                                         load_flavor_settings)
        flavor_creator.create()
        self.created_object.append(flavor_creator)

        chassis_image_settings = ImageConfig(
            name=self.test['requirements']['chassis']['image'],
            image_user='admin',
            exists=True)

        card_image_settings = ImageConfig(
            name=self.test['requirements']['card']['image'],
            image_user='admin',
            exists=True)

        load_image_settings = ImageConfig(
            name=self.test['requirements']['load']['image'],
            image_user='admin',
            exists=True)

        chassis_port_settings = PortConfig(
            name='ixia_chassis_port', network_name=network_settings.name)

        card1_port1_settings = PortConfig(
            name='ixia_card1_port1', network_name=network_settings.name)

        card2_port1_settings = PortConfig(
            name='ixia_card2_port1', network_name=network_settings.name)

        card1_port2_settings = PortConfig(
            name='ixia_card1_port2', network_name="cloudify_ims_network")

        card2_port2_settings = PortConfig(
            name='ixia_card2_port2', network_name="cloudify_ims_network")

        load_port_settings = PortConfig(
            name='ixia_load_port', network_name=network_settings.name)

        chassis_settings = VmInstanceConfig(
            name='ixia_vChassis',
            flavor=chassis_flavor_settings.name,
            port_settings=[chassis_port_settings],
            security_group_names=[ixia_ssh_http_sg_settings.name,
                                  ixia_managment_sg_settings.name],
            floating_ip_settings=[FloatingIpConfig(
                name='ixia_vChassis_fip',
                port_name=chassis_port_settings.name,
                router_name=router_creator.router_settings.name)])

        vm_creator = OpenStackVmInstance(self.snaps_creds,
                                         chassis_settings,
                                         chassis_image_settings)

        self.__logger.info("Creating Ixia vChassis VM")
        vm_creator.create()
        fip_chassis = vm_creator.get_floating_ip().ip
        self.created_object.append(vm_creator)

        card1_settings = VmInstanceConfig(
            name='ixia_vCard1',
            flavor=card_flavor_settings.name,
            port_settings=[card1_port1_settings, card1_port2_settings],
            security_group_names=[ixia_managment_sg_settings.name])

        vm_creator = OpenStackVmInstance(self.snaps_creds,
                                         card1_settings,
                                         card_image_settings)

        self.__logger.info("Creating Ixia vCard1 VM")
        vm_creator.create()
        vcard_ips = list()
        vcard_ips_p2 = list()
        vcard_ips.append(vm_creator.get_port_ip('ixia_card1_port1'))
        vcard_ips_p2.append(vm_creator.get_port_ip('ixia_card1_port2'))
        self.created_object.append(vm_creator)

        card2_settings = VmInstanceConfig(
            name='ixia_vCard2',
            flavor=card_flavor_settings.name,
            port_settings=[card2_port1_settings, card2_port2_settings],
            security_group_names=[ixia_managment_sg_settings.name])

        vm_creator = OpenStackVmInstance(self.snaps_creds,
                                         card2_settings,
                                         card_image_settings)

        self.__logger.info("Creating Ixia vCard2 VM")
        vm_creator.create()
        vcard_ips.append(vm_creator.get_port_ip('ixia_card2_port1'))
        vcard_ips_p2.append(vm_creator.get_port_ip('ixia_card2_port2'))
        self.created_object.append(vm_creator)

        load_settings = VmInstanceConfig(
            name='ixia_vLoad',
            flavor=load_flavor_settings.name,
            port_settings=[load_port_settings],
            security_group_names=[ixia_ssh_http_sg_settings.name,
                                  ixia_managment_sg_settings.name],
            floating_ip_settings=[FloatingIpConfig(
                name='ixia_vLoad_fip',
                port_name=load_port_settings.name,
                router_name=router_creator.router_settings.name)])

        vm_creator = OpenStackVmInstance(self.snaps_creds,
                                         load_settings,
                                         load_image_settings)

        self.__logger.info("Creating Ixia vLoad VM")
        vm_creator.create()
        fip_load = vm_creator.get_floating_ip().ip
        self.created_object.append(vm_creator)

        self.__logger.info("Chassis IP is: %s", fip_chassis)
        login_url = "https://" + str(fip_chassis) + "/api/v1/auth/session"
        cards_url = "https://" + str(fip_chassis) + "/api/v2/ixos/cards/"

        payload = json.dumps({"username": "admin",
                              "password": "admin",
                              "rememberMe": "false"})
        api_key = json.loads((
            IxChassisUtils.ChassisRestAPI.postWithPayload(
                login_url, payload)))["apiKey"]

        self.__logger.info("Adding 2 card back inside the ixia chassis...")

        for ip in vcard_ips:
            payload = {"ipAddress": str(ip)}
            response = json.loads(IxChassisUtils.ChassisRestAPI.postOperation(
                cards_url, api_key, payload))
            count = 0
            while (int(
                    IxChassisUtils.ChassisRestAPI.getWithHeaders(
                        response['url'], api_key)['progress']) != 100):
                self.__logger.debug("Operation did not finish yet. \
                                    Waiting for 1 more second..")
                time.sleep(1)
                if count > 60:
                    raise Exception("Adding card take more than 60 seconds")
                count += 1

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        ssh.connect(fip_chassis, username="admin", password="admin")
        cmd = "set license-check disable"
        run_blocking_ssh_command(ssh, cmd)
        cmd = "restart-service ixServer"
        run_blocking_ssh_command(ssh, cmd)

        self.config_ellis(ellis_ip)

        # Get IPs of P-CSCF
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_ip]
        result = resolver.query("bono.clearwater.local")

        iplistims = ''
        i = 0
        for rdata in result:
            i = i + 1
            print rdata.address
            iplistims += str(rdata.address)
            if i != len(result):
                iplistims += ';'

        kResourcesUrl = 'http://%s:%s/api/v0/resources' % (fip_load, 8080)

        kRxfPath = r"REG_CALL_OPNFV_v13.rxf"
        test_filname = self.test['inputs']['test_filname']
        kGatewaySharedFolder = '/mnt/ixload-share/'
        kRxfRelativeUploadPath = 'uploads/%s' % os.path.split(kRxfPath)[1]
        kRxfAbsoluteUploadPath = os.path.join(kGatewaySharedFolder,
                                              kRxfRelativeUploadPath)
        kChassisList = [str(fip_chassis)]
        dataFileNameList = [test_filname,
                            'Registration_only_LPS.tst',
                            'SIPCall.tst']

        kPortListPerCommunityCommunity = {"VoIP1@VM1": [(1, 1, 1)],
                                          "VoIP2@VM2": [(1, 2, 1)]}

        kStatsToDisplayDict = self.test['inputs']['stats']
        connection = IxRestUtils.getConnection(fip_load, 8080)

        self.__logger.info("Creating a new session...")
        sessionUrl = IxLoadUtils.createSession(connection,
                                               self.test['version'])

        license_server = self.test['inputs']['licenseServer']
        IxLoadUtils.configureLicenseServer(connection,
                                           sessionUrl,
                                           license_server)

        files_dir = os.path.join(self.case_dir, 'ixia/files')
        target_file = open(os.path.join(files_dir, test_filname), 'w')
        j2_env = Environment(loader=FileSystemLoader(files_dir),
                             trim_blocks=True)
        self.test['inputs'].update(dict(
            ipchassis=fip_chassis, ipcard1=vcard_ips_p2[0],
            ipcard2=vcard_ips_p2[1], iplistims=iplistims
        ))

        target_file.write(
            j2_env.get_template(test_filname + '.template').render(
                self.test['inputs']
            ))
        target_file.close()

        self.__logger.info('Uploading files %s...' % kRxfPath)
        for dataFile in dataFileNameList:
            localFilePath = os.path.join(files_dir, dataFile)
            remoteFilePath = os.path.join(kGatewaySharedFolder,
                                          'uploads/%s' % dataFile)
            IxLoadUtils.uploadFile(connection, kResourcesUrl,
                                   localFilePath, remoteFilePath)
        self.__logger.info('Upload file finished.')

        self.__logger.info("Loading repository %s..." % kRxfAbsoluteUploadPath)
        IxLoadUtils.loadRepository(connection, sessionUrl,
                                   kRxfAbsoluteUploadPath)

        self.__logger.info("Clearing chassis list...")
        IxLoadUtils.clearChassisList(connection, sessionUrl)

        self.__logger.info("Adding chassis %s..." % (kChassisList))
        IxLoadUtils.addChassisList(connection, sessionUrl, kChassisList)

        self.__logger.info("Assigning new ports...")
        IxLoadUtils.assignPorts(connection, sessionUrl,
                                kPortListPerCommunityCommunity)

        self.__logger.info("Starting the test...")
        IxLoadUtils.runTest(connection, sessionUrl)

        self.__logger.info(
            "Polling values for stats %s..." % (kStatsToDisplayDict))
        result = IxLoadUtils.pollStats(connection, sessionUrl,
                                       kStatsToDisplayDict)
        self.__logger.info("Test finished.")
        self.__logger.info("Checking test status...")
        testRunError = IxLoadUtils.getTestRunError(connection, sessionUrl)

        self.__logger.info(result)
        duration = time.time() - start_time
        self.details['test_vnf'].update(status='PASS',
                                        result=result,
                                        duration=duration)
        if testRunError:
            self.__logger.info(
                "The test exited with following error: %s" % (testRunError))
            self.details['test_vnf'].update(status='FAIL', duration=duration)
            return False
        else:
            self.__logger.info("The test completed successfully.")
            self.details['test_vnf'].update(status='PASS', duration=duration)
            self.result += 1/3 * 100
            return True

    def clean(self):
        """Clean created objects/functions."""
        super(CloudifyImsPerf, self).clean()

    @energy.enable_recording
    def run(self, **kwargs):
        """Execute CloudifyIms test case."""
        return super(CloudifyImsPerf, self).run(**kwargs)


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


def run_blocking_ssh_command(ssh, cmd, error_msg="Unable to run this command"):
    """Command to run ssh command with the exit status."""
    stdin, stdout, stderr = ssh.exec_command(cmd)
    if stdout.channel.recv_exit_status() != 0:
        raise Exception(error_msg)
