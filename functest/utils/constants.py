#!/usr/bin/env python

import six

from functest.utils import config
from functest.utils import env


class Constants(object):
    def __init__(self):
        for attr_n, attr_v in six.iteritems(config.CONF.__dict__):
            self.__setattr__(attr_n, attr_v)
        for env_n, env_v in six.iteritems(env.ENV.__dict__):
            self.__setattr__(env_n, env_v)


CONST = Constants()
