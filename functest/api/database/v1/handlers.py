#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Used to handle tasks: insert the task info into database and update it
"""

from functest.api.database.db import DB_SESSION
from functest.api.database.v1.models import Tasks


class TasksHandler(object):
    """ Tasks Handler Class """

    def insert(self, kwargs):  # pylint: disable=no-self-use
        """ To insert the task info into database """
        task = Tasks(**kwargs)
        DB_SESSION.add(task)  # pylint: disable=maybe-no-member
        DB_SESSION.commit()  # pylint: disable=maybe-no-member
        return task

    def get_task_by_taskid(self, task_id):  # pylint: disable=no-self-use
        """ Obtain the task by task id """
        # pylint: disable=maybe-no-member
        task = Tasks.query.filter_by(task_id=task_id).first()
        if not task:
            raise ValueError

        return task

    def update_attr(self, task_id, attr):
        """ Update the required attributes of the task """
        task = self.get_task_by_taskid(task_id)

        for key, value in attr.items():
            setattr(task, key, value)
        DB_SESSION.commit()  # pylint: disable=maybe-no-member
