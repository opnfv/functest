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
from functest.utils import constants


class EnvTesting(unittest.TestCase):
    # pylint: disable=missing-docstring

    def setUp(self):
        os.environ['FOO'] = 'foo'
        os.environ['BUILD_TAG'] = 'master'
        os.environ['CI_LOOP'] = 'weekly'

    def test_get_unset_unknown_env(self):
        del os.environ['FOO']
        self.assertEqual(env.Environment.get('FOO'), None)
        # Backward compatibilty (waiting for SDNVPN and SFC)
        reload_module(env)
        with self.assertRaises(AttributeError):
            getattr(env.ENV, 'FOO')
        reload_module(constants)
        with self.assertRaises(AttributeError):
            getattr(constants.CONST, 'FOO')

    def test_get_unknown_env(self):
        self.assertEqual(env.Environment.get('FOO'), 'foo')
        reload_module(env)
        # Backward compatibilty (waiting for SDNVPN and SFC)
        with self.assertRaises(AttributeError):
            getattr(env.ENV, 'FOO')
        reload_module(constants)
        with self.assertRaises(AttributeError):
            getattr(constants.CONST, 'FOO')

    def test_get_unset_env(self):
        del os.environ['CI_LOOP']
        self.assertEqual(
            env.Environment.get('CI_LOOP'), env.Environment.inputs['CI_LOOP'])
        # Backward compatibilty (waiting for SDNVPN and SFC)
        reload_module(env)
        self.assertEqual(
            getattr(env.ENV, 'CI_LOOP'), env.Environment.inputs['CI_LOOP'])
        reload_module(constants)
        self.assertEqual(
            getattr(constants.CONST, 'CI_LOOP'),
            env.Environment.inputs['CI_LOOP'])

    def test_get_env(self):
        self.assertEqual(
            env.Environment.get('CI_LOOP'), 'weekly')
        # Backward compatibilty (waiting for SDNVPN and SFC)
        reload_module(env)
        self.assertEqual(getattr(env.ENV, 'CI_LOOP'), 'weekly')
        reload_module(constants)
        self.assertEqual(getattr(constants.CONST, 'CI_LOOP'), 'weekly')

    def test_get_unset_env2(self):
        del os.environ['BUILD_TAG']
        self.assertEqual(
            env.Environment.get('BUILD_TAG'),
            env.Environment.inputs['BUILD_TAG'])
        # Backward compatibilty (waiting for SDNVPN and SFC)
        reload_module(env)
        self.assertEqual(
            getattr(env.ENV, 'BUILD_TAG'), env.Environment.inputs['BUILD_TAG'])
        reload_module(constants)
        self.assertEqual(
            getattr(constants.CONST, 'BUILD_TAG'),
            env.Environment.inputs['BUILD_TAG'])

    def test_get_env2(self):
        self.assertEqual(
            env.Environment.get('BUILD_TAG'), 'master')
        # Backward compatibilty (waiting for SDNVPN and SFC)
        reload_module(env)
        self.assertEqual(getattr(env.ENV, 'BUILD_TAG'), 'master')
        reload_module(env)
        self.assertEqual(getattr(constants.CONST, 'BUILD_TAG'), 'master')


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
