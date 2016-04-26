#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

# Logging levels:
# Level     Numeric value
# CRITICAL  50
# ERROR     40
# WARNING   30
# INFO      20
# DEBUG     10
# NOTSET    0


import logging
import os


class Logger:
    def __init__(self, logger_name):

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                      '%(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        CI_DEBUG = os.getenv('CI_DEBUG')

        if CI_DEBUG is None or CI_DEBUG.lower() == "false":
            ch.setLevel(logging.INFO)
        else:
            ch.setLevel(logging.DEBUG)

        self.logger.addHandler(ch)

    def getLogger(self):
        return self.logger
