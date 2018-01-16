#!/usr/bin/env python

import pkg_resources
import os
import re

import six


default_envs = {
    'NODE_NAME': 'unknown_pod',
    'CI_DEBUG': 'false',
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


class Environment(object):

    def __init__(self):
        for k, v in six.iteritems(os.environ):
            self.__setattr__(k, v)
        for k, v in six.iteritems(default_envs):
            if k not in os.environ:
                self.__setattr__(k, v)
        self._set_ci_run()
        if 'CI_LOOP' not in os.environ:
            self._set_ci_loop()

    def _set_ci_run(self):
        if self.BUILD_TAG:
            self.IS_CI_RUN = True
        else:
            self.IS_CI_RUN = False

    def _set_ci_loop(self):
        if self.BUILD_TAG and re.search("daily", self.BUILD_TAG):
            self.CI_LOOP = "daily"
        else:
            self.CI_LOOP = "weekly"


ENV = Environment()
