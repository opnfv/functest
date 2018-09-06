#!/usr/bin/env python

# pylint: disable=missing-docstring

import pkg_resources
import yaml

import six

from functest.utils import env


class Config(object):
    def __init__(self):
        try:
            # pylint: disable=bad-continuation
            with open(pkg_resources.resource_filename(
                    'functest', 'ci/config_functest.yaml')) as yfile:
                self.functest_yaml = yaml.safe_load(yfile)
        except Exception as error:
            raise Exception('Parse config failed: {}'.format(str(error)))

    @staticmethod
    def _merge_dicts(dict1, dict2):
        for k in set(dict1.keys()).union(dict2.keys()):
            if k in dict1 and k in dict2:
                if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                    yield (k, dict(Config._merge_dicts(dict1[k], dict2[k])))
                else:
                    yield (k, dict2[k])
            elif k in dict1:
                yield (k, dict1[k])
            else:
                yield (k, dict2[k])

    def patch_file(self, patch_file_path):
        with open(patch_file_path) as yfile:
            patch_file = yaml.safe_load(yfile)

        for key in patch_file:
            if key in env.get('DEPLOY_SCENARIO'):
                self.functest_yaml = dict(Config._merge_dicts(
                    self.functest_yaml, patch_file[key]))

    def _parse(self, attr_now, left_parametes):
        for param_n, param_v in six.iteritems(left_parametes):
            attr_further = self._get_attr_further(attr_now, param_n)
            if attr_further:
                setattr(self, attr_further, param_v)
            if isinstance(param_v, dict):
                self._parse(attr_further, param_v)

    @staticmethod
    def _get_attr_further(attr_now, next):  # pylint: disable=redefined-builtin
        return attr_now if next == 'general' else (
            '{}_{}'.format(attr_now, next) if attr_now else next)

    def fill(self):
        try:
            self._parse(None, self.functest_yaml)
        except Exception as error:
            raise Exception('Parse config failed: {}'.format(str(error)))


CONF = Config()
CONF.patch_file(pkg_resources.resource_filename(
    'functest', 'ci/config_patch.yaml'))
if env.get('VOLUME_DEVICE_TYPE'):
    CONF.patch_file(pkg_resources.resource_filename(
        'functest', 'ci/config_disk_type_patch.yaml'))
if env.get("POD_ARCH") in ['aarch64']:
    CONF.patch_file(pkg_resources.resource_filename(
        'functest', 'ci/config_aarch64_patch.yaml'))
CONF.fill()
