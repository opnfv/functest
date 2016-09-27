import os
import subprocess

import yaml

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils

logger = ft_logger.Logger("config_functest").getLogger()


def get_functest_config(parameter):
    yaml_ = os.environ["CONFIG_FUNCTEST_YAML"]
    return ft_utils.get_parameter_from_yaml(parameter, yaml_)


def get_functest_yaml():
    with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
        functest_yaml = yaml.safe_load(f)
    f.close()
    return functest_yaml


def get_deployment_dir():
    """
    Returns current Rally deployment directory
    """
    deployment_name = get_functest_config('rally.deployment_name')
    rally_dir = get_functest_config('general.directories.dir_rally_inst')
    cmd = ("rally deployment list | awk '/" + deployment_name +
           "/ {print $2}'")
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    deployment_uuid = p.stdout.readline().rstrip()
    if deployment_uuid == "":
        logger.error("Rally deployment not found.")
        exit(-1)
    deployment_dir = (rally_dir + "/tempest/for-deployment-" +
                      deployment_uuid)
    return deployment_dir


def get_db_url():
    """
    Returns DB URL
    """
    return get_functest_config('results.test_db_url')