#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
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

import os
import time
import sys
import yaml


FUNCTEST_REPO = '%s/functest' % os.environ['repos_dir']
DOCTOR_REPO '%s/doctor' % os.environ['repos_dir']

sys.path.append("%s/testcases" % FUNCTEST_REPO)
import functest_utils


def get_result_db_url():
    with open('%s/testcases/config_functest.yaml' % FUNCTEST_REPO) as f:
        functest_yaml = yaml.safe_load(f)
    test_db = functest_yaml.get('results').get('test_db_url')
    return '%s/results' % test_db


def main():
    cmd = 'cd %s/tests && ./run.sh' % DOCTOR_REPO
    env = {
        'OS_USERNAME': 'admin',
        'OS_PASSWORD': 'admin',
        'OS_AUTH_URL': 'http://192.168.20.71:5000/v2.0',
        'OS_TENANT_NAME', 'admin'),
    }
    start_time_ts = time.time()

    ret = functest_utils.execute_command(cmd, env=env)

    end_time_ts = time.time()
    duration = round(end_time_ts - start_time_ts, 1)
    if ret:
        test_status = 'OK'
    else:
        test_status = 'NOK'

    db_url = get_result_db_url()
    details = {
        'timestart': start_time_ts,
        'duration': duration,
        'status': test_status,
    }
    pod_name = functest_utils.get_pod_name()
    git_version = functest_utils.get_git_branch(DOCTOR_REPO)
    functest_utils.push_results_to_db(db_url,
                                      'doctor-notification',
                                      None,
                                      pod_name,
                                      git_version,
                                      details)


if __name__ == '__main__':
    main()
