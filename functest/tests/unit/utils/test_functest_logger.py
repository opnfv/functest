#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.utils import functest_logger
from functest.utils.constants import CONST


class OSUtilsLogger(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        with mock.patch('__builtin__.open', mock.mock_open()):
            with mock.patch('functest.utils.functest_logger.os.path.exists',
                            return_value=True), \
                mock.patch('functest.utils.functest_logger.'
                           'json.load'), \
                mock.patch('functest.utils.functest_logger.'
                           'logging.config.dictConfig') as m:
                self.logger = functest_logger.Logger('os_utils')
                self.assertTrue(m.called)
            with mock.patch('functest.utils.functest_logger.os.path.exists',
                            return_value=False), \
                mock.patch('functest.utils.functest_logger.'
                           'logging.basicConfig') as m:
                self.logger = functest_logger.Logger('os_utils')
                self.assertTrue(m.called)

    def test_is_debug_false(self):
        CONST.CI_DEBUG = False
        self.assertFalse(self.logger.is_debug())

    def test_is_debug_true(self):
        CONST.CI_DEBUG = "True"
        self.assertTrue(self.logger.is_debug())


if __name__ == "__main__":
    unittest.main(verbosity=2)
