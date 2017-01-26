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
        except:
            raise Exception('Parse {} failed'.format(self.config_functest))


CONF = Config()
