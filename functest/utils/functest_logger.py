#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Logging levels:
#  Level     Numeric value
#  CRITICAL  50
#  ERROR     40
#  WARNING   30
#  INFO      20
#  DEBUG     10
#  NOTSET    0
#
# Usage:
#  import functest_logger as fl
#  logger = fl.Logger("script_name").getLogger()
#  logger.info("message to be shown with - INFO - ")
#  logger.debug("message to be shown with - DEBUG -")
import logging
import logging.config
import os

import json

from functest.utils.constants import CONST

ignore = ["paramiko",
          "stevedore.extension",
          "keystoneauth.session",
          "keystoneauth.identity.v3.base",
          "novaclient.v2.client",
          "neutronclient.v2_0.client",
          "glanceclient.common.http",
          "cinderclient.v2.client",
          "cinderclient.client"]


class Logger(object):

    def __init__(self, logger_name):
        self.setup_logging()
        self.logger = logging.getLogger(logger_name)
        for module_name in ignore:
            logging.getLogger(module_name).setLevel(logging.WARNING)

    def getLogger(self):
        return self.logger

    def is_debug(self):
        if CONST.CI_DEBUG and CONST.CI_DEBUG.lower() == "true":
            return True
        return False

    def setup_logging(self, default_path=CONST.dir_functest_logging_cfg,
                      default_level=logging.INFO,
                      env_key='LOG_CFG'):
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
                if (config['handlers'] and
                        config['handlers']['console']):
                    stream_level = logging.INFO
                    if self.is_debug():
                        stream_level = logging.DEBUG
                    config['handlers']['console']['level'] = stream_level
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
