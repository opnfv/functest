#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
VMTP_ is a small python application that will automatically perform ping
connectivity, round trip time measurement (latency) and TCP/UDP throughput
measurement for the following East/West flows on any OpenStack deployment:

- VM to VM same network (private fixed IP, flow #1)
- VM to VM different network using fixed IP (same as intra-tenant L3 fixed IP,
  flow #2)
- VM to VM different network using floating IP and NAT (same as floating IP
  inter-tenant L3, flow #3)

.. _VMTP: http://vmtp.readthedocs.io/en/latest/
"""

import json
import logging
import os
import subprocess
import tempfile
import time
import yaml

from xtesting.core import testcase

from functest.core import singlevm
from functest.utils import env


class Vmtp(singlevm.VmReady1):
    """Class to run Vmtp_ as an OPNFV Functest testcase

    .. _Vmtp: http://vmtp.readthedocs.io/en/latest/
    """
    # pylint: disable=too-many-instance-attributes

    __logger = logging.getLogger(__name__)

    filename = ('/home/opnfv/functest/images/'
                'ubuntu-14.04-server-cloudimg-amd64-disk1.img')
    flavor_ram = 2048
    flavor_vcpus = 1
    flavor_disk = 0

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'vmtp'
        super(Vmtp, self).__init__(**kwargs)
        self.config = "{}/vmtp.conf".format(self.res_dir)
        (_, self.privkey_filename) = tempfile.mkstemp()
        (_, self.pubkey_filename) = tempfile.mkstemp()

    def generate_keys(self):
        """Generate Keys

        Raises: Exception on error
        """
        assert self.cloud
        name = "vmtp_{}".format(self.guid)
        self.__logger.info("Creating keypair with name: '%s'", name)
        keypair = self.cloud.create_keypair(name)
        self.__logger.debug("keypair: %s", keypair)
        with open(self.privkey_filename, 'w') as key_file:
            key_file.write(keypair.private_key)
        with open(self.pubkey_filename, 'w') as key_file:
            key_file.write(keypair.public_key)
        self.cloud.delete_keypair(keypair.id)

    def write_config(self):
        """Write vmtp.conf

        Raises: Exception on error
        """
        assert self.cloud
        if not os.path.exists(self.res_dir):
            os.makedirs(self.res_dir)
        cmd = ['vmtp', '-sc']
        output = subprocess.check_output(cmd)
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        with open(self.config, "w+") as conf:
            vmtp_conf = yaml.load(output)
            vmtp_conf["private_key_file"] = self.privkey_filename
            vmtp_conf["public_key_file"] = self.pubkey_filename
            vmtp_conf["image_name"] = str(self.image.name)
            vmtp_conf["router_name"] = "pns_router_{}".format(self.guid)
            vmtp_conf["flavor_type"] = str(self.flavor.name)
            vmtp_conf["internal_network_name"] = [
                "pns-internal-net_{}".format(self.guid),
                "pns-internal-net2_{}".format(self.guid)]
            vmtp_conf["vm_name_client"] = "TestClient_{}".format(self.guid)
            vmtp_conf["vm_name_server"] = "TestServer_{}".format(self.guid)
            vmtp_conf["security_group_name"] = "pns-security{}".format(
                self.guid)
            vmtp_conf["dns_nameservers"] = [env.get('NAMESERVER')]
            conf.write(yaml.dump(vmtp_conf))

    def run_vmtp(self):
        """Run Vmtp and generate charts

        Raises: Exception on error
        """
        assert self.cloud
        cmd = ['vmtp', '-d', '--json', '{}/vmtp.json'.format(self.res_dir),
               '-c', self.config]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        cmd = ['vmtp_genchart', '-c', '{}/vmtp.html'.format(self.res_dir),
               '{}/vmtp.json'.format(self.res_dir)]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        with open('{}/vmtp.json'.format(self.res_dir), 'r') as res_file:
            self.details = json.load(res_file)

    def run(self, **kwargs):
        self.start_time = time.time()
        status = testcase.TestCase.EX_RUN_ERROR
        try:
            assert self.cloud
            self.image = self.publish_image()
            self.flavor = self.create_flavor()
            self.generate_keys()
            self.write_config()
            self.run_vmtp()
            self.result = 100
            status = testcase.TestCase.EX_OK
        except subprocess.CalledProcessError as cpe:
            self.__logger.error(
                "Exception when calling %s\n%s", cpe.cmd, cpe.output)
            self.result = 0
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot run vmtp")
            self.result = 0
        self.stop_time = time.time()
        return status

    def clean(self):
        try:
            assert self.cloud
            os.remove(self.privkey_filename)
            os.remove(self.pubkey_filename)
            self.cloud.delete_image(self.image)
            self.cloud.delete_network("pns-internal-net_{}".format(self.guid))
            self.cloud.delete_network("pns-internal-net2_{}".format(self.guid))
        except Exception:  # pylint: disable=broad-except
            pass
