#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

from flask import jsonify
import re

from functest.cli.commands.cli_tier import CliTier
from functest.api import ApiResource


class V1Tiers(ApiResource):
    def get(self):
        tiers_list = CliTier().list()
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
