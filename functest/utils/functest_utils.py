#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# valentin.boucher@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

from __future__ import print_function
import logging
import os
import subprocess
import sys
import yaml

from shade import _utils
import six

LOGGER = logging.getLogger(__name__)


def execute_command_raise(cmd, info=False, error_msg="",
                          verbose=True, output_file=None):
    ret = execute_command(cmd, info, error_msg, verbose, output_file)
    if ret != 0:
        raise Exception(error_msg)


def execute_command(cmd, info=False, error_msg="",
                    verbose=True, output_file=None):
    if not error_msg:
        error_msg = ("The command '%s' failed." % cmd)
    msg_exec = ("Executing command: '%s'" % cmd)
    if verbose:
        if info:
            LOGGER.info(msg_exec)
        else:
            LOGGER.debug(msg_exec)
    popen = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if output_file:
        ofd = open(output_file, "w")
    for line in iter(popen.stdout.readline, b''):
        if output_file:
            ofd.write(line.decode("utf-8"))
        else:
            line = line.decode("utf-8").replace('\n', '')
            print(line)
            sys.stdout.flush()
    if output_file:
        ofd.close()
    popen.stdout.close()
    returncode = popen.wait()
    if returncode != 0:
        if verbose:
            LOGGER.error(error_msg)

    return returncode


def get_parameter_from_yaml(parameter, yfile):
    """
    Returns the value of a given parameter in file.yaml
    parameter must be given in string format with dots
    Example: general.openstack.image_name
    """
    with open(yfile) as yfd:
        file_yaml = yaml.safe_load(yfd)
    value = file_yaml
    for element in parameter.split("."):
        value = value.get(element)
        if value is None:
            raise ValueError("The parameter %s is not defined in"
                             " %s" % (parameter, yfile))
    return value


def get_nova_version(cloud):
    """ Get Nova API microversion

    Returns:

    - Nova API microversion
    - None on operation error
    """
    # pylint: disable=protected-access
    try:
        request = cloud._compute_client.request("/", "GET")
        LOGGER.debug('cloud._compute_client.request: %s', request)
        version = request["version"]["version"]
        major, minor = version.split('.')
        LOGGER.debug('nova version: %s', (int(major), int(minor)))
        return (int(major), int(minor))
    except Exception:  # pylint: disable=broad-except
        LOGGER.exception("Cannot detect Nova version")
        return None


def get_openstack_version(cloud):
    """ Detect OpenStack version via Nova API microversion

    It follows `MicroversionHistory
    <https://docs.openstack.org/nova/latest/reference/api-microversion-history.html>`_.

    Returns:

    - OpenStack release
    - Unknown on operation error
    """
    # pylint: disable=too-many-branches
    version = get_nova_version(cloud)
    try:
        assert version
        if version > (2, 87):
            osversion = "Master"
        elif version > (2, 79):
            osversion = "Ussuri or Victoria"
        elif version > (2, 72):
            osversion = "Train"
        elif version > (2, 65):
            osversion = "Stein"
        elif version > (2, 60):
            osversion = "Rocky"
        elif version > (2, 53):
            osversion = "Queens"
        elif version > (2, 42):
            osversion = "Pike"
        elif version > (2, 38):
            osversion = "Ocata"
        elif version > (2, 25):
            osversion = "Newton"
        elif version > (2, 12):
            osversion = "Mitaka"
        elif version > (2, 3):
            osversion = "Liberty"
        elif version >= (2, 1):
            osversion = "Kilo"
        else:
            osversion = "Unknown"
        LOGGER.info('Detect OpenStack version: %s', osversion)
        return osversion
    except AssertionError:
        LOGGER.exception("Cannot detect OpenStack version")
        return "Unknown"


def list_services(cloud):
    # pylint: disable=protected-access
    """Search Keystone services via $OS_INTERFACE.

    It mainly conforms with `Shade
    <https://docs.openstack.org/shade/latest>`_ but allows testing vs
    public endpoints. It's worth mentioning that it doesn't support keystone
    v2.

    :returns: a list of ``munch.Munch`` containing the services description

    :raises: ``OpenStackCloudException`` if something goes wrong during the
        openstack API call.
    """
    url, key = '/services', 'services'
    data = cloud._identity_client.get(
        url, endpoint_filter={
            'interface': os.environ.get('OS_INTERFACE', 'public')},
        error_message="Failed to list services")
    services = cloud._get_and_munchify(key, data)
    return _utils.normalize_keystone_services(services)


def search_services(cloud, name_or_id=None, filters=None):
    # pylint: disable=protected-access
    """Search Keystone services ia $OS_INTERFACE.

    It mainly conforms with `Shade
    <https://docs.openstack.org/shade/latest>`_ but allows testing vs
    public endpoints. It's worth mentioning that it doesn't support keystone
    v2.

    :param name_or_id: Name or id of the desired service.
    :param filters: a dict containing additional filters to use. e.g.
                    {'type': 'network'}.

    :returns: a list of ``munch.Munch`` containing the services description

    :raises: ``OpenStackCloudException`` if something goes wrong during the
        openstack API call.
    """
    services = list_services(cloud)
    return _utils._filter_list(services, name_or_id, filters)


def convert_dict_to_ini(value):
    "Convert dict to oslo.conf input"
    assert isinstance(value, dict)
    return ",".join("{}:{}".format(
        key, val) for (key, val) in six.iteritems(value))


def convert_list_to_ini(value):
    "Convert list to oslo.conf input"
    assert isinstance(value, list)
    return ",".join("{}".format(val) for val in value)


def convert_ini_to_dict(value):
    "Convert oslo.conf input to dict"
    assert isinstance(value, str)
    try:
        return dict((x.rsplit(':', 1) for x in value.split(',')))
    except ValueError:
        return {}


def convert_ini_to_list(value):
    "Convert list to oslo.conf input"
    assert isinstance(value, str)
    if not value:
        return []
    return list(value.split(','))
