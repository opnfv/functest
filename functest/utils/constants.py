#!/usr/bin/env python

# pylint: disable=missing-docstring

import pkg_resources
import six

from functest.utils import config
from functest.utils import env


class Constants(object):  # pylint: disable=too-few-public-methods

    CONFIG_FUNCTEST_YAML = pkg_resources.resource_filename(
        'functest', 'ci/config_functest.yaml')

    def __init__(self):
        for attr_n, attr_v in six.iteritems(config.CONF.__dict__):
            setattr(self, attr_n, attr_v)
        for env_n, env_v in six.iteritems(env.ENV.__dict__):
            setattr(self, env_n, env_v)


CONST = Constants()
