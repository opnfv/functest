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


class IntelNfvCi(tempest.TempestCommon):

    __logger = logging.getLogger(__name__)

    def configure(self, **kwargs):
        super(IntelNfvCi, self).configure(**kwargs)
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        rconfig.add_section('intel_nfv_ci')
        rconfig.set('intel_nfv_ci', 'qemu_ssh_user',
                    kwargs.get('qemu_ssh_user', 'ubuntu'))
        rconfig.set('intel_nfv_ci', 'qemu_ssh_private_key_path',
                    kwargs.get('qemu_ssh_private_key_path',
                               '/root/.ssh/id_rsa'))
        with open(self.conf_file, 'wb') as config_file:
            rconfig.write(config_file)
        self.backup_tempest_config(self.conf_file, self.res_dir)
