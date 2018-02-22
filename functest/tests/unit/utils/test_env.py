#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import os
import unittest

from six.moves import reload_module

from functest.utils import env


class EnvTesting(unittest.TestCase):
    # pylint: disable=missing-docstring

    def setUp(self):
        os.environ['FOO'] = 'foo'
        os.environ['BUILD_TAG'] = 'master'
        os.environ['CI_LOOP'] = 'weekly'

    def test_get_unset_unknown_env(self):
        del os.environ['FOO']
        self.assertEqual(env.get('FOO'), None)

    def test_get_unknown_env(self):
        self.assertEqual(env.get('FOO'), 'foo')
        reload_module(env)

    def test_get_unset_env(self):
        del os.environ['CI_LOOP']
        self.assertEqual(
            env.get('CI_LOOP'), env.INPUTS['CI_LOOP'])

    def test_get_env(self):
        self.assertEqual(
            env.get('CI_LOOP'), 'weekly')

    def test_get_unset_env2(self):
        del os.environ['BUILD_TAG']
        self.assertEqual(
            env.get('BUILD_TAG'), env.INPUTS['BUILD_TAG'])

    def test_get_env2(self):
        self.assertEqual(env.get('BUILD_TAG'), 'master')


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
