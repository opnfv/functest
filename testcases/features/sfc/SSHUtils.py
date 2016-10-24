##############################################################################
# Copyright (c) 2015 Ericsson AB and others.
# Authors: George Paraskevopoulos (geopar@intracom-telecom.com)
#          Jose Lausuch (jose.lausuch@ericsson.com)
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import paramiko
import functest.utils.functest_logger as rl
import os

logger = rl.Logger('SSHUtils').getLogger()


def get_ssh_client(hostname, username, password=None, proxy=None):
    client = None
    try:
        if proxy is None:
            client = paramiko.SSHClient()
        else:
            client = ProxyHopClient()
            client.configure_jump_host(proxy['ip'],
                                       proxy['username'],
                                       proxy['password'])

        if client is None:
            raise Exception('Could not connect to client')

        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,
                       username=username,
                       password=password)
        return client
    except Exception, e:
        logger.error(e)
        return None


def get_file(ssh_conn, src, dest):
    try:
        sftp = ssh_conn.open_sftp()
        sftp.get(src, dest)
        return True
    except Exception, e:
        logger.error("Error [get_file(ssh_conn, '%s', '%s']: %s" %
                     (src, dest, e))
        return None


def put_file(ssh_conn, src, dest):
    try:
        sftp = ssh_conn.open_sftp()
        sftp.put(src, dest)
        return True
    except Exception, e:
        logger.error("Error [put_file(ssh_conn, '%s', '%s']: %s" %
                     (src, dest, e))
        return None


class ProxyHopClient(paramiko.SSHClient):
    '''
    Connect to a remote server using a proxy hop
    '''
    def __init__(self, *args, **kwargs):
        self.logger = rl.Logger("ProxyHopClient").getLogger()
        self.proxy_ssh = None
        self.proxy_transport = None
        self.proxy_channel = None
        self.proxy_ip = None
        self.proxy_ssh_key = None
        self.local_ssh_key = os.path.join(os.getcwd(), 'id_rsa')
        super(ProxyHopClient, self).__init__(*args, **kwargs)

    def configure_jump_host(self, jh_ip, jh_user, jh_pass,
                            jh_ssh_key='/root/.ssh/id_rsa'):
        self.proxy_ip = jh_ip
        self.proxy_ssh_key = jh_ssh_key
        self.proxy_ssh = paramiko.SSHClient()
        self.proxy_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.proxy_ssh.connect(jh_ip,
                               username=jh_user,
                               password=jh_pass)
        self.proxy_transport = self.proxy_ssh.get_transport()

    def connect(self, hostname, port=22, username='root', password=None,
                pkey=None, key_filename=None, timeout=None, allow_agent=True,
                look_for_keys=True, compress=False, sock=None, gss_auth=False,
                gss_kex=False, gss_deleg_creds=True, gss_host=None,
                banner_timeout=None):
        try:
            if self.proxy_ssh is None:
                raise Exception('You must configure the jump '
                                'host before calling connect')

            get_file_res = get_file(self.proxy_ssh,
                                    self.proxy_ssh_key,
                                    self.local_ssh_key)
            if get_file_res is None:
                raise Exception('Could\'t fetch SSH key from jump host')
            proxy_key = (paramiko.RSAKey
                         .from_private_key_file(self.local_ssh_key))

            self.proxy_channel = self.proxy_transport.open_channel(
                "direct-tcpip",
                (hostname, 22),
                (self.proxy_ip, 22))

            self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            super(ProxyHopClient, self).connect(hostname,
                                                username=username,
                                                pkey=proxy_key,
                                                sock=self.proxy_channel)
            os.remove(self.local_ssh_key)
        except Exception, e:
            self.logger.error(e)
