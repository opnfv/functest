#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the class required to fully cover shaker."""

import logging
import unittest

import mock
import shade

from functest.opnfv_tests.openstack.shaker import shaker

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"


class ShakerTesting(unittest.TestCase):

    """The super class which testing classes could inherit."""
    # pylint: disable=missing-docstring

    logging.disable(logging.CRITICAL)

    def setUp(self):
        with mock.patch('os_client_config.get_config'), \
                mock.patch('shade.OpenStackCloud'):
            self.test = shaker.Shaker()

    def test_create_sg_rules_ko1(self):
        self.test.cloud = None
        with self.assertRaises(AssertionError):
            self.test.create_sg_rules()

    def test_create_sg_rules_ko2(self):
        self.test.cloud.create_security_group_rule.side_effect = shade.OpenStackCloudException(None)
        with self.assertRaises(shade.OpenStackCloudException):
            self.test.create_sg_rules()
        self.test.cloud.create_security_group_rule.has_been_called_once_with()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
