# This script must be use with vxlan-gpe + nsh. Once we have eth + nsh support
# in ODL, we will not need it anymore

import paramiko
import pdb
import os
import sys

paramiko.util.log_to_file("paramiko.log")
ssh_options = "-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
BASEDIR = os.path.dirname(__file__)
print(BASEDIR)

try:
    INSTALLER_IP=os.environ['INSTALLER_IP']

except:
    print("INSTALLER_IP does not exist. We create 10.20.0.2")
    INSTALLER_IP = "10.20.0.2"

if not INSTALLER_IP:
    INSTALLER_IP = "10.20.0.2"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(INSTALLER_IP, username="root",
                password="r00tme", timeout=2)
    command = "fuel node | grep compute | awk '{print $10}'"
#    logger.info("Executing ssh to collect the compute IPs")
    print("Executing ssh to collect the compute IPs")
    (stdin, stdout, stderr) = ssh.exec_command(command)
except:
    print("Something went wrong in the ssh to collect the computes IP")
#    logger.debug("Something went wrong in the ssh to collect the computes IP")

output = stdout.readlines()

for ip in output:
    print(ip.rstrip())
    try:
        ssh.connect(INSTALLER_IP, username="root",
                password="r00tme", timeout=2)
#        command = ("ssh " + ssh_options + " root@" + ip + " ifconfig br-int up")
        command = ("ssh " + ssh_options + " root@" + ip + " 'which touch '")
#       logger.info("Executing ssh to collect the compute IPs")
        print(command)
        print("Bringing up the br-int interface of the computes")
#        router_channel = ssh.invoke_shell()
#        router_channel.send(command)
        (stdin, stdout, stderr) = ssh.exec_command(command, timeout=2)
        stdin.channel.shutdown_write()
        print(stdout.readlines())
        print(stderr.readlines())
#        command = ("ssh " + ssh_options + " root@" + ip + " 'ls'")
#        command = ("ssh " + ssh_options + " root@" + ip + " ip route add "
#                    "11.0.0.0/24 dev br-int")
#        (stdin, stdout, stderr) = ssh.exec_command(command)
#        print(command)
#        stdin.channel.shutdown_write()
#        print(stdout.readlines()) 
    except:
        print("Something went wrong bringing up the network of the computes")
#       logger.debug("Something went wrong in the ssh to collect the computes IP")

sys.exit(0)

#output=$(sshpass -p r00tme ssh $ssh_options root@${INSTALLER_IP} 'ssh root@'"$ip"' ip route | \
#cut -d" " -f1 | grep 11.0.0.0' ; exit 0)
#
#if [ -z "$output" ]; then
#sshpass -p r00tme ssh $ssh_options root@${INSTALLER_IP} 'ssh root@'"$ip"' ip route add 11.0.0.0/24 \
#dev br-int'
#fi
