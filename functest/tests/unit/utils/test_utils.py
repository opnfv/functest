#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import unittest
import urllib2

from functest.utils import functest_utils


class FunctestUtilsTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.url = 'http://www.opnfv.org/'
        self.timeout = 5

    @mock.patch('urllib2.urlopen',
                side_effect=urllib2.URLError('no host given'))
    def test_check_internet_connectivity_failed(self, mock_method):
        self.assertFalse(functest_utils.check_internet_connectivity())
        mock_method.assert_called_once_with(self.url, timeout=self.timeout)

    @mock.patch('urllib2.urlopen')
    def test_check_internet_connectivity_default(self, mock_method):
        self.assertTrue(functest_utils.check_internet_connectivity())
        mock_method.assert_called_once_with(self.url, timeout=self.timeout)

    @mock.patch('urllib2.urlopen')
    def test_check_internet_connectivity_debian(self, mock_method):
        self.url = "https://www.debian.org/"
        self.assertTrue(functest_utils.check_internet_connectivity(self.url))
        mock_method.assert_called_once_with(self.url, timeout=self.timeout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
