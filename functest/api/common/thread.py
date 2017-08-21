#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Used to handle multi-thread tasks
"""

import logging
import threading

from oslo_serialization import jsonutils


LOGGER = logging.getLogger(__name__)


class TaskThread(threading.Thread):
    """ Task Thread Class """

    def __init__(self, target, args, handler):
        super(TaskThread, self).__init__(target=target, args=args)
        self.target = target
        self.args = args
        self.handler = handler

    def run(self):
        """ Override the function run: run testcase and update database """
        update_data = {'task_id': self.args.get('task_id'),
                       'status': 'IN PROGRESS'}
        self.handler.insert(update_data)

        LOGGER.info('Starting running test case')

        try:
            data = self.target(self.args)
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.exception('Task Failed')
            update_data = {'status': 'FAIL', 'error': str(err)}
            self.handler.update_attr(self.args.get('task_id'), update_data)
        else:
            LOGGER.info('Task Finished')
            LOGGER.debug('Result: %s', data)
            new_data = {'status': 'FINISHED',
                        'result': jsonutils.dumps(data.get('result', {}))}

            self.handler.update_attr(self.args.get('task_id'), new_data)
