#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import unittest

from functest.ci import run_tests as rt


class AnyStringWith(str):
    def __eq__(self, other):
        if self in other:
            return True
        return False


class RunTestsTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    @mock.patch('functest.ci.run_tests.logger.info')
    def test_print_separator_default(self, mock_logger_info):
        count = 45
        rt.print_separator()
        line = ""
        for i in range(0, count - 1):
            line += str
        mock_logger_info.mock_logger_info.assert_called_once_with(line)


if __name__ == "__main__":
    unittest.main(verbosity=2)
