#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Resources to retrieve the task results
"""


import json
import logging
import uuid

from flask import jsonify

from functest.api.base import ApiResource
from functest.api.common import api_utils
from functest.api.database.v1.handlers import TasksHandler


LOGGER = logging.getLogger(__name__)


class V1Tasks(ApiResource):
    """ V1Tasks Resource class"""

    def get(self, task_id):  # pylint: disable=no-self-use
        """ GET the result of the task id """
        try:
            uuid.UUID(task_id)
        except ValueError:
            return api_utils.result_handler(status=1, data='Invalid task id')

        task_handler = TasksHandler()
        try:
            task = task_handler.get_task_by_taskid(task_id)
        except ValueError:
            return api_utils.result_handler(status=1, data='No such task id')

        status = task.status
        LOGGER.debug('Task status is: %s', status)

        if status not in ['IN PROGRESS', 'FAIL', 'FINISHED']:
            return api_utils.result_handler(status=1,
                                            data='internal server error')
        if status == 'IN PROGRESS':
            result = {'status': status, 'result': ''}
        elif status == 'FAIL':
            result = {'status': status, 'error': task.error}
        else:
            result = {'status': status, 'result': json.loads(task.result)}

        return jsonify(result)
