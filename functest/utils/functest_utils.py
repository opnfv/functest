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
import subprocess
import sys
import yaml

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
            ofd.write(line)
        else:
            line = line.replace('\n', '')
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
    version = get_nova_version(cloud)
    try:
        assert version
        if version > (2, 60):
            osversion = "Rocky or newer"
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
