#!/usr/bin/env python
#
#  Copyright 2017 Okinawa Open Laboratory
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
import functest.core.feature as base
import json
import os

RESULT_DETAILS_FILE = "test_result.json"


class VrouterVnf(base.Feature):
    def __init__(self):
        super(VrouterVnf, self).__init__(project='functest',
                                         case='vyos_vrouter',
                                         repo='dir_repo_vrouter')
        self.cmd = 'cd %s && ./run.sh' % self.repo

    def set_result_details(self):
        filepath = os.path.join(self.repo, RESULT_DETAILS_FILE)
        if os.path.exists(filepath):
            f = open(filepath, 'r')
            self.details = json.load(f)
            f.close()

    def log_results(self):
        if self.criteria == 'PASS':
            self.set_result_details()
        super(VrouterVnf, self).log_results()
