##############################################################################
# Copyright (c) 2015 Ericsson AB and others.
# Author: George Paraskevopoulos (geopar@intracom-telecom.com)
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import functest.utils.functest_logger as rl
import os
import time

logger = rl.Logger('ovs_utils').getLogger()


class OVSLogger(object):
    def __init__(self, basedir):
        self.ovs_dir = os.path.join(basedir, 'odl-sfc/ovs')
        self.__mkdir_p(self.ovs_dir)

    def __mkdir_p(self, dirpath):
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

    def __ssh_host(self, ssh_conn):
        return ssh_conn.get_transport().getpeername()[0]

    def __dump_to_file(self, operation, host, text, timestamp=None):
        ts = (timestamp if timestamp is not None
              else time.strftime("%Y%m%d-%H%M%S"))
        dumpdir = os.path.join(self.ovs_dir, ts)
        self.__mkdir_p(dumpdir)
        fname = '{0}_{1}'.format(operation, host)
        with open(os.path.join(dumpdir, fname), 'w') as f:
            f.write(text)

    def __remote_cmd(self, ssh_conn, cmd):
        try:
            _, stdout, stderr = ssh_conn.exec_command(cmd)
            errors = stderr.readlines()
            if len(errors) > 0:
                host = self.__ssh_host(ssh_conn)
                logger.error(''.join(errors))
                raise Exception('Could not execute {0} in {1}'
                                .format(cmd, host))
            output = ''.join(stdout.readlines())
            return output
        except Exception, e:
            logger.error('[__remote_command(ssh_client, {0})]: {1}'
                         .format(cmd, e))
            return None

    def ofctl_dump_flows(self, ssh_conn, br='br-int',
                         choose_table=None, timestamp=None):
        try:
            cmd = 'ovs-ofctl -OOpenFlow13 dump-flows {0}'.format(br)
            if choose_table is not None:
                cmd = '{0} table={1}'.format(cmd, choose_table)
            output = self.__remote_cmd(ssh_conn, cmd)
            operation = 'ofctl_dump_flows'
            host = self.__ssh_host(ssh_conn)
            self.__dump_to_file(operation, host, output, timestamp=timestamp)
            return output
        except Exception, e:
            logger.error('[ofctl_dump_flows(ssh_client, {0}, {1})]: {2}'
                         .format(br, choose_table, e))
            return None

    def vsctl_show(self, ssh_conn, timestamp=None):
        try:
            cmd = 'ovs-vsctl show'
            output = self.__remote_cmd(ssh_conn, cmd)
            operation = 'vsctl_show'
            host = self.__ssh_host(ssh_conn)
            self.__dump_to_file(operation, host, output, timestamp=timestamp)
            return output
        except Exception, e:
            logger.error('[vsctl_show(ssh_client)]: {0}'.format(e))
            return None
