#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Refstack testcase implementation."""

import logging
import os
import re
import subprocess
import yaml

from functest.opnfv_tests.openstack.tempest import tempest
from functest.utils import config


class Refstack(tempest.TempestCommon):
    """Refstack testcase implementation class."""

    __logger = logging.getLogger(__name__)

    defcorelist = os.path.join(
        getattr(config.CONF, 'dir_refstack_data'), 'defcore.txt')

    def _extract_refstack_data(self):
        yaml_data = ""
        with open(self.defcorelist) as def_file:
            for line in def_file:
                try:
                    grp = re.search(r'^([^\[]*)(\[.*\])\n*$', line)
                    yaml_data = "{}\n{}: {}".format(
                        yaml_data, grp.group(1), grp.group(2))
                except Exception:  # pylint: disable=broad-except
                    self.__logger.warning("Cannot parse %s", line)
        return yaml.load(yaml_data)

    def _extract_tempest_data(self):
        try:
            cmd = ['stestr', '--here', self.verifier_repo_dir, 'list',
                   '^tempest.']
            output = subprocess.check_output(cmd)
        except subprocess.CalledProcessError as cpe:
            self.__logger.error(
                "Exception when listing tempest tests: %s\n%s",
                cpe.cmd, cpe.output)
            raise
        yaml_data2 = ""
        for line in output.splitlines():
            try:
                grp = re.search(r'^([^\[]*)(\[.*\])\n*$', line)
                yaml_data2 = "{}\n{}: {}".format(
                    yaml_data2, grp.group(1), grp.group(2))
            except Exception:  # pylint: disable=broad-except
                self.__logger.warning("Cannot parse %s. skipping it", line)
        return yaml.load(yaml_data2)

    def generate_test_list(self, **kwargs):
        self.backup_tempest_config(self.conf_file, '/etc')
        refstack_data = self._extract_refstack_data()
        tempest_data = self._extract_tempest_data()
        with open(self.list, 'w') as ref_file:
            for key in refstack_data.keys():
                try:
                    for data in tempest_data[key]:
                        if data == refstack_data[key][0]:
                            break
                    else:
                        self.__logger.info("%s: ids differ. skipping it", key)
                        continue
                    ref_file.write("{}{}\n".format(
                        key, str(tempest_data[key]).replace(
                            "'", "").replace(", ", ",")))
                except Exception:  # pylint: disable=broad-except
                    self.__logger.info("%s: not found. skipping it", key)
                    continue
