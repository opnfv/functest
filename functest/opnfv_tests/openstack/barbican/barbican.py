#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging

from six.moves import configparser

from functest.opnfv_tests.openstack.tempest import tempest


class Barbican(tempest.TempestCommon):

    __logger = logging.getLogger(__name__)

    def configure(self, **kwargs):
        super(Barbican, self).configure(**kwargs)
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        rconfig.add_section('auth')
        rconfig.set('auth', 'tempest_roles', 'creator')
        rconfig.add_section('glance')
        rconfig.set('glance', 'verify_glance_signatures', True)
        rconfig.add_section('ephemeral_storage_encryption')
        rconfig.set('ephemeral_storage_encryption', 'key_size', 256)
        rconfig.set(
            'ephemeral_storage_encryption', 'cipher', 'aes-xts-plain64')
        rconfig.set('ephemeral_storage_encryption', 'enabled', True)
        rconfig.add_section('image-feature-enabled')
        rconfig.set('image-feature-enabled', 'api_v1', False)
        with open(self.conf_file, 'wb') as config_file:
            rconfig.write(config_file)
        self.backup_tempest_config(self.conf_file, self.res_dir)
