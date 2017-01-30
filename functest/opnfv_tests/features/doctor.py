#!/usr/bin/python
#
# Copyright (c) 2017 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# 0.1: This script boots the VM1 and allocates IP address from Nova
# Later, the VM2 boots then execute cloud-init to ping VM1.
# After successful ping, both the VMs are deleted.
# 0.2: measure test duration and publish results under json format
#
#
import functest.core.feature_base as base


class Doctor(base.FeatureBase):
    def __init__(self):
        super(Doctor, self).__init__(project='doctor',
                                     case='doctor-notification',
                                     repo='dir_repo_doctor')
        self.cmd = 'cd %s/tests && ./run.sh' % self.repo

    def parse_results(self, ret):
        exit_code = super(Doctor, self).paese_results(ret)

        if ret == 0:
            test_status = 'OK'
        else:
            test_status = 'NOK'

        duration = round(self.start_time - self.stop_time, 1)

        self.details = {
            'timestart': self.start_time,
            'duration': duration,
            'status': test_status,
        }

        return exit_code
