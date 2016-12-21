import config
import env
import os


class Constants(object):
    def __init__(self):
        for attr_n, attr_v in config.CONF.__dict__.iteritems():
            self.__setattr__(attr_n, attr_v)
        for env_n, env_v in env.ENV.__dict__.iteritems():
            self.__setattr__(env_n, env_v)

        if hasattr(self, 'BUILD_TAG') and self.BUILD_TAG:
            self.IS_CI_RUN = True
        else:
            self.IS_CI_RUN = False
        self.env_active = os.path.join(self.dir_functest_conf, "env_active")

CONST = Constants()

if __name__ == '__main__':
    print CONST.__dict__
    print CONST.NODE_NAME
    print CONST.vIMS_clearwater_blueprint_url
    print CONST.vIMS_clearwater_blueprint_file_name
    print CONST.vIMS_clearwater_blueprint_name
