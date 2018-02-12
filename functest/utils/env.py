#!/usr/bin/env python

# pylint: disable=missing-docstring

import os
import re

import pkg_resources
import six


class Environment(object):  # pylint: disable=too-few-public-methods

    default_envs = {
        'NODE_NAME': 'unknown_pod',
        'DEPLOY_SCENARIO': 'os-nosdn-nofeature-noha',
        'DEPLOY_TYPE': 'virt',
        'INSTALLER_TYPE': None,
        'INSTALLER_IP': None,
        'BUILD_TAG': None,
        'OS_ENDPOINT_TYPE': None,
        'OS_AUTH_URL': None,
        'CONFIG_FUNCTEST_YAML': pkg_resources.resource_filename(
            'functest', 'ci/config_functest.yaml'),
        'OS_INSECURE': '',
        'OS_REGION_NAME': 'RegionOne'
    }

    def __init__(self):
        for key, value in six.iteritems(os.environ):
            setattr(self, key, value)
        for key, value in six.iteritems(self.default_envs):
            if key not in os.environ:
                setattr(self, key, value)
        self._set_ci_run()
        if 'CI_LOOP' not in os.environ:
            self._set_ci_loop()

    def _set_ci_run(self):
        if getattr(self, "BUILD_TAG"):
            setattr(self, "IS_CI_RUN", True)
        else:
            setattr(self, "IS_CI_RUN", False)

    def _set_ci_loop(self):
        if (getattr(self, "BUILD_TAG") and
                re.search("daily", getattr(self, "BUILD_TAG"))):
            setattr(self, "CI_LOOP", "daily")
        else:
            setattr(self, "CI_LOOP", "weekly")


ENV = Environment()
