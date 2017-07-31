#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

from functest.api.database.db import db_session
from functest.api.database.v1.models import Tasks


class TasksHandler(object):

    def insert(self, kwargs):
        task = Tasks(**kwargs)
        db_session.add(task)
        db_session.commit()
        return task

    def get_task_by_taskid(self, task_id):
        task = Tasks.query.filter_by(task_id=task_id).first()
        if not task:
            raise ValueError

        return task

    def update_attr(self, task_id, attr):
        task = self.get_task_by_taskid(task_id)

        for key, value in attr.items():
            setattr(task, key, value)
        db_session.commit()
