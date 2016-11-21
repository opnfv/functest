import os
import pprint
import re
import sys
import time

import paramiko
from scp import SCPClient

import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
import functest.utils.functest_constants as ft_constants
FUNCTEST_REPO = ft_constants.FUNCTEST_REPO_DIR

NAME_VM_1 = ft_constants.NAME_VM_1
NAME_VM_2 = ft_constants.NAME_VM_2

VM_BOOT_TIMEOUT = 180
VM_DELETE_TIMEOUT = 100
PING_TIMEOUT = ft_constants.PING_TIMEOUT

VPING_IMAGE_NAME = ft_constants.VPING__IMAGE_NAME
GLANCE_IMAGE_FILENAME = ft_constants.GLANCE_IMAGE_FILENAME
GLANCE_IMAGE_FORMAT = ft_constants.GLANCE_IMAGE_FORMAT
GLANCE_IMAGE_PATH = ft_constants.FUNCTEST_DATA_DIR + \
    "/" + GLANCE_IMAGE_FILENAME


VPING_VM_FLAVOR = ft_constants.VPING_VM_FLAVOR

# NEUTRON Private Network parameters
VPING_PRIVATE_NET_NAME = ft_constants.VPING_PRIVATE_NET_NAME
VPING_PRIVATE_SUBNET_NAME = ft_constants.VPING_PRIVATE_SUBNET_NAME
VPING_PRIVATE_SUBNET_CIDR = ft_constants.VPING_PRIVATE_SUBNET_CIDR
VPING_ROUTER_NAME = ft_constants.VPING_ROUTER_NAME

VPING_SECGROUP_NAME = ft_constants.VPING_SECGROUP_NAME
VPING_SECGROUP_DESCR = ft_constants.VPING_SECGROUP_DESCR


class GlobalVariables:
    neutron_client = None
    glance_client = None
    nova_client = None
    logger = None


pp = pprint.PrettyPrinter(indent=4)


def pMsg(value):
    """pretty printing"""
    pp.pprint(value)


def check_repo_exist():
    if not os.path.exists(FUNCTEST_REPO):
        GlobalVariables.logger.error("Functest repository not found '%s'"
                                     % FUNCTEST_REPO)
        exit(-1)


def get_vmname_1():
    return NAME_VM_1


def get_vmname_2():
    return NAME_VM_2


def init(vping_logger):
    GlobalVariables.nova_client = os_utils.get_nova_client()
    GlobalVariables.neutron_client = os_utils.get_neutron_client()
    GlobalVariables.glance_client = os_utils.get_glance_client()
    GlobalVariables.logger = vping_logger


def waitVmActive(nova, vm):

    # sleep and wait for VM status change
    sleep_time = 3
    count = VM_BOOT_TIMEOUT / sleep_time
    while True:
        status = os_utils.get_instance_status(nova, vm)
        GlobalVariables.logger.debug("Status: %s" % status)
        if status == "ACTIVE":
            return True
        if status == "ERROR" or status == "error":
            return False
        if count == 0:
            GlobalVariables.logger.debug("Booting a VM timed out...")
            return False
        count -= 1
        time.sleep(sleep_time)
    return False


def create_security_group():
    sg_id = os_utils.get_security_group_id(GlobalVariables.neutron_client,
                                           VPING_SECGROUP_NAME)
    if sg_id != '':
        GlobalVariables.logger.info("Using existing security group '%s'..."
                                    % VPING_SECGROUP_NAME)
    else:
        GlobalVariables.logger.info("Creating security group  '%s'..."
                                    % VPING_SECGROUP_NAME)
        SECGROUP = \
            os_utils.create_security_group(GlobalVariables.neutron_client,
                                           VPING_SECGROUP_NAME,
                                           VPING_SECGROUP_DESCR)
        if not SECGROUP:
            GlobalVariables.logger.error(
                "Failed to create the security group...")
            return False

        sg_id = SECGROUP['id']

        GlobalVariables.logger.debug(
            "Security group '%s'with ID=%s created successfully."
            % (SECGROUP['name'], sg_id))

        GlobalVariables.logger.debug(
            "Adding ICMP rules in security group '%s'..."
            % VPING_SECGROUP_NAME)
        if not os_utils.create_secgroup_rule(GlobalVariables.neutron_client,
                                             sg_id, 'ingress', 'icmp'):
            GlobalVariables.logger.error(
                "Failed to create the security group rule...")
            return False

        GlobalVariables.logger.debug(
            "Adding SSH rules in security group '%s'..."
            % VPING_SECGROUP_NAME)
        if not os_utils.create_secgroup_rule(GlobalVariables.neutron_client,
                                             sg_id, 'ingress', 'tcp',
                                             '22', '22'):
            GlobalVariables.logger.error(
                "Failed to create the security group rule...")
            return False

        if not os_utils.create_secgroup_rule(
                GlobalVariables.neutron_client, sg_id,
                'egress', 'tcp', '22', '22'):
            GlobalVariables.logger.error(
                "Failed to create the security group rule...")
            return False
    return sg_id


def create_image():
    _, image_id = os_utils.get_or_create_image(VPING_IMAGE_NAME,
                                               GLANCE_IMAGE_PATH,
                                               GLANCE_IMAGE_FORMAT)
    if not image_id:
        exit(-1)

    return image_id


def get_flavor():
    EXIT_CODE = -1

    # Check if the given flavor exists
    try:
        flavor = GlobalVariables.nova_client.flavors.find(name=VPING_VM_FLAVOR)
        GlobalVariables.logger.info(
            "Using existing Flavor '%s'..." % VPING_VM_FLAVOR)
        return flavor
    except:
        GlobalVariables.logger.error("Flavor '%s' not found."
                                     % VPING_VM_FLAVOR)
        GlobalVariables.logger.info("Available flavors are: ")
        pMsg(GlobalVariables.nova_client.flavor.list())
        exit(EXIT_CODE)


def create_network_full():
    EXIT_CODE = -1

    network_dic = os_utils.create_network_full(GlobalVariables.neutron_client,
                                               VPING_PRIVATE_NET_NAME,
                                               VPING_PRIVATE_SUBNET_NAME,
                                               VPING_ROUTER_NAME,
                                               VPING_PRIVATE_SUBNET_CIDR)

    if not network_dic:
        GlobalVariables.logger.error(
            "There has been a problem when creating the neutron network")
        exit(EXIT_CODE)
    network_id = network_dic["net_id"]
    return network_id


def delete_exist_vms():
    servers = GlobalVariables.nova_client.servers.list()
    for server in servers:
        if server.name == NAME_VM_1 or server.name == NAME_VM_2:
            GlobalVariables.logger.info("Instance %s found. Deleting..."
                                        % server.name)
            server.delete()


def is_userdata(case):
    return case == 'vping_userdata'


def is_ssh(case):
    return case == 'vping_ssh'


def boot_vm(case, name, image_id, flavor, network_id, test_ip, sg_id):
    EXIT_CODE = -1

    config = dict()
    config['name'] = name
    config['flavor'] = flavor
    config['image'] = image_id
    config['nics'] = [{"net-id": network_id}]
    if is_userdata(case):
        config['config_drive'] = True
        if name == NAME_VM_2:
            u = ("#!/bin/sh\n\n"
                 "while true; do\n"
                 " ping -c 1 %s 2>&1 >/dev/null\n"
                 " RES=$?\n"
                 " if [ \"Z$RES\" = \"Z0\" ] ; then\n"
                 "  echo 'vPing OK'\n"
                 "  break\n"
                 " else\n"
                 "  echo 'vPing KO'\n"
                 " fi\n"
                 " sleep 1\n"
                 "done\n" % test_ip)
            config['userdata'] = u

    GlobalVariables.logger.info("Creating instance '%s'..." % name)
    GlobalVariables.logger.debug("Configuration: %s" % config)
    vm = GlobalVariables.nova_client.servers.create(**config)

    # wait until VM status is active
    if not waitVmActive(GlobalVariables.nova_client, vm):

        GlobalVariables.logger.error(
            "Instance '%s' cannot be booted. Status is '%s'"
            % (name, os_utils.get_instance_status(
                GlobalVariables.nova_client, vm)))
        exit(EXIT_CODE)
    else:
        GlobalVariables.logger.info("Instance '%s' is ACTIVE." % name)

    add_secgroup(name, vm.id, sg_id)

    return vm


def get_test_ip(vm):
    test_ip = vm.networks.get(VPING_PRIVATE_NET_NAME)[0]
    GlobalVariables.logger.debug("Instance '%s' got %s" % (vm.name, test_ip))
    return test_ip


def add_secgroup(vmname, vm_id, sg_id):
    GlobalVariables.logger.info("Adding '%s' to security group '%s'..." %
                                (vmname, VPING_SECGROUP_NAME))
    os_utils.add_secgroup_to_instance(GlobalVariables.nova_client,
                                      vm_id, sg_id)


def add_float_ip(vm):
    EXIT_CODE = -1

    GlobalVariables.logger.info("Creating floating IP for VM '%s'..."
                                % NAME_VM_2)
    floatip_dic = os_utils.create_floating_ip(GlobalVariables.neutron_client)
    floatip = floatip_dic['fip_addr']

    if floatip is None:
        GlobalVariables.logger.error("Cannot create floating IP.")
        exit(EXIT_CODE)
    GlobalVariables.logger.info("Floating IP created: '%s'" % floatip)

    GlobalVariables.logger.info("Associating floating ip: '%s' to VM '%s' "
                                % (floatip, NAME_VM_2))
    if not os_utils.add_floating_ip(GlobalVariables.nova_client,
                                    vm.id, floatip):
        GlobalVariables.logger.error("Cannot associate floating IP to VM.")
        exit(EXIT_CODE)

    return floatip


def establish_ssh(vm, floatip):
    EXIT_CODE = -1

    GlobalVariables.logger.info("Trying to establish SSH connection to %s..."
                                % floatip)
    username = 'cirros'
    password = 'cubswin:)'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    timeout = 50
    nolease = False
    got_ip = False
    discover_count = 0
    cidr_first_octet = VPING_PRIVATE_SUBNET_CIDR.split('.')[0]
    while timeout > 0:
        try:
            ssh.connect(floatip, username=username,
                        password=password, timeout=2)
            GlobalVariables.logger.debug("SSH connection established to %s."
                                         % floatip)
            break
        except:
            GlobalVariables.logger.debug("Waiting for %s..." % floatip)
            time.sleep(6)
            timeout -= 1

        console_log = vm.get_console_output()

        # print each "Sending discover" captured on the console log
        if (len(re.findall("Sending discover", console_log)) >
                discover_count and not got_ip):
            discover_count += 1
            GlobalVariables.logger.debug(
                "Console-log '%s': Sending discover..." % NAME_VM_2)

        # check if eth0 got an ip,the line looks like this:
        # "inet addr:192.168."....
        # if the dhcp agent fails to assing ip, this line will not appear
        if "inet addr:" + cidr_first_octet in console_log and not got_ip:
            got_ip = True
            GlobalVariables.logger.debug(
                "The instance '%s' succeeded to get the IP "
                "from the dhcp agent." % NAME_VM_2)

        # if dhcp doesnt work,it shows "No lease, failing".The test will fail
        if "No lease, failing" in console_log and not nolease and not got_ip:
            nolease = True
            GlobalVariables.logger.debug(
                "Console-log '%s': No lease, failing..." % NAME_VM_2)
            GlobalVariables.logger.info(
                "The instance failed to get an IP from the "
                "DHCP agent. The test will probably timeout...")

    if timeout == 0:  # 300 sec timeout (5 min)
        GlobalVariables.logger.error(
            "Cannot establish connection to IP '%s'. Aborting" % floatip)
        exit(EXIT_CODE)
    return ssh


def transfer_ping_script(ssh, floatip):
    EXIT_CODE = -1

    GlobalVariables.logger.info("Trying to transfer ping.sh to %s..."
                                % floatip)
    scp = SCPClient(ssh.get_transport())

    ping_script = (
        FUNCTEST_REPO + "/functest/opnfv_tests/OpenStack/vPing/ping.sh")
    try:
        scp.put(ping_script, "~/")
    except:
        GlobalVariables.logger.error("Cannot SCP the file '%s' to VM '%s'"
                                     % (ping_script, floatip))
        exit(EXIT_CODE)

    cmd = 'chmod 755 ~/ping.sh'
    (stdin, stdout, stderr) = ssh.exec_command(cmd)
    for line in stdout.readlines():
        print line


def do_vping_ssh(ssh, test_ip):
    GlobalVariables.logger.info("Waiting for ping...")

    sec = 0
    cmd = '~/ping.sh ' + test_ip
    flag = False

    while True:
        time.sleep(1)
        (stdin, stdout, stderr) = ssh.exec_command(cmd)
        output = stdout.readlines()

        for line in output:
            if "vPing OK" in line:
                GlobalVariables.logger.info("vPing detected!")
                EXIT_CODE = 0
                flag = True
                break

            elif sec == PING_TIMEOUT:
                GlobalVariables.logger.info("Timeout reached.")
                flag = True
                break
        if flag:
            break
        GlobalVariables.logger.debug("Pinging %s. Waiting for response..."
                                     % test_ip)
        sec += 1
    return EXIT_CODE, time.time()


def do_vping_userdata(vm, test_ip):
    GlobalVariables.logger.info("Waiting for ping...")
    EXIT_CODE = -1
    sec = 0
    metadata_tries = 0

    while True:
        time.sleep(1)
        console_log = vm.get_console_output()
        if "vPing OK" in console_log:
            GlobalVariables.logger.info("vPing detected!")
            EXIT_CODE = 0
            break
        elif ("failed to read iid from metadata" in console_log or
              metadata_tries > 5):
            EXIT_CODE = -2
            break
        elif sec == PING_TIMEOUT:
            GlobalVariables.logger.info("Timeout reached.")
            break
        elif sec % 10 == 0:
            if "request failed" in console_log:
                GlobalVariables.logger.debug(
                    "It seems userdata is not supported in "
                    "nova boot. Waiting a bit...")
                metadata_tries += 1
            else:
                GlobalVariables.logger.debug(
                    "Pinging %s. Waiting for response..." % test_ip)
        sec += 1

    return EXIT_CODE, time.time()


def do_vping(case, vm, test_ip):
    if is_userdata(case):
        return do_vping_userdata(vm, test_ip)
    else:
        floatip = add_float_ip(vm)
        ssh = establish_ssh(vm, floatip)
        transfer_ping_script(ssh, floatip)
        return do_vping_ssh(ssh, test_ip)


def check_result(code, start_time, stop_time):
    test_status = "FAIL"
    if code == 0:
        GlobalVariables.logger.info("vPing OK")
        duration = round(stop_time - start_time, 1)
        GlobalVariables.logger.info("vPing duration:'%s'" % duration)
        test_status = "PASS"
    elif code == -2:
        duration = 0
        GlobalVariables.logger.info(
            "Userdata is not supported in nova boot. Aborting test...")
    else:
        duration = 0
        GlobalVariables.logger.error("vPing FAILED")

    details = {'timestart': start_time,
               'duration': duration,
               'status': test_status}

    return details


def push_result(report, case, start_time, stop_time, details):
    if report:
        try:
            GlobalVariables.logger.debug("Pushing vPing %s results into DB..."
                                         % case)
            ft_utils.push_results_to_db('functest',
                                        case,
                                        start_time,
                                        stop_time,
                                        details['status'],
                                        details=details)
        except:
            GlobalVariables.logger.error(
                "Error pushing results into Database '%s'" % sys.exc_info()[0])
