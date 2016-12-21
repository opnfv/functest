import os

default_envs = {
    'NODE_NAME': 'unknown_pod',
    'CI_DEBUG': 'true',
    'DEPLOY_SCENARIO': 'os-nosdn-nofeature-ha',
}


class Environment(object):
    def __init__(self):
        for k, v in os.environ.iteritems():
            self.__setattr__(k, v)
        for k, v in default_envs.iteritems():
            if k not in os.environ:
                self.__setattr__(k, v)


ENV = Environment()
