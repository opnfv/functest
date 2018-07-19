#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock

from functest.opnfv_tests.vnf.ims import clearwater


class ClearwaterTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os.makedirs'):
            self.ims_vnf = clearwater.ClearwaterTesting("foo", "0.0.0.0")

        self.mock_post = mock.Mock()
        attrs = {'status_code': 201,
                 'cookies': ""}
        self.mock_post.configure_mock(**attrs)

        self.mock_post_200 = mock.Mock()
        attrs = {'status_code': 200,
                 'cookies': ""}
        self.mock_post_200.configure_mock(**attrs)

        self.mock_post_500 = mock.Mock()
        attrs = {'status_code': 500,
                 'cookies': ""}
        self.mock_post_200.configure_mock(**attrs)

if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
