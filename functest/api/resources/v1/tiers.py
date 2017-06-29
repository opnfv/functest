#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Resources to handle tier related requests
"""

from flask import jsonify
import re

from functest.api.base import ApiResource
from functest.api.actions.api_tier import ApiTier
from functest.utils import error


class V1Tiers(ApiResource):
    """ V1Tiers Resource class """

    def get(self):
        """ GET all tiers """
        tiers_list = ApiTier().list()
        data = re.split("[\n\t]", tiers_list)
        data = [i.strip() for i in data if i != '']
        data_dict = dict()
        for i in range(len(data) / 2):
            one_data = {data[i * 2]: data[i * 2 + 1]}
            if i == 0:
                data_dict = one_data
            else:
                data_dict.update(one_data)
        result = {'tiers': data_dict}
        return jsonify(result)


class V1Tier(ApiResource):
    """ V1Tier Resource class """

    def get(self, tier_name):
        """ GET the info of one tier """
        testcases = ApiTier().gettests(tier_name)
        if not testcases:
            return error.notFoundError(
                "The tier with name '%s' does not exist." % tier_name)
        tier_info = ApiTier().show(tier_name)
        tier_info.__dict__.pop('name')
        tier_info.__dict__.pop('tests_array')
        result = {'tier': tier_name, 'testcases': testcases}
        result.update(tier_info.__dict__)
        return jsonify(result)


class V1TestcasesinTier(ApiResource):
    """ V1TestcasesinTier Resource class """

    def get(self, tier_name):
        """ GET all testcases within given tier """
        testcases = ApiTier().gettests(tier_name)
        if not testcases:
            return error.notFoundError(
                "The tier with name '%s' does not exist." % tier_name)
        result = {'tier': tier_name, 'testcases': testcases}
        return jsonify(result)
