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

    def _extract_refstack_data(self, refstack_list):
        yaml_data = ""
        with open(refstack_list, encoding='utf-8') as def_file:
            for line in def_file:
                try:
                    grp = re.search(r'^([^\[]*)(\[.*\])\n*$', line)
                    yaml_data = f"{yaml_data}\n{grp.group(1)}: {grp.group(2)}"
                except Exception:  # pylint: disable=broad-except
                    self.__logger.warning("Cannot parse %s", line)
        return yaml.full_load(yaml_data)

    def _extract_tempest_data(self):
        olddir = os.getcwd()
        try:
            os.chdir(self.verifier_repo_dir)
            cmd = ['stestr', 'list', '^tempest.']
            output = subprocess.check_output(cmd)
        except subprocess.CalledProcessError as cpe:
            self.__logger.error(
                "Exception when listing tempest tests: %s\n%s",
                cpe.cmd, cpe.output.decode("utf-8"))
            raise
        finally:
            os.chdir(olddir)
        yaml_data2 = ""
        for line in output.splitlines():
            try:
                grp = re.search(r'^([^\[]*)(\[.*\])\n*$', line.decode("utf-8"))
                yaml_data2 = f"{yaml_data2}\n{grp.group(1)}: {grp.group(2)}"
            except Exception:  # pylint: disable=broad-except
                self.__logger.warning("Cannot parse %s. skipping it", line)
        return yaml.full_load(yaml_data2)

    def generate_test_list(self, **kwargs):
        refstack_list = os.path.join(
            getattr(config.CONF, 'dir_refstack_data'),
            f"{kwargs.get('target', 'compute')}.txt")
        self.backup_tempest_config(self.conf_file, '/etc')
        refstack_data = self._extract_refstack_data(refstack_list)
        tempest_data = self._extract_tempest_data()
        with open(self.list, 'w', encoding='utf-8') as ref_file:
            for key in refstack_data.keys():
                try:
                    for data in tempest_data[key]:
                        if data == refstack_data[key][0]:
                            break
                    else:
                        self.__logger.info("%s: ids differ. skipping it", key)
                        continue
                    value = str(tempest_data[key]).replace(
                        "'", "").replace(", ", ",")
                    ref_file.write(f"{key}{value}\n")
                except Exception:  # pylint: disable=broad-except
                    self.__logger.info("%s: not found. skipping it", key)
                    continue
