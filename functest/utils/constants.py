#!/usr/bin/env python

# pylint: disable=missing-docstring

import pkg_resources

CONFIG_FUNCTEST_YAML = pkg_resources.resource_filename(
    'functest', 'ci/config_functest.yaml')

ENV_FILE = '/home/opnfv/functest/conf/env_file'
