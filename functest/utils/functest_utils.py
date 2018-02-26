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
            print (line)
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
