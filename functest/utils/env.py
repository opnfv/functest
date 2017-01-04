import os
import re

default_envs = {
    'NODE_NAME': 'unknown_pod',
    'CI_DEBUG': 'true',
    'DEPLOY_SCENARIO': 'os-nosdn-nofeature-noha',
    'DEPLOY_TYPE': 'virt',
    'INSTALLER_TYPE': None,
    'INSTALLER_IP': None,
    'BUILD_TAG': None,
    'OS_ENDPOINT_TYPE': None,
    'OS_AUTH_URL': None
}


class Environment(object):

    def __init__(self):
        for k, v in os.environ.iteritems():
            self.__setattr__(k, v)
        for k, v in default_envs.iteritems():
            if k not in os.environ:
                self.__setattr__(k, v)
        self._set_ci_run()
        self._set_ci_loop()
        self._set_version()

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

    def _set_version(self):
        """
        Get version
        """
        # Use the build tag to retrieve the version
        # By default version is unknown
        # if launched through CI the build tag has the following format
        # jenkins-<project>-<installer>-<pod>-<job>-<branch>-<id>
        # e.g. jenkins-functest-fuel-opnfv-jump-2-daily-master-190
        # use regex to match branch info
        rule = "daily-(.+?)-[0-9]*"
        if self.BUILD_TAG:
            m = re.search(rule, self.BUILD_TAG)
            if m:
                self.VERSION = m.group(1)
            else:
                self.VERSION = "unknown"
        else:
            self.VERSION = "unknown"


ENV = Environment()
