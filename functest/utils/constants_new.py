import config_new as config
import env


class Constants(object):
    def __init__(self):
        for attr_n, attr_v in config.CONF.__dict__.iteritems():
            self.__setattr__(attr_n, attr_v)
        for env_n, env_v in env.ENV.__dict__.iteritems():
            self.__setattr__(env_n, env_v)

    def __getattr__(self, key):
        dict_key = key.split('_')
        if dict_key and len(dict_key) >= 1:
            dict_one_key = dict_key.pop(0)
            value = config.CONF.functest_yaml.get(dict_one_key)
            if not dict_key:
                if value is None:
                    raise ValueError("The key '%s' is not found" % key)
                return value
            for element in dict_key:
                value = value.get(element)
                if value is None:
                    raise ValueError("The key '%s' is not found" % key)
                return value


CONST = Constants()

if __name__ == '__main__':
    # print CONST.__dict__
    print CONST.NODE_NAME
    print CONST.vnf_aaa
    print CONST.ONOS
    print CONST.ONOS_environment
    print CONST.ONOS_environment_OCT
    print CONST.general_dir
