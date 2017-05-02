#!/usr/bin/env python

# Copyright (c) 2017 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import json
import logging
import os
import time

from opera import openo_connect
import requests

import functest.opnfv_tests.vnf.ims.clearwater_ims_base as clearwater_ims_base


class OperaIms(clearwater_ims_base.ClearwaterOnBoardingBase):

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "opera_ims"
        super(OperaIms, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.ellis_file = os.path.join(self.result_dir, 'ellis.info')
        self.live_test_file = os.path.join(self.result_dir,
                                           'live_test_report.json')
        try:
            self.openo_msb_endpoint = os.environ['OPENO_MSB_ENDPOINT']
        except KeyError:
            raise Exception('OPENO_MSB_ENDPOINT is not specified,'
                            ' put it as <OPEN-O ip>:<port>')
        else:
            self.logger.info('OPEN-O endpoint is: %s', self.openo_msb_endpoint)

    def prepare(self):
        pass

    def clean(self):
        pass

    def deploy_vnf(self):
        try:
            openo_connect.create_service(self.openo_msb_endpoint,
                                         'functest_opera',
                                         'VNF for functest testing')
        except Exception as e:
            self.logger.error(e)
            return {'status': 'FAIL', 'result': e}
        else:
            self.logger.info('vIMS deployment is kicked off')
            return {'status': 'PASS', 'result': ''}

    def dump_info(self, info_file, result):
        with open(info_file, 'w') as f:
            self.logger.debug('Save information to file: %s', info_file)
            json.dump(result, f)

    def test_vnf(self):
        vnfm_ip = openo_connect.get_vnfm_ip(self.openo_msb_endpoint)
        self.logger.info('VNFM IP: %s', vnfm_ip)
        vnf_status_url = 'http://{0}:5000/api/v1/model/status'.format(vnfm_ip)
        vnf_alive = False
        retry = 40

        self.logger.info('Check the VNF status')
        while retry > 0:
            rq = requests.get(vnf_status_url, timeout=90)
            response = rq.json()
            vnf_alive = response['vnf_alive']
            msg = response['msg']
            self.logger.info(msg)
            if vnf_alive:
                break
            self.logger.info('check again in one and half a minute...')
            retry = retry - 1
            time.sleep(90)

        if not vnf_alive:
            raise Exception('VNF failed to start: {0}'.format(msg))

        ellis_config_url = ('http://{0}:5000/api/v1/model/ellis/configure'
                            .format(vnfm_ip))
        rq = requests.get(ellis_config_url, timeout=90)
        if rq.json() and not rq.json()['ellis_ok']:
            self.logger.error(rq.json()['data'])
            raise Exception('Failed to configure Ellis')

        self.logger.info('Get Clearwater deployment detail')
        vnf_info_url = ('http://{0}:5000/api/v1/model/output'
                        .format(vnfm_ip))
        rq = requests.get(vnf_info_url, timeout=90)
        data = rq.json()['data']
        self.logger.info(data)
        bono_ip = data['bono_ip']
        ellis_ip = data['ellis_ip']
        dns_ip = data['dns_ip']
        result = self.config_ellis(ellis_ip, 'signup', True)
        self.logger.debug('Ellis Result: %s', result)
        self.dump_info(self.ellis_file, result)

        if dns_ip:
            vims_test_result = self.run_clearwater_live_test(
                dns_ip,
                'clearwater.local',
                bono_ip,
                ellis_ip,
                'signup')
            if vims_test_result != '':
                self.dump_info(self.live_test_file, vims_test_result)
                return {'status': 'PASS', 'result': vims_test_result}
            else:
                return {'status': 'FAIL', 'result': ''}

    def main(self, **kwargs):
        self.logger.info("Start to run Opera vIMS VNF onboarding test")
        self.execute()
        self.logger.info("Opera vIMS VNF onboarding test finished")
        if self.result is "PASS":
            return self.EX_OK
        else:
            return self.EX_RUN_ERROR

    def run(self):
        kwargs = {}
        return self.main(**kwargs)
