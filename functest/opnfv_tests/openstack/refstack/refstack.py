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

from refstack_client import list_parser

from functest.opnfv_tests.openstack.tempest import tempest
from functest.utils import config


class Refstack(tempest.TempestCommon):
    """Refstack testcase implementation class."""

    __logger = logging.getLogger(__name__)

    defcorelist = os.path.join(
        getattr(config.CONF, 'dir_refstack_data'), 'defcore.txt')

    def generate_test_list(self, **kwargs):
        parser = list_parser.TestListParser(
            getattr(config.CONF, 'dir_repo_tempest'))
        nfile = parser.get_normalized_test_list(Refstack.defcorelist)
        shutil.copyfile(nfile, self.list)
