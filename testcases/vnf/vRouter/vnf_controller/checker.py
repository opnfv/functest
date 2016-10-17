##!/usr/bin/python
## coding: utf8
#######################################################################
#
# Copyright (c) 2016 Okinawa Open Laboratory
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#######################################################################
import json
import logging
import re

from jinja2 import Environment, FileSystemLoader

import functest.utils.functest_logger as ft_logger

""" logging configuration """
logger = ft_logger.Logger("vRouter.cecker").getLogger()
logger.setLevel(logging.DEBUG)

class Checker:
    def __init__(self):
        logger.debug("init cecker")

    def load_check_rule(self, rule_file_dir, rule_file_name, parameter):
        loader = FileSystemLoader(rule_file_dir,
                                  encoding='utf8')
        env = Environment(loader=loader)
        check_rule_template = env.get_template(rule_file_name)
        check_rule = check_rule_template.render(parameter)
        check_rule_data = json.loads(check_rule)
        return check_rule_data


    def regexp_information(self, response, rules):
        status = False
        result_data = []

        for rule in rules["rules"]:
            sec_bar = "========================================================"
            logger.info(sec_bar)
            result_data.append(sec_bar)
            logout = '{0:50}'.format(" " + rule["description"])

            match = re.search(rule["regexp"],
                              response)
            rule["response"] = response
            if match == None:
                logger.info(logout + "| NG |")
                result_data.append(logout + "| NG |")
                result_data.append("Nothing Match Data")
                return False

            if not match.group(1) == rule["result"] :
                logger.info(logout + "| NG |")
                result_data.append(logout + "| NG |")
                result_data.append("Nothing Match Data")
                status = False
            else:
                logger.info(logout + "| OK |")
                result_data.append(logout + "| OK |")
                status = True

            result_data.append("rule     : " + rule["regexp"])
            result_data.append("response : " + response)

        return status, result_data
