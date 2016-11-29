#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import os
import subprocess

from oslo_utils import importutils
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("openstack_utils").getLogger()


class MissingEnvVar(Exception):

    def __init__(self, var):
        self.var = var

    def __str__(self):
        return str.format("Please set the mandatory env var: {}", self.var)


def source_credentials(rc_file):
    pipe = subprocess.Popen(". %s; env" % rc_file, stdout=subprocess.PIPE,
                            shell=True)
    output = pipe.communicate()[0]
    env = dict((line.split("=", 1) for line in output.splitlines()))
    os.environ.update(env)
    return env


def check_credentials():
    """
    Check if the OpenStack credentials (openrc) are sourced
    """
    env_vars = ['OS_AUTH_URL', 'OS_USERNAME', 'OS_PASSWORD', 'OS_TENANT_NAME']
    return all(map(lambda v: v in os.environ and os.environ[v], env_vars))


def get_credentials(service):
    """Returns a creds dictionary filled with the following keys:
    * username
    * password/api_key (depending on the service)
    * tenant_name/project_id (depending on the service)
    * auth_url
    :param service: a string indicating the name of the service
                    requesting the credentials.
    """
    creds = {}

    # Check that the env vars exists:
    envvars = ('OS_USERNAME', 'OS_PASSWORD', 'OS_AUTH_URL', 'OS_TENANT_NAME')
    for envvar in envvars:
        if os.getenv(envvar) is None:
            raise MissingEnvVar(envvar)

    # Unfortunately, each of the OpenStack client will request slightly
    # different entries in their credentials dict.
    if service.lower() in ("nova", "cinder"):
        password = "api_key"
        tenant = "project_id"
    else:
        password = "password"
        tenant = "tenant_name"

    # The most common way to pass these info to the script is to do it through
    # environment variables.
    creds.update({
        "username": os.environ.get("OS_USERNAME"),
        password: os.environ.get("OS_PASSWORD"),
        "auth_url": os.environ.get("OS_AUTH_URL"),
        tenant: os.environ.get("OS_TENANT_NAME")
    })
    if os.getenv('OS_ENDPOINT_TYPE') is not None:
        creds.update({
            "endpoint_type": os.environ.get("OS_ENDPOINT_TYPE")
        })
    if os.getenv('OS_REGION_NAME') is not None:
        creds.update({
            "region_name": os.environ.get("OS_REGION_NAME")
        })
    cacert = os.environ.get("OS_CACERT")
    if cacert is not None:
        # each openstack client uses differnt kwargs for this
        creds.update({"cacert": cacert,
                      "ca_cert": cacert,
                      "https_ca_cert": cacert,
                      "https_cacert": cacert,
                      "ca_file": cacert})
        creds.update({"insecure": "True", "https_insecure": "True"})
        if not os.path.isfile(cacert):
            logger.info("WARNING: The 'OS_CACERT' environment variable is "
                        "set to %s but the file does not exist." % cacert)
    return creds


def get_credentials_for_rally():
    creds = get_credentials("keystone")
    admin_keys = ['username', 'tenant_name', 'password']
    endpoint_types = [('internalURL', 'internal'),
                      ('publicURL', 'public'), ('adminURL', 'admin')]
    if 'endpoint_type' in creds.keys():
        for k, v in endpoint_types:
            if creds['endpoint_type'] == k:
                creds['endpoint_type'] = v
    rally_conf = {"type": "ExistingCloud", "admin": {}}
    for key in creds:
        if key in admin_keys:
            rally_conf['admin'][key] = creds[key]
        else:
            rally_conf[key] = creds[key]
    return rally_conf


def get_client_class(api_name, version, version_map):
    """Returns the client class for the requested API version

    :param api_name: the name of the API, e.g. 'compute', 'image', etc
    :param version: the requested API version
    :param version_map: a dict of client classes keyed by version
    :rtype: a client class for the requested API version
    """
    try:
        client_path = version_map[str(version)]
        logger.debug("client_path: " + client_path)
    except (KeyError, ValueError):
        logger.error("Invalid {} client version {}. \
            It must be one of: {}".format(api_name, version, version_map))

    return importutils.import_class(client_path)
