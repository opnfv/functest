#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

"""vrouter test result check module"""

import json
import logging
import re

from jinja2 import Environment, FileSystemLoader


class Checker(object):
    """vrouter test result check class"""

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.logger.debug("init checker")

    @staticmethod
    def load_check_rule(rule_file_dir, rule_file_name, parameter):
        loader = FileSystemLoader(rule_file_dir,
                                  encoding='utf8')
        env = Environment(loader=loader)
        check_rule_template = env.get_template(rule_file_name)
        check_rule = check_rule_template.render(parameter)
        check_rule_data = json.loads(check_rule)
        return check_rule_data

    @staticmethod
    def regexp_information(response, rules):
        status = False
        result_data = {}

        for rule in rules["rules"]:
            result_data = {
                "test_name": rule["description"],
                "result": "NG"
            }

            match = re.search(rule["regexp"],
                              response)
            rule["response"] = response
            if match is None:
                status = False
                break

            if not match.group(1) == rule["result"]:
                status = False
            else:
                result_data["result"] = "OK"
                status = True

        return status, result_data
