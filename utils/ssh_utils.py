import paramiko
import os
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("ssh_utils").getLogger()

FUEL_IP = '10.20.0.2'
FUEL_USER = 'root'
FUEL_PASS = 'r00tme'
FUEL_SSH_KEY = '/root/.ssh/id_rsa'
LOCAL_SSH_KEY = os.path.join(os.getcwd(), 'id_rsa')


def fetch_file(ssh_conn, src, dest):
    try:
        sftp = ssh_conn.open_sftp()
        sftp.get(src, dest)
        return True
    except Exception, e:
        logger.error("Error [fetch_file(ssh_conn, '%s', '%s']: %s" %
                     (src, dest, e))
        return None


class FuelJumpHostShell(paramiko.SSHClient):
    def __init__(self, *args, **kwargs):
        self.fuel_ssh = paramiko.SSHClient()
        self.fuel_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.fuel_ssh.connect(FUEL_IP,
                              username=FUEL_USER,
                              password=FUEL_PASS)
        self.fuel_transport = self.fuel_ssh.get_transport()
        self.fuel_channel = None
        super(FuelJumpHostShell, self).__init__(*args, **kwargs)

    def connect(self, hostname, port=22, username='root', password=None,
                pkey=None, key_filename=None, timeout=None, allow_agent=True,
                look_for_keys=True, compress=False, sock=None, gss_auth=False,
                gss_kex=False, gss_deleg_creds=True, gss_host=None,
                banner_timeout=None):
        if fetch_file(self.fuel_ssh, FUEL_SSH_KEY, LOCAL_SSH_KEY) is None:
            raise Exception('Could\'t fetch SSH key from Fuel master')
        fuel_key = paramiko.RSAKey.from_private_key_file(LOCAL_SSH_KEY)
        dest_addr = (hostname, 22)
        local_addr = (FUEL_IP, 22)
        self.fuel_channel = self.fuel_transport.open_channel("direct-tcpip",
                                                             dest_addr,
                                                             local_addr)
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        super(FuelJumpHostShell, self).connect(hostname,
                                               username=username,
                                               pkey=fuel_key,
                                               sock=self.fuel_channel)
        os.remove(LOCAL_SSH_KEY)
