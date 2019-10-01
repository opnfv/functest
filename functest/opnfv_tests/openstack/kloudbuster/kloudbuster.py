#!/usr/bin/env python

# Copyright (c) 2019 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
KloudBuster_ is a tool that can load the data plane or storage infrastructure
of any OpenStack cloud at massive scale and measure how well the cloud behaves
under load where it matters: from the VMs standpoint, where cloud applications
run.

.. _KloudBuster: https://kloudbuster.readthedocs.io/en/latest/
"""

import json
import logging
import os
import subprocess
import time
import yaml

from xtesting.core import testcase

from functest.core import singlevm


class KloudBuster(singlevm.VmReady2):
    """Class to run KloudBuster_ as an OPNFV Functest testcase

    .. _KloudBuster: https://kloudbuster.readthedocs.io/en/latest/
    """

    __logger = logging.getLogger(__name__)

    filename = '/home/opnfv/functest/images/kloudbuster-7.1.1.qcow2'

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'kloudbuster'
        super(KloudBuster, self).__init__(**kwargs)
        self.config = "{}/kb.conf".format(self.res_dir)

    def create_flavor(self, name=None):
        pass

    def write_config(self):
        """Write kloudbuster.conf

        Raises: Exception on error
        """
        assert self.cloud
        if not os.path.exists(self.res_dir):
            os.makedirs(self.res_dir)
        cmd = ['kloudbuster', '--show-config']
        output = subprocess.check_output(cmd).decode("utf-8")
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        with open(self.config, "w+") as conf:
            kb_conf = yaml.load(output)
            kb_conf["image_name"] = str(self.image.name)
            conf.write(yaml.dump(kb_conf))

    def run_kloudbuster(self):
        """Run KloudBuster and generate charts

        Raises: Exception on error
        """
        assert self.cloud
        cmd = ['kloudbuster', '--rc', '/home/opnfv/functest/conf/env_file',
               '--config', self.config,
               '--html', '{}/http_data_plane_scale.html'.format(self.res_dir),
               '--json', '{}/http_data_plane_scale.json'.format(self.res_dir)]
        output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT).decode("utf-8")
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        with open('{}/http_data_plane_scale.json'.format(self.res_dir),
                  'r') as res_file:
            self.details['http_data_plane_scale'] = json.load(res_file)
        cmd = ['kloudbuster', '--rc', '/home/opnfv/functest/conf/env_file',
               '--config', self.config, '--storage',
               '--html', '{}/storage_scale.html'.format(self.res_dir),
               '--json', '{}/storage_scale.json'.format(self.res_dir)]
        output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT).decode("utf-8")
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        with open('{}/storage_scale.json'.format(self.res_dir),
                  'r') as res_file:
            self.details['storage_scale'] = json.load(res_file)

    def run(self, **kwargs):
        self.start_time = time.time()
        status = testcase.TestCase.EX_RUN_ERROR
        try:
            assert self.cloud
            assert super(KloudBuster, self).run(**kwargs) == self.EX_OK
            self.write_config()
            self.run_kloudbuster()
            self.result = 100
            status = testcase.TestCase.EX_OK
        except subprocess.CalledProcessError as cpe:
            self.__logger.error(
                "Exception when calling %s\n%s", cpe.cmd,
                cpe.output.decode("utf-8"))
            self.result = 0
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot run KloudBuster")
            self.result = 0
        self.stop_time = time.time()
        return status
