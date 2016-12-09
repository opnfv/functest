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
            raise 'safe_load {} failed'.format(self.config_functest)

    @property
    def db_url(self):
        return self.__get_attribute__('results.test_db_url')

    @property
    def repos_dir(self):
        return self.__get_attribute__('general.directories.dir_repos')

    @property
    def results_dir(self):
        return self.__get_attribute__('general.directories.dir_results')

    @property
    def functest_conf_dir(self):
        return self.__get_attribute__('general.directories.dir_functest_conf')

    @property
    def functest_data_dir(self):
        return self.__get_attribute__('general.directories.dir_functest_data')

    @property
    def example_vm_name(self):
        return self.__get_attribute__('example.example_vm_name')

    @property
    def example_flavor(self):
        return self.__get_attribute__('example.example_flavor')

    @property
    def example_image_name(self):
        return self.__get_attribute__('example.example_image_name')

    @property
    def example_private_net_name(self):
        return self.__get_attribute__('example.example_private_net_name')

    @property
    def example_private_subnet_name(self):
        return self.__get_attribute__('example.example_private_subnet_name')

    @property
    def example_private_subnet_cidr(self):
        return self.__get_attribute__('example.example_private_subnet_cidr')

    @property
    def example_router_name(self):
        return self.__get_attribute__('example.example_router_name')

    @property
    def example_sg_name(self):
        return self.__get_attribute__('example.example_sg_name')

    @property
    def example_sg_descr(self):
        return self.__get_attribute__('example.example_sg_descr')

    @property
    def os_snapshot_file(self):
        return self.__get_attribute__('general.openstack.snapshot_file')

    @property
    def os_image_name(self):
        return self.__get_attribute__('general.openstack.image_name')

    @property
    def os_image_file(self):
        return self.__get_attribute__('general.openstack.image_file_name')

    @property
    def os_image_format(self):
        return self.__get_attribute__('general.openstack.image_disk_format')

    @property
    def os_flavor_name(self):
        return self.__get_attribute__('general.openstack.flavor_name')

    @property
    def os_flavor_ram(self):
        return self.__get_attribute__('general.openstack.flavor_ram')

    @property
    def os_flavor_disk(self):
        return self.__get_attribute__('general.openstack.flavor_disk')

    @property
    def os_flavor_vcpus(self):
        return self.__get_attribute__('general.openstack.flavor_vcpus')

    @property
    def onos_sfc_image_name(self):
        return self.__get_attribute__('onos_sfc.image_name')

    @property
    def onos_sfc_image_file(self):
        return self.__get_attribute__('onos_sfc.image_file_name')

    @property
    def onos_sfc_repo(self):
        return self.__get_attribute__('general.directories.dir_onos_sfc')

    @property
    def onos_bench_username(self):
        return self.__get_attribute__('ONOS.general.onosbench_username')

    @property
    def onos_bench_password(self):
        return self.__get_attribute__('ONOS.general.onosbench_password')

    @property
    def onos_cli_username(self):
        return self.__get_attribute__('ONOS.general.onoscli_username')

    @property
    def onos_cli_password(self):
        return self.__get_attribute__('ONOS.general.onoscli_password')

    @property
    def onos_run_timeout(self):
        return self.__get_attribute__('ONOS.general.runtimeout')

    @property
    def onos_env_oct(self):
        return self.__get_attribute__('ONOS.environment.OCT')

    @property
    def onos_env_oc1(self):
        return self.__get_attribute__('ONOS.environment.OC1')

    @property
    def onos_env_oc2(self):
        return self.__get_attribute__('ONOS.environment.OC2')

    @property
    def vIMS_clearwater_blueprint_url(self):
        return self.__get_attribute__('vIMS.clearwater.blueprint.url')

    @property
    def vIMS_clearwater_blueprint_file_name(self):
        return self.__get_attribute__('vIMS.clearwater.blueprint.file_name')

    @property
    def vIMS_clearwater_blueprint_name(self):
        return self.__get_attribute__('vIMS.clearwater.blueprint.name')

    def __get_attribute__(self, attr):
        if self.functest_yaml:
            value = self.functest_yaml
            for element in attr.split("."):
                value = value.get(element)
                if value is None:
                    raise AttributeError("The attribute %s is not defined in"
                                         " %s" % (attr, self.config_functest))
            return value
        else:
            raise Exception("Please check CONFIG_FUNCTEST_YAML in env")


CONF = Config()
