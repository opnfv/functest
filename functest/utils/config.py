#!/usr/bin/env python

import yaml

import six

from functest.utils import env


class Config(object):
    def __init__(self):
        try:
            with open(env.ENV.CONFIG_FUNCTEST_YAML) as f:
                self.functest_yaml = yaml.safe_load(f)
                self._parse(None, self.functest_yaml)
        except Exception as error:
            raise Exception('Parse config failed: {}'.format(str(error)))
        self._set_others()

    def _parse(self, attr_now, left_parametes):
        for param_n, param_v in six.iteritems(left_parametes):
            attr_further = self._get_attr_further(attr_now, param_n)
            if attr_further:
                self.__setattr__(attr_further, param_v)
            if isinstance(param_v, dict):
                self._parse(attr_further, param_v)

    def _get_attr_further(self, attr_now, next):
        return attr_now if next == 'general' else (
            '{}_{}'.format(attr_now, next) if attr_now else next)


CONF = Config()
