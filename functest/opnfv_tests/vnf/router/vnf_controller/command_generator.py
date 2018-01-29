#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

"""command generator module for vrouter testing"""

import logging
from jinja2 import Environment, FileSystemLoader


class CommandGenerator(object):
    """command generator class for vrouter testing"""

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.logger.debug("init command generator")

    @staticmethod
    def load_template(template_dir, template):
        # pylint disable=missing-docstring
        loader = FileSystemLoader(template_dir,
                                  encoding='utf8')
        env = Environment(loader=loader)
        return env.get_template(template)

    @staticmethod
    def command_create(template, parameter):
        # pylint disable=missing-docstring
        commands = template.render(parameter)
        return commands.split('\n')
