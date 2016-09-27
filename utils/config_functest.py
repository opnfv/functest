import os
import subprocess

import yaml

import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("config_functest").getLogger()


def get_parameter_from_yaml(parameter, file):
    """
    Returns the value of a given parameter in file.yaml
    parameter must be given in string format with dots
    Example: general.openstack.image_name
    """
    with open(file) as f:
        file_yaml = yaml.safe_load(f)
    f.close()
    value = file_yaml
    for element in parameter.split("."):
        value = value.get(element)
        if value is None:
            raise ValueError("The parameter %s is not defined in"
                             " config_functest.yaml" % parameter)
    return value


class ConfigFunctest:
    config_functest = os.environ["CONFIG_FUNCTEST_YAML"]

    @property
    def functest_yaml(self):
        with self.config_functest as f:
            functest_yaml = yaml.safe_load(f)
        f.close()
        return functest_yaml

    @property
    def db_url(self):
        return self.get_config('results.test_db_url')

    @property
    def repos_dir(self):
        return self.get_config('general.directories.dir_repos')

    @property
    def results_dir(self):
        return self.get_config('general.directories.dir_results')

    @property
    def functest_conf_dir(self):
        return self.get_config('general.directories.dir_functest_conf')

    @property
    def functest_data_dir(self):
        return self.get_config('general.directories.dir_functest_data')

    @property
    def example_vm_name(self):
        return self.get_config('example.example_vm_name')

    @property
    def example_flavor(self):
        return self.get_config('example.example_flavor')

    @property
    def example_image_name(self):
        return self.get_config('example.example_image_name')

    @property
    def example_private_net_name(self):
        return self.get_config('example.example_private_net_name')

    @property
    def example_private_subnet_name(self):
        return self.get_config('example.example_private_subnet_name')

    @property
    def example_private_subnet_cidr(self):
        return self.get_config('example.example_private_subnet_cidr')

    @property
    def example_router_name(self):
        return self.get_config('example.example_router_name')

    @property
    def example_sg_name(self):
        return self.get_config('example.example_sg_name')

    @property
    def example_sg_descr(self):
        return self.get_config('example.example_sg_descr')

    @property
    def os_snapshot_file(self):
        return self.get_config('general.openstack.snapshot_file')

    @property
    def os_image_name(self):
        return self.get_config('general.openstack.image_name')

    @property
    def os_image_file(self):
        return self.get_config('general.openstack.image_file_name')

    @property
    def os_image_format(self):
        return self.get_config('general.openstack.image_disk_format')

    @property
    def os_flavor_name(self):
        return self.get_config('general.openstack.flavor_name')

    @property
    def os_flavor_ram(self):
        return self.get_config('general.openstack.flavor_ram')

    @property
    def os_flavor_disk(self):
        return self.get_config('general.openstack.flavor_disk')

    @property
    def os_flavor_vcpus(self):
        return self.get_config('general.openstack.flavor_vcpus')

    @property
    def onos_sfc_image_name(self):
        return self.get_config('onos_sfc.image_name')

    @property
    def onos_sfc_image_file(self):
        return self.get_config('onos_sfc.image_file_name')

    @property
    def onos_sfc_repo(self):
        return self.get_config('general.directories.dir_onos_sfc')

    @property
    def onos_bench_username(self):
        return self.get_config('ONOS.general.onosbench_username')

    @property
    def onos_bench_password(self):
        return self.get_config('ONOS.general.onosbench_password')

    @property
    def onos_cli_username(self):
        return self.get_config('ONOS.general.onoscli_username')

    @property
    def onos_cli_password(self):
        return self.get_config('ONOS.general.onoscli_password')

    @property
    def onos_run_timeout(self):
        return self.get_config('ONOS.general.runtimeout')

    @property
    def onos_env_oct(self):
        return self.get_config('ONOS.environment.OCT')

    @property
    def onos_env_oc1(self):
        return self.get_config('ONOS.environment.OC1')

    @property
    def onos_env_oc2(self):
        return self.get_config('ONOS.environment.OC2')

    @property
    def onos_env_oc3(self):
        return self.get_config('ONOS.environment.OC3')

    @property
    def onos_env_ocn(self):
        return self.get_config('ONOS.environment.OCN')

    @property
    def onos_env_ocn2(self):
        return self.get_config('ONOS.environment.OCN2')

    @property
    def onos_installer(self):
        return self.get_config('ONOS.environment.installer_master')

    @property
    def onos_installer_username(self):
        return self.get_config('ONOS.environment.installer_master_username')

    @property
    def onos_installer_password(self):
        return self.get_config('ONOS.environment.installer_master_password')

    @property
    def copper_repo(self):
        return self.get_config('general.directories.dir_repo_copper')

    @property
    def doctor_repo(self):
        return self.get_config('general.directories.dir_repo_doctor')

    @property
    def domino_repo(self):
        return self.get_config('general.directories.dir_repo_domino')

    @property
    def parser_repo(self):
        return self.get_config('general.directories.dir_repo_parser')

    @property
    def promise_repo(self):
        return self.get_config('general.directories.dir_repo_promise')

    @property
    def promise_tenant_name(self):
        return self.get_config('promise.tenant_name')

    @property
    def promise_tenant_description(self):
        return self.get_config('promise.tenant_description')

    @property
    def promise_username(self):
        return self.get_config('promise.user_name')

    @property
    def promise_password(self):
        return self.get_config('promise.user_pwd')

    @property
    def promise_image_name(self):
        return self.get_config('promise.image_name')

    @property
    def promise_flavor_name(self):
        return self.get_config('promise.flavor_name')

    @property
    def promise_flavor_cpus(self):
        return self.get_config('promise.flavor_vcpus')

    @property
    def promise_flavor_ram(self):
        return self.get_config('promise.flavor_ram')

    @property
    def promise_flavor_disk(self):
        return self.get_config('promise.flavor_disk')

    @property
    def promise_network_name(self):
        return self.get_config('promise.network_name')

    @property
    def promise_subnet_name(self):
        return self.get_config('promise.subnet_name')

    @property
    def promise_subnet_cidr(self):
        return self.get_config('promise.subnet_cidr')

    @property
    def promise_router_name(self):
        return self.get_config('promise.router_name')

    @property
    def tempest_repo(self):
        return self.get_config('general.directories.dir_repo_tempest')

    @property
    def tempest_private_net_name(self):
        return self.get_config('tempest.private_net_name')

    @property
    def tempest_private_subnet_name(self):
        return self.get_config('tempest.private_subnet_name')

    @property
    def tempest_private_subnet_cidr(self):
        return self.get_config('tempest.private_subnet_cidr')

    @property
    def tempest_router_name(self):
        return self.get_config('tempest.router_name')

    @property
    def tempest_tenant_name(self):
        return self.get_config('tempest.identity.tenant_name')

    @property
    def tempest_tenant_description(self):
        return self.get_config('tempest.identity.tenant_description')

    @property
    def tempest_username(self):
        return self.get_config('tempest.identity.user_name')

    @property
    def tempest_password(self):
        return self.get_config('tempest.identity.user_password')

    @property
    def tempest_ssh_timeout(self):
        return self.get_config('tempest.validation.ssh_timeout')

    @property
    def tempest_use_custom_images(self):
        return self.get_config('tempest.use_custom_images')

    @property
    def tempest_use_custom_flavors(self):
        return self.get_config('tempest.use_custom_flavors')

    @property
    def tempest_cases_dir(self):
        return self.get_config('general.directories.dir_tempest_cases')

    @property
    def rally_deployment_name(self):
        return self.get_config('rally.deployment_name')

    @property
    def rally_result_dir(self):
        return self.get_config('general.directories.dir_rally_res')

    @property
    def rally_inst_dir(self):
        return self.get_config('general.directories.dir_rally_inst')

    @property
    def rally_network_name(self):
        return self.get_config('rally.network_name')

    @property
    def rally_subnet_name(self):
        return self.get_config('rally.subnet_name')

    @property
    def rally_subnet_cidr(self):
        return self.get_config('rally.subnet_cidr')

    @property
    def rally_router_name(self):
        return self.get_config('rally.router_name')

    @property
    def rally_test_repo(self):
        return self.get_config('general.directories.dir_rally')

    @property
    def rally_deployment_dir(self):
        cmd = ("rally deployment list | awk '/" + self.rally_deployment_name +
               "/ {print $2}'")
        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        deployment_uuid = p.stdout.readline().rstrip()
        if deployment_uuid == "":
            logger.error("Rally deployment not found.")
            exit(-1)
        deployment_dir = (self.rally_inst_dir + "/tempest/for-deployment-" +
                          deployment_uuid)
        return deployment_dir

    def multisite_installer_username(self, installer):
        return self.get_config("multisite." +
                               installer +
                               "_environment.installer_username")

    def multisite_installer_password(self, installer):
        return self.get_config("multisite." +
                               installer +
                               "_environment.installer_password")

    @property
    def vping_vm_name_1(self):
        return self.get_config('vping.vm_name_1')

    @property
    def vping_vm_name_2(self):
        return self.get_config('vping.vm_name_2')

    @property
    def vping_ping_timeout(self):
        return self.get_config('vping.ping_timeout')

    @property
    def vping_image_name(self):
        return self.get_config('vping.image_name')

    @property
    def vping_flavor(self):
        return self.get_config('vping.vm_flavor')

    @property
    def vping_private_net_name(self):
        return self.get_config('vping.vping_private_net_name')

    @property
    def vping_private_subnet_name(self):
        return self.get_config('vping.vping_private_subnet_name')

    @property
    def vping_private_subnet_cidr(self):
        return self.get_config('vping.vping_private_subnet_cidr')

    @property
    def vping_router_name(self):
        return self.get_config('vping.vping_router_name')

    @property
    def vping_sg_name(self):
        return self.get_config('vping.vping_sg_name')

    @property
    def vping_sg_descr(self):
        return self.get_config('vping.vping_sg_descr')

    @property
    def vims_test_dir(self):
        return self.get_config('general.directories.dir_vIMS')

    @property
    def vims_data_dir(self):
        return self.get_config('general.directories.dir_vIMS_data')

    @property
    def vims_repo(self):
        return self.get_config('general.directories.dir_repo_vims_test')

    @property
    def vims_tenant_name(self):
        return self.get_config('vIMS.general.tenant_name')

    @property
    def vims_tenant_description(self):
        return self.get_config('vIMS.general.tenant_description')

    @property
    def vims_images(self):
        return self.get_config('vIMS.general.images')

    @property
    def vims_cloudify_blueprint(self):
        return self.get_config('vIMS.cloudify.blueprint')

    @property
    def vims_cloudify_requierments(self):
        return self.get_config('vIMS.cloudify.requierments')

    @property
    def vims_cloudify_inputs(self):
        return self.get_config('vIMS.cloudify.inputs')

    @property
    def vims_clearwater_blueprint(self):
        return self.get_config('vIMS.clearwater.blueprint')

    @property
    def vims_clearwater_deployment_name(self):
        return self.get_config('vIMS.clearwater.deployment-name')

    @property
    def vims_clearwater_inputs(self):
        return self.get_config('vIMS.clearwater.inputs')

    @property
    def vims_clearwater_requierments(self):
        return self.get_config('vIMS.clearwater.requierments')

    @property
    def flavor_extra_specs(self):
        return self.get_config('general.flavor_extra_specs')

    @property
    def image_properties(self):
        return self.get_config('general.image_properties')

    def get_config(self, parameter):
        return get_parameter_from_yaml(parameter, self.config_functest)


CONF = ConfigFunctest()
