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
import shutil
import time

from refstack_client import list_parser
from xtesting.core import testcase
from xtesting.energy import energy

from functest.opnfv_tests.openstack.tempest import tempest
from functest.utils import config


class Refstack(tempest.TempestCommon):
    """Refstack testcase implementation class."""

    __logger = logging.getLogger(__name__)

    defcorelist = os.path.join(
        getattr(config.CONF, 'dir_refstack_data'), 'defcore.txt')

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'refstack'
        super(Refstack, self).__init__(**kwargs)
        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), 'refstack')
        self.list = os.path.join(self.res_dir, 'tempest-list.txt')

    @energy.enable_recording
    def run(self, **kwargs):
        """Start Refstack testcase."""
        self.start_time = time.time()
        try:
            self.configure()
            parser = list_parser.TestListParser(
                getattr(config.CONF, 'dir_repo_tempest'))
            nfile = parser.get_normalized_test_list(Refstack.defcorelist)
            shutil.copyfile(nfile, self.list)
            self.run_verifier_tests()
            self.parse_verifier_result()
            self.generate_report()
            res = testcase.TestCase.EX_OK
        except Exception as err:  # pylint: disable=broad-except
            self.__logger.error('Error with run: %s', err)
            res = testcase.TestCase.EX_RUN_ERROR
        finally:
            self.resources.cleanup()
        self.stop_time = time.time()
        return res
