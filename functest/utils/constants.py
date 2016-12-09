import config
import env


class Constant(object):
    def __init__(self):
        for attr_n in dir(config.CONF):
            if not (attr_n.startswith('__') and attr_n.endswith('__')):
                self.__setattr__(attr_n, config.CONF.__getattribute__(attr_n))
        for env_n, env_v in env.ENV.__dict__.iteritems():
            self.__setattr__(env_n, env_v)


const = Constant()

if __name__ == '__main__':
    print const.NODE_NAME
    print const.vIMS_clearwater_blueprint_url
    print const.vIMS_clearwater_blueprint_file_name
    print const.vIMS_clearwater_blueprint_name
