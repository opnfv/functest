import os

import yaml


class Config(object):
    def __init__(self):
        if 'CONFIG_FUNCTEST_YAML' not in os.environ:
            raise Exception('CONFIG_FUNCTEST_YAML not configed')
        self.config_functest = os.environ['CONFIG_FUNCTEST_YAML']
        try:
            with open(self.config_functest) as f:
                self.functest_yaml = yaml.safe_load(f)
                self._parse(None, self.functest_yaml)
        except:
            raise Exception('Parse {} failed'.format(self.config_functest))
        self._set_others()

    def _parse(self, attr_now, left_parametes):
        for param_n, param_v in left_parametes.iteritems():
            attr_further = self._get_attr_further(attr_now, param_n)
            if not isinstance(param_v, dict):
                self.__setattr__(attr_further, param_v)
            else:
                self._parse(attr_further, param_v)

    def _get_attr_further(self, attr_now, next):
        return attr_now if next == 'general' else (
            '{}_{}'.format(attr_now, next) if attr_now else next)

    def _set_others(self):
        self.env_active = os.path.join(self.dir_functest_conf, "env_active")


CONF = Config()
