import os
import subprocess
import sys
import time

import argparse
import paramiko

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")

args = parser.parse_args()

""" logging configuration """
logger = ft_logger.Logger("ODL_SFC").getLogger()

FUNCTEST_REPO = ft_utils.FUNCTEST_REPO

HOME = os.environ['HOME'] + "/"

VM_BOOT_TIMEOUT = 180
INSTANCE_NAME = "client"
FLAVOR = "m1.small"
IMAGE_NAME = "sf_nsh_colorado"
IMAGE_FILENAME = "sf_nsh_colorado.qcow2"
IMAGE_FORMAT = "qcow2"
IMAGE_PATH = "/home/opnfv/functest/data" + "/" + IMAGE_FILENAME

# NEUTRON Private Network parameters

NET_NAME = "example-net"
SUBNET_NAME = "example-subnet"
SUBNET_CIDR = "11.0.0.0/24"
ROUTER_NAME = "example-router"

SECGROUP_NAME = "example-sg"
SECGROUP_DESCR = "Example Security group"

INSTANCE_NAME_2 = "server"

# TEST_DB = ft_utils.get_parameter_from_yaml("results.test_db_url")

PRE_SETUP_SCRIPT = 'sfc_pre_setup.bash'
TACKER_SCRIPT = 'sfc_tacker.bash'
TEARDOWN_SCRIPT = "sfc_teardown.bash"
TACKER_CHANGECLASSI = "sfc_change_classi.bash"

ssh_options = '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'


def check_ssh(ip):
    cmd = "sshpass -p opnfv ssh " + ssh_options + " -q " + ip + " exit"
    success = subprocess.call(cmd, shell=True) == 0
    if not success:
        logger.debug("Wating for SSH connectivity in SF with IP: %s" % ip)
    return success


def main():

    # Allow any port so that tacker commands reaches the server.
    # This will be deleted when tacker is included in OPNFV installation

    status = "PASS"
    failures = 0
    start_time = time.time()
    json_results = {}

    contr_cmd = ("sshpass -p r00tme ssh " + ssh_options + " root@10.20.0.2"
                 " 'fuel node'|grep controller|awk '{print $10}'")
    logger.info("Executing script to get ip_server: '%s'" % contr_cmd)
    process = subprocess.Popen(contr_cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    ip_server = process.stdout.readline().rstrip()

    contr_cmd2 = ("sshpass -p r00tme ssh " + ssh_options + " root@10.20.0.2"
                  " 'fuel node'|grep compute|awk '{print $10}'")
    logger.info("Executing script to get ip_compute: '%s'" % contr_cmd2)
    process = subprocess.Popen(contr_cmd2,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    ip_compute = process.stdout.readline().rstrip()

    iptable_cmd1 = ("sshpass -p r00tme ssh " + ssh_options + " root@10.20.0.2"
                    " ssh " + ip_server + " iptables -P INPUT ACCEPT ")
    iptable_cmd2 = ("sshpass -p r00tme ssh " + ssh_options + " root@10.20.0.2"
                    " ssh " + ip_server + " iptables -t nat -P INPUT ACCEPT ")
    iptable_cmd3 = ("sshpass -p r00tme ssh " + ssh_options + " root@10.20.0.2"
                    " ssh " + ssh_options + " " + ip_server +
                    " iptables -A INPUT -m state"
                    " --state NEW,ESTABLISHED,RELATED -j ACCEPT")

    logger.info("Changing firewall policy in controller: '%s'" % iptable_cmd1)
    subprocess.call(iptable_cmd1, shell=True, stderr=subprocess.PIPE)

    logger.info("Changing firewall policy in controller: '%s'" % iptable_cmd2)
    subprocess.call(iptable_cmd2, shell=True, stderr=subprocess.PIPE)

    logger.info("Changing firewall policy in controller: '%s'" % iptable_cmd3)
    subprocess.call(iptable_cmd3, shell=True, stderr=subprocess.PIPE)

# Getting the different clients

    nova_client = os_utils.get_nova_client()
    neutron_client = os_utils.get_neutron_client()
    glance_client = os_utils.get_glance_client()

# Download the image

    if not os.path.isfile(IMAGE_PATH):
        logger.info("Downloading image")
        ft_utils.download_url(
            "http://artifacts.opnfv.org/sfc/demo/sf_nsh_colorado.qcow2",
            "/home/opnfv/functest/data/")
    else:
        logger.info("Using old image")

# Create glance image and the neutron network

    image_id = os_utils.create_glance_image(glance_client,
                                            IMAGE_NAME,
                                            IMAGE_PATH,
                                            disk=IMAGE_FORMAT,
                                            container="bare",
                                            public=True)

    network_dic = os_utils.create_network_full(neutron_client,
                                               NET_NAME,
                                               SUBNET_NAME,
                                               ROUTER_NAME,
                                               SUBNET_CIDR)
    if not network_dic:
        logger.error(
            "There has been a problem when creating the neutron network")
        sys.exit(-1)

    network_id = network_dic["net_id"]

    sg_id = os_utils.create_security_group_full(neutron_client,
                                                SECGROUP_NAME, SECGROUP_DESCR)

    # boot INTANCE
    logger.info("Creating instance '%s'..." % INSTANCE_NAME)
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n "
        "network=%s \n" % (INSTANCE_NAME, FLAVOR, image_id, network_id))
    instance = os_utils.create_instance_and_wait_for_active(FLAVOR,
                                                            image_id,
                                                            network_id,
                                                            INSTANCE_NAME)

    if instance is None:
        logger.error("Error while booting instance.")
        sys.exit(-1)
    # Retrieve IP of INSTANCE
    instance_ip = instance.networks.get(NET_NAME)[0]
    logger.debug("Instance '%s' got private ip '%s'." %
                 (INSTANCE_NAME, instance_ip))

    logger.info("Adding '%s' to security group '%s'..."
                % (INSTANCE_NAME, SECGROUP_NAME))
    os_utils.add_secgroup_to_instance(nova_client, instance.id, sg_id)

    logger.info("Creating floating IP for VM '%s'..." % INSTANCE_NAME)
    floatip_dic = os_utils.create_floating_ip(neutron_client)
    floatip_client = floatip_dic['fip_addr']
    # floatip_id = floatip_dic['fip_id']

    if floatip_client is None:
        logger.error("Cannot create floating IP.")
        sys.exit(-1)
    logger.info("Floating IP created: '%s'" % floatip_client)

    logger.info("Associating floating ip: '%s' to VM '%s' "
                % (floatip_client, INSTANCE_NAME))
    if not os_utils.add_floating_ip(nova_client, instance.id, floatip_client):
        logger.error("Cannot associate floating IP to VM.")
        sys.exit(-1)

# STARTING SECOND VM (server) ###

    # boot INTANCE
    logger.info("Creating instance '%s'..." % INSTANCE_NAME)
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n "
        "network=%s \n" % (INSTANCE_NAME, FLAVOR, image_id, network_id))
    instance_2 = os_utils.create_instance_and_wait_for_active(FLAVOR,
                                                              image_id,
                                                              network_id,
                                                              INSTANCE_NAME_2)

    if instance_2 is None:
        logger.error("Error while booting instance.")
        sys.exit(-1)
    # Retrieve IP of INSTANCE
    instance_ip_2 = instance_2.networks.get(NET_NAME)[0]
    logger.debug("Instance '%s' got private ip '%s'." %
                 (INSTANCE_NAME_2, instance_ip_2))

    logger.info("Adding '%s' to security group '%s'..."
                % (INSTANCE_NAME_2, SECGROUP_NAME))
    os_utils.add_secgroup_to_instance(nova_client, instance_2.id, sg_id)

    logger.info("Creating floating IP for VM '%s'..." % INSTANCE_NAME_2)
    floatip_dic = os_utils.create_floating_ip(neutron_client)
    floatip_server = floatip_dic['fip_addr']
    # floatip_id = floatip_dic['fip_id']

    if floatip_server is None:
        logger.error("Cannot create floating IP.")
        sys.exit(-1)
    logger.info("Floating IP created: '%s'" % floatip_server)

    logger.info("Associating floating ip: '%s' to VM '%s' "
                % (floatip_server, INSTANCE_NAME_2))

    if not os_utils.add_floating_ip(nova_client,
                                    instance_2.id,
                                    floatip_server):
        logger.error("Cannot associate floating IP to VM.")
        sys.exit(-1)

    # CREATION OF THE 2 SF ####

    tacker_script = "%s/testcases/features/sfc/%s" % \
                    (FUNCTEST_REPO, TACKER_SCRIPT)
    logger.info("Executing tacker script: '%s'" % tacker_script)
    subprocess.call(tacker_script, shell=True)

    # SSH CALL TO START HTTP SERVER
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(floatip_server, username="root",
                    password="opnfv", timeout=2)
        command = "python -m SimpleHTTPServer 80 > /dev/null 2>&1 &"
        logger.info("Starting HTTP server")
        (stdin, stdout, stderr) = ssh.exec_command(command)
    except:
        logger.debug("Waiting for %s..." % floatip_server)
        time.sleep(6)
        # timeout -= 1

    instances = nova_client.servers.list(search_opts={'all_tenants': 1})
    ips = []
    try:
        for instance in instances:
            if "server" not in instance.name:
                if "client" not in instance.name:
                    logger.debug(
                        "This is the instance name: %s " % instance.name)
                    floatip_dic = os_utils.create_floating_ip(neutron_client)
                    floatip = floatip_dic['fip_addr']
                    ips.append(floatip)
                    instance.add_floating_ip(floatip)
    except:
        logger.debug("Problems assigning floating IP to SFs")

    # If no IPs were obtained, then we cant continue
    if not ips:
        logger.error('Failed to obtain IPs, cant continue, exiting')
        return

    logger.debug("Floating IPs for SFs: %s..." % ips)

    # Check SSH connectivity to VNFs
    r = 0
    retries = 100
    check = [False, False]

    logger.info("Checking SSH connectivity to the SFs with ips %s" % str(ips))
    while r < retries and not all(check):
        try:
            check = [check_ssh(ips[0]), check_ssh(ips[1])]
        except Exception:
            logger.exception("SSH check failed")
            check = [False, False]
        time.sleep(3)
        r += 1

    logger.info("SSH connectivity to the SFs established")

    if not all(check):
        logger.error("Cannot establish SSH connection to the SFs")
        # TODO: Handle this with appropriate exit condition

    # SSH TO START THE VXLAN_TOOL ON SF1
    logger.info("Configuring the SFs")
    try:
        ssh.connect(ips[0], username="root",
                    password="opnfv", timeout=2)
        command = ("nohup python vxlan_tool.py -i eth0 "
                   "-d forward -v off -b 80 > /dev/null 2>&1 &")
        (stdin, stdout, stderr) = ssh.exec_command(command)
    except:
        logger.debug("Waiting for %s..." % ips[0])
        time.sleep(6)
        # timeout -= 1

    try:
        while 1:
            (stdin, stdout, stderr) = ssh.exec_command(
                "ps aux | grep \"vxlan_tool.py\" | grep -v grep")
            if len(stdout.readlines()) > 0:
                logger.debug("HTTP firewall started")
                break
            else:
                logger.debug("HTTP firewall not started")
                time.sleep(3)
    except Exception:
        logger.exception("vxlan_tool not started in SF1")

    # SSH TO START THE VXLAN_TOOL ON SF2
    try:
        ssh.connect(ips[1], username="root",
                    password="opnfv", timeout=2)
        command = ("nohup python vxlan_tool.py -i eth0 "
                   "-d forward -v off -b 22 > /dev/null 2>&1 &")
        (stdin, stdout, stderr) = ssh.exec_command(command)
    except:
        logger.debug("Waiting for %s..." % ips[1])
        time.sleep(6)
        # timeout -= 1

    try:
        while 1:
            (stdin, stdout, stderr) = ssh.exec_command(
                "ps aux | grep \"vxlan_tool.py\" | grep -v grep")
            if len(stdout.readlines()) > 0:
                logger.debug("SSH firewall started")
                break
            else:
                logger.debug("SSH firewall not started")
                time.sleep(3)
    except Exception:
        logger.exception("vxlan_tool not started in SF2")

    # SSH to modify the classification flows in compute

    contr_cmd3 = ("sshpass -p r00tme ssh " + ssh_options + " root@10.20.0.2"
                  " 'ssh " + ip_compute + " 'bash correct_classifier.bash''")
    logger.info("Executing script to modify the classi: '%s'" % contr_cmd3)
    process = subprocess.Popen(contr_cmd3,
                               shell=True,
                               stdout=subprocess.PIPE)

    i = 0

    # SSH TO EXECUTE cmd_client
    logger.info("TEST STARTED")
    try:
        ssh.connect(floatip_client, username="root",
                    password="opnfv", timeout=2)
        command = "nc -w 5 -zv " + instance_ip_2 + " 22 2>&1"
        (stdin, stdout, stderr) = ssh.exec_command(command)

        # WRITE THE CORRECT WAY TO DO LOGGING
        if "timed out" in stdout.readlines()[0]:
            logger.info('\033[92m' + "TEST 1 [PASSED] "
                        "==> SSH BLOCKED" + '\033[0m')
            i = i + 1
            json_results.update({"Test 1: SSH Blocked": "Passed"})
        else:
            logger.error('\033[91m' + "TEST 1 [FAILED] "
                         "==> SSH NOT BLOCKED" + '\033[0m')
            status = "FAIL"
            json_results.update({"Test 1: SSH Blocked": "Failed"})
            failures += 1
    except:
        logger.debug("Waiting for %s..." % floatip_client)
        time.sleep(6)
        # timeout -= 1

    # SSH TO EXECUTE cmd_client
    try:
        ssh.connect(floatip_client, username="root",
                    password="opnfv", timeout=2)
        command = "nc -w 5 -zv " + instance_ip_2 + " 80 2>&1"
        (stdin, stdout, stderr) = ssh.exec_command(command)

        if "succeeded" in stdout.readlines()[0]:
            logger.info('\033[92m' + "TEST 2 [PASSED] "
                        "==> HTTP WORKS" + '\033[0m')
            i = i + 1
            json_results.update({"Test 2: HTTP works": "Passed"})
        else:
            logger.error('\033[91m' + "TEST 2 [FAILED] "
                         "==> HTTP BLOCKED" + '\033[0m')
            status = "FAIL"
            json_results.update({"Test 2: HTTP works": "Failed"})
            failures += 1
    except:
        logger.debug("Waiting for %s..." % floatip_client)
        time.sleep(6)
        # timeout -= 1

    # CHANGE OF CLASSIFICATION #
    logger.info("Changing the classification")
    tacker_classi = "%s/testcases/features/sfc/%s" % \
                    (FUNCTEST_REPO, TACKER_CHANGECLASSI)
    subprocess.call(tacker_classi, shell=True)

    logger.info("Wait for ODL to update the classification rules in OVS")
    time.sleep(10)

    # SSH to modify the classification flows in compute

    contr_cmd4 = ("sshpass -p r00tme ssh " + ssh_options + " root@10.20.0.2"
                  " 'ssh " + ip_compute + " 'bash correct_classifier.bash''")
    logger.info("Executing script to modify the classi: '%s'" % contr_cmd4)
    process = subprocess.Popen(contr_cmd4,
                               shell=True,
                               stdout=subprocess.PIPE)

    # SSH TO EXECUTE cmd_client

    try:
        ssh.connect(floatip_client, username="root",
                    password="opnfv", timeout=2)
        command = "nc -w 5 -zv " + instance_ip_2 + " 80 2>&1"
        (stdin, stdout, stderr) = ssh.exec_command(command)

        if "timed out" in stdout.readlines()[0]:
            logger.info('\033[92m' + "TEST 3 [PASSED] "
                        "==> HTTP BLOCKED" + '\033[0m')
            i = i + 1
            json_results.update({"Test 3: HTTP Blocked": "Passed"})
        else:
            logger.error('\033[91m' + "TEST 3 [FAILED] "
                         "==> HTTP NOT BLOCKED" + '\033[0m')
            status = "FAIL"
            json_results.update({"Test 3: HTTP Blocked": "Failed"})
            failures += 1
    except:
        logger.debug("Waiting for %s..." % floatip_client)
        time.sleep(6)
        # timeout -= 1

    # SSH TO EXECUTE cmd_client
    try:
        ssh.connect(floatip_client, username="root",
                    password="opnfv", timeout=2)
        command = "nc -w 5 -zv " + instance_ip_2 + " 22 2>&1"
        (stdin, stdout, stderr) = ssh.exec_command(command)

        if "succeeded" in stdout.readlines()[0]:
            logger.info('\033[92m' + "TEST 4 [PASSED] "
                        "==> SSH WORKS" + '\033[0m')
            i = i + 1
            json_results.update({"Test 4: SSH works": "Passed"})
        else:
            logger.error('\033[91m' + "TEST 4 [FAILED] "
                         "==> SSH BLOCKED" + '\033[0m')
            status = "FAIL"
            json_results.update({"Test 4: SSH works": "Failed"})
            failures += 1
    except:
        logger.debug("Waiting for %s..." % floatip_client)
        time.sleep(6)
        # timeout -= 1

    if i == 4:
        for x in range(0, 5):
            logger.info('\033[92m' + "SFC TEST WORKED"
                        " :) \n" + '\033[0m')

    if args.report:
        stop_time = time.time()
        json_results.update({"tests": "4", "failures": int(failures)})
        logger.debug("Promise Results json: " + str(json_results))
        ft_utils.push_results_to_db("sfc",
                                    "functest-odl-sfc",
                                    start_time,
                                    stop_time,
                                    status,
                                    json_results)
    if status == "PASS":
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
