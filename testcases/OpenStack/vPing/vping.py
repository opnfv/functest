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
# 0.3: adapt push 2 DB after Test API refacroting
#
#
import datetime
import time

import argparse
import functest.utils.functest_logger as ft_logger

import vping_util as util

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
parser.add_argument("-m", "--mode", default='ssh',
                    help="vPing mode: userdata or ssh",
                    action="store")

args = parser.parse_args()

""" logging configuration """
logger = ft_logger.Logger("vping_userdata").getLogger()


def main():
    if args.mode == 'ssh':
        case = 'vping_ssh'
    else:
        case = 'vping_userdata'

    util.init(logger)

    util.check_repo_exist()

    vmname_1 = util.get_vmname_1()
    vmname_2 = util.get_vmname_2()

    image_id = util.create_image()

    flavor = util.get_flavor()

    network_id = util.create_network_full()

    sg_id = util.create_security_group()

    util.delete_exist_vms()

    start_time = time.time()
    logger.info("vPing Start Time:'%s'" % (
        datetime.datetime.fromtimestamp(start_time).strftime(
            '%Y-%m-%d %H:%M:%S')))

    vm1 = util.boot_vm(case,
                       vmname_1,
                       image_id,
                       flavor,
                       network_id,
                       None,
                       sg_id)
    test_ip = util.get_test_ip(vm1)
    vm2 = util.boot_vm(case,
                       vmname_2,
                       image_id,
                       flavor,
                       network_id,
                       test_ip,
                       sg_id)

    EXIT_CODE, stop_time = util.do_vping(case, vm2, test_ip)
    details = util.check_result(EXIT_CODE,
                                start_time,
                                stop_time)
    util.push_result(args.report,
                     case,
                     start_time,
                     stop_time,
                     details)

    exit(EXIT_CODE)


if __name__ == '__main__':
    main()
