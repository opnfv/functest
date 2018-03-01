#!/usr/bin/env python

# pylint: disable=missing-docstring

import pkg_resources
from xtesting.utils import constants

CONFIG_FUNCTEST_YAML = pkg_resources.resource_filename(
    'functest', 'ci/config_functest.yaml')

ENV_FILE = constants.ENV_FILE
