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

import uuid

from flask import jsonify
import re

from functest.api.actions.api_tier import ApiTier
from functest.api.base import ApiResource
from functest.api.common import api_utils, error, thread
from functest.api.database.v1.handlers import TasksHandler


class V1Tiers(ApiResource):
    """ V1Tiers Resource class """

    def get(self):
        """ GET all tiers """
        tiers_list = ApiTier().list()
        data = re.split("[\n\t]", tiers_list)
        data = [i.strip() for i in data if i != '']
        data_dict = dict()
        for i in range(len(data) / 2):
            data_dict[data[i * 2]] = data[i * 2 + 1]
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

    def post(self):
        """ Used to handle post request """
        return self._dispatch_post()

    def run_tier(self, args):
        """ Run a tier """
        try:
            tier_name = args['tier']
        except KeyError:
            return api_utils.result_handler(
                status=1, data='tier name must be provided')

        task_id = str(uuid.uuid4())
        task_args = {'tier': tier_name, 'task_id': task_id}
        task_args.update(args.get('opts', {}))

        task_thread = thread.TaskThread(ApiTier.run, task_args, TasksHandler())
        task_thread.start()

        results = {'tier': tier_name, 'task_id': task_id}
        return jsonify(results)


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
