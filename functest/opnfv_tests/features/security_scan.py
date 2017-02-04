#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

import os
import paramiko

import functest.core.feature_base as base
from functest.utils.constants import CONST


class SecurityScan(base.FeatureBase):
    def __init__(self):
        super(SecurityScan, self).__init__(project='security_scan',
                                           case='security_scan',
                                           repo='dir_repo_securityscan')
        self.cmd = ('bash {0} && '
                    'cd {1} && '
                    'python security_scan.py --config config.ini && '
                    'cd -'.format(CONST.openstack_creds,
                                  self.repo))
        self.rsa_key_file = '/root/.ssh/id_rsa'

    def prepare(self):
        self.logger.debug('Generating RSA key...')
        rsa_key = paramiko.RSAKey.generate(bits=2048, progress_func=None)
        self.logger.debug('Saving the RSA private key...')
        rsa_key.write_private_key_file(self.rsa_key_file)
        del rsa_key

    def post(self):
        if os.path.exists(self.rsa_key_file):
            try:
                self.logger.debug('Removing RSA key file')
                os.remove(self.rsa_key_file)
            except Exception as e:
                self.logger.debug('Error when removing the RSA key: %s'
                                  % e)
