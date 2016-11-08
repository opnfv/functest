import argparse
import os
import subprocess
import sys
import time
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
import re
import json
import SSHUtils as ssh_utils
import ovs_utils
import thread

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")

args = parser.parse_args()

""" logging configuration """
logger = ft_logger.Logger("ODL_SFC").getLogger()

FUNCTEST_RESULTS_DIR = '/home/opnfv/functest/results/odl-sfc'
FUNCTEST_REPO = ft_utils.FUNCTEST_REPO
REPO_PATH = os.environ['repos_dir'] + '/functest/'
HOME = os.environ['HOME'] + "/"
CLIENT = "client"
SERVER = "server"
FLAVOR = "custom"
IMAGE_NAME = "sf_nsh_colorado"
IMAGE_FILENAME = "sf_nsh_colorado.qcow2"
IMAGE_FORMAT = "qcow2"
IMAGE_DIR = "/home/opnfv/functest/data"
IMAGE_PATH = IMAGE_DIR + "/" + IMAGE_FILENAME
IMAGE_URL = "http://artifacts.opnfv.org/sfc/demo/" + IMAGE_FILENAME

# NEUTRON Private Network parameters
NET_NAME = "example-net"
SUBNET_NAME = "example-subnet"
SUBNET_CIDR = "11.0.0.0/24"
ROUTER_NAME = "example-router"
SECGROUP_NAME = "example-sg"
SECGROUP_DESCR = "Example Security group"
SFC_TEST_DIR = REPO_PATH + "/testcases/features/sfc/"
TACKER_SCRIPT = SFC_TEST_DIR + "sfc_tacker.bash"
TACKER_CHANGECLASSI = SFC_TEST_DIR + "sfc_change_classi.bash"
ssh_options = '-q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
json_results = {"tests": 4, "failures": 0}

PROXY = {
    'ip': '10.20.0.2',
    'username': 'root',
    'password': 'r00tme'
}

# run given command locally and return commands output if success


def run_cmd(cmd, wdir=None, ignore_stderr=False, ignore_no_output=True):
    pipe = subprocess.Popen(cmd, shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, cwd=wdir)

    (output, errors) = pipe.communicate()
    if output:
        output = output.strip()
    if pipe.returncode < 0:
        logger.error(errors)
        return False
    if errors:
        logger.error(errors)
        if ignore_stderr:
            return True
        else:
            return False

    if ignore_no_output:
        if not output:
            return True

    return output

# run given command on OpenStack controller


def run_cmd_on_cntlr(cmd):
    ip_cntlrs = get_openstack_node_ips("controller")
    if not ip_cntlrs:
        return None

    ssh_cmd = "ssh %s %s %s" % (ssh_options, ip_cntlrs[0], cmd)
    return run_cmd_on_fm(ssh_cmd)

# run given command on OpenStack Compute node


def run_cmd_on_compute(cmd):
    ip_computes = get_openstack_node_ips("compute")
    if not ip_computes:
        return None

    ssh_cmd = "ssh %s %s %s" % (ssh_options, ip_computes[0], cmd)
    return run_cmd_on_fm(ssh_cmd)

# run given command on Fuel Master


def run_cmd_on_fm(cmd, username="root", passwd="r00tme"):
    ip = os.environ.get("INSTALLER_IP")
    ssh_cmd = "sshpass -p %s ssh %s %s@%s %s" % (
        passwd, ssh_options, username, ip, cmd)
    return run_cmd(ssh_cmd)

# run given command on Remote Machine, Can be VM


def run_cmd_remote(ip, cmd, username="root", passwd="opnfv"):
    ssh_opt_append = "%s -o ConnectTimeout=50 " % ssh_options
    ssh_cmd = "sshpass -p %s ssh %s %s@%s %s" % (
        passwd, ssh_opt_append, username, ip, cmd)
    return run_cmd(ssh_cmd)

# Get OpenStack Nodes IP Address


def get_openstack_node_ips(role):
    fuel_env = os.environ.get("FUEL_ENV")
    if fuel_env is not None:
        cmd = "fuel2 node list -f json -e %s" % fuel_env
    else:
        cmd = "fuel2 node list -f json"

    nodes = run_cmd_on_fm(cmd)
    ips = []
    nodes = json.loads(nodes)
    for node in nodes:
        if role in node["roles"]:
            ips.append(node["ip"])

    return ips

# Configures IPTABLES on OpenStack Controller


def configure_iptables():
    iptable_cmds = ["iptables -P INPUT ACCEPT",
                    "iptables -t nat -P INPUT ACCEPT",
                    "iptables -A INPUT -m state \
                    --state NEW,ESTABLISHED,RELATED -j ACCEPT"]

    for cmd in iptable_cmds:
        logger.info("Configuring %s on contoller" % cmd)
        run_cmd_on_cntlr(cmd)

    return


def download_image():
    if not os.path.isfile(IMAGE_PATH):
        logger.info("Downloading image")
        ft_utils.download_url(IMAGE_URL, IMAGE_DIR)

    logger.info("Using old image")
    return


def setup_glance(glance_client):
    image_id = os_utils.create_glance_image(glance_client,
                                            IMAGE_NAME,
                                            IMAGE_PATH,
                                            disk=IMAGE_FORMAT,
                                            container="bare",
                                            public=True)

    return image_id


def setup_neutron(neutron_client):
    n_dict = os_utils.create_network_full(neutron_client,
                                          NET_NAME,
                                          SUBNET_NAME,
                                          ROUTER_NAME,
                                          SUBNET_CIDR)
    if not n_dict:
        logger.error("failed to create neutron network")
        sys.exit(-1)

    network_id = n_dict["net_id"]
    return network_id


def setup_ingress_egress_secgroup(neutron_client, protocol,
                                  min_port=None, max_port=None):
    secgroups = os_utils.get_security_groups(neutron_client)
    for sg in secgroups:
        os_utils.create_secgroup_rule(neutron_client, sg['id'],
                                      'ingress', protocol,
                                      port_range_min=min_port,
                                      port_range_max=max_port)
        os_utils.create_secgroup_rule(neutron_client, sg['id'],
                                      'egress', protocol,
                                      port_range_min=min_port,
                                      port_range_max=max_port)
    return


def setup_security_groups(neutron_client):
    sg_id = os_utils.create_security_group_full(neutron_client,
                                                SECGROUP_NAME, SECGROUP_DESCR)
    setup_ingress_egress_secgroup(neutron_client, "icmp")
    setup_ingress_egress_secgroup(neutron_client, "udp", 67, 68)
    setup_ingress_egress_secgroup(neutron_client, "tcp", 22, 22)
    setup_ingress_egress_secgroup(neutron_client, "tcp", 80, 80)
    return sg_id


def boot_instance(nova_client, name, flavor, image_id, network_id, sg_id):
    logger.info("Creating instance '%s'..." % name)
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n "
        "network=%s \n" % (name, flavor, image_id, network_id))

    instance = os_utils.create_instance_and_wait_for_active(flavor,
                                                            image_id,
                                                            network_id,
                                                            name)

    if instance is None:
        logger.error("Error while booting instance.")
        sys.exit(-1)

    instance_ip = instance.networks.get(NET_NAME)[0]
    logger.debug("Instance '%s' got private ip '%s'." %
                 (name, instance_ip))

    logger.info("Adding '%s' to security group %s" % (name, SECGROUP_NAME))
    os_utils.add_secgroup_to_instance(nova_client, instance.id, sg_id)

    return instance_ip


def ping(remote, pkt_cnt=1, iface=None, retries=100, timeout=None):
    ping_cmd = 'ping'

    if timeout:
        ping_cmd = ping_cmd + ' -w %s' % timeout

    grep_cmd = "grep -e 'packet loss' -e rtt"

    if iface is not None:
        ping_cmd = ping_cmd + ' -I %s' % iface

    ping_cmd = ping_cmd + ' -i 0 -c %d %s' % (pkt_cnt, remote)
    cmd = ping_cmd + '|' + grep_cmd

    while retries > 0:
        output = run_cmd(cmd)
        if not output:
            return False

        match = re.search('(\d*)% packet loss', output)
        if not match:
            return False

        packet_loss = int(match.group(1))
        if packet_loss == 0:
            return True

        retries = retries - 1

    return False


def get_floating_ips(nova_client, neutron_client):
    ips = []
    instances = nova_client.servers.list(search_opts={'all_tenants': 1})
    for instance in instances:
        floatip_dic = os_utils.create_floating_ip(neutron_client)
        floatip = floatip_dic['fip_addr']
        instance.add_floating_ip(floatip)
        logger.info("Instance name and ip %s:%s " % (instance.name, floatip))
        logger.info("Waiting for instance %s:%s to come up" %
                    (instance.name, floatip))
        if not ping(floatip):
            logger.info("Instance %s:%s didn't come up" %
                        (instance.name, floatip))
            sys.exit(1)

        if instance.name == "server":
            logger.info("Server:%s is reachable" % floatip)
            server_ip = floatip
        elif instance.name == "client":
            logger.info("Client:%s is reachable" % floatip)
            client_ip = floatip
        else:
            logger.info("SF:%s is reachable" % floatip)
            ips.append(floatip)

    return server_ip, client_ip, ips[1], ips[0]

# Start http server on a give machine, Can be VM


def start_http_server(ip):
    cmd = "\'python -m SimpleHTTPServer 80"
    cmd = cmd + " > /dev/null 2>&1 &\'"
    return run_cmd_remote(ip, cmd)

# Set firewall using vxlan_tool.py on a give machine, Can be VM


def vxlan_firewall(sf, iface="eth0", port="22", block=True):
    cmd = "python vxlan_tool.py"
    cmd = cmd + " -i " + iface + " -d forward -v off"
    if block:
        cmd = "python vxlan_tool.py -i eth0 -d forward -v off -b " + port

    cmd = "sh -c 'cd /root;nohup " + cmd + " > /dev/null 2>&1 &'"
    run_cmd_remote(sf, cmd)

# Run netcat on a give machine, Can be VM


def netcat(s_ip, c_ip, port="80", timeout=5):
    cmd = "nc -zv "
    cmd = cmd + " -w %s %s %s" % (timeout, s_ip, port)
    cmd = cmd + " 2>&1"
    output = run_cmd_remote(c_ip, cmd)
    logger.info("%s" % output)
    return output


def is_ssh_blocked(srv_prv_ip, client_ip):
    res = netcat(srv_prv_ip, client_ip, port="22")
    match = re.search("nc:.*timed out:.*", res, re.M)
    if match:
        return True

    return False


def is_http_blocked(srv_prv_ip, client_ip):
    res = netcat(srv_prv_ip, client_ip, port="80")
    match = re.search(".* 80 port.* succeeded!", res, re.M)
    if match:
        return False

    return True


def capture_err_logs(controller_clients, compute_clients, error):
    ovs_logger = ovs_utils.OVSLogger(
        os.path.join(os.getcwd(), 'ovs-logs'),
        FUNCTEST_RESULTS_DIR)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    ovs_logger.dump_ovs_logs(controller_clients,
                             compute_clients,
                             related_error=error,
                             timestamp=timestamp)
    return


def update_json_results(name, result):
    json_results.update({name: result})
    if result is not "Passed":
        json_results["failures"] += 1

    return


def get_ssh_clients(role):
    clients = []
    for ip in get_openstack_node_ips(role):
        s_client = ssh_utils.get_ssh_client(ip,
                                            'root',
                                            proxy=PROXY)
        clients.append(s_client)

    return clients

# Check SSH connectivity to VNFs


def check_ssh(ips, retries=100):
    check = [False, False]
    logger.info("Checking SSH connectivity to the SFs with ips %s" % str(ips))
    while retries and not all(check):
        for index, ip in enumerate(ips):
            check[index] = run_cmd_remote(ip, "exit")

        if all(check):
            logger.info("SSH connectivity to the SFs established")
            return True

        time.sleep(3)
        retries -= 1

    return False

# Measure the time it takes to update the classification rules


def capture_time_log(compute_clients):
    ovs_logger = ovs_utils.OVSLogger(
        os.path.join(os.getcwd(), 'ovs-logs'),
        "test")
    i = 0
    first_RSP = ""
    start_time = time.time()
    while True:
        output = ovs_logger.ofctl_time_counter(compute_clients[0])
        rsps = output.split('\n')
        if not i:
            first_RSP = rsps[0]
            i = i + 1
        if(first_RSP != rsps[0]):
            if (rsps[0] == rsps[1]):
                stop_time = time.time()
                logger.info("classification rules updated")
                difference = stop_time - start_time
                logger.info("It took %s seconds" % difference)
                break
        time.sleep(1)
    return


def main():
    installer_type = os.environ.get("INSTALLER_TYPE")
    if installer_type != "fuel":
        logger.error(
            '\033[91mCurrently supported only Fuel Installer type\033[0m')
        sys.exit(1)

    installer_ip = os.environ.get("INSTALLER_IP")
    if not installer_ip:
        logger.error(
            '\033[91minstaller ip is not set\033[0m')
        logger.error(
            '\033[91mexport INSTALLER_IP=<ip>\033[0m')
        sys.exit(1)

    env_list = run_cmd_on_fm("fuel2 env list -f json")
    fuel_env = os.environ.get("FUEL_ENV")
    if len(eval(env_list)) > 1 and fuel_env is None:
        out = run_cmd_on_fm("fuel env")
        logger.error(
            '\033[91mMore than one fuel env found\033[0m\n %s' % out)
        logger.error(
            '\033[91mexport FUEL_ENV=<env-id> to set ENV\033[0m')
        sys.exit(1)

    start_time = time.time()
    status = "PASS"
    configure_iptables()
    download_image()
    _, custom_flv_id = os_utils.get_or_create_flavor(
        FLAVOR, 1500, 10, 1, public=True)
    if not custom_flv_id:
        logger.error("Failed to create custom flavor")
        sys.exit(1)

    glance_client = os_utils.get_glance_client()
    neutron_client = os_utils.get_neutron_client()
    nova_client = os_utils.get_nova_client()

    controller_clients = get_ssh_clients("controller")
    compute_clients = get_ssh_clients("compute")

    image_id = setup_glance(glance_client)
    network_id = setup_neutron(neutron_client)
    sg_id = setup_security_groups(neutron_client)

    boot_instance(
        nova_client, CLIENT, FLAVOR, image_id, network_id, sg_id)
    srv_prv_ip = boot_instance(
        nova_client, SERVER, FLAVOR, image_id, network_id, sg_id)

    subprocess.call(TACKER_SCRIPT, shell=True)

    # Start measuring the time it takes to implement the classification rules
    try:
        thread.start_new_thread(capture_time_log, (compute_clients,))
    except Exception, e:
        logger.error("Unable to start the thread that counts time %s" % e)

    server_ip, client_ip, sf1, sf2 = get_floating_ips(
        nova_client, neutron_client)

    if not check_ssh([sf1, sf2]):
        logger.error("Cannot establish SSH connection to the SFs")
        sys.exit(1)

    logger.info("Starting HTTP server on %s" % server_ip)
    if not start_http_server(server_ip):
        logger.error(
            '\033[91mFailed to start HTTP server on %s\033[0m' % server_ip)
        sys.exit(1)

    logger.info("Starting HTTP firewall on %s" % sf2)
    vxlan_firewall(sf2, port="80")
    logger.info("Starting SSH firewall on %s" % sf1)
    vxlan_firewall(sf1, port="22")

    logger.info("Wait for ODL to update the classification rules in OVS")
    time.sleep(120)

    logger.info("Test SSH")
    if is_ssh_blocked(srv_prv_ip, client_ip):
        logger.info('\033[92mTEST 1 [PASSED] ==> SSH BLOCKED\033[0m')
        update_json_results("Test 1: SSH Blocked", "Passed")
    else:
        error = ('\033[91mTEST 1 [FAILED] ==> SSH NOT BLOCKED\033[0m')
        logger.error(error)
        capture_err_logs(controller_clients, compute_clients, error)
        update_json_results("Test 1: SSH Blocked", "Failed")

    logger.info("Test HTTP")
    if not is_http_blocked(srv_prv_ip, client_ip):
        logger.info('\033[92mTEST 2 [PASSED] ==> HTTP WORKS\033[0m')
        update_json_results("Test 2: HTTP works", "Passed")
    else:
        error = ('\033[91mTEST 2 [FAILED] ==> HTTP BLOCKED\033[0m')
        logger.error(error)
        capture_err_logs(controller_clients, compute_clients, error)
        update_json_results("Test 2: HTTP works", "Failed")

    logger.info("Changing the classification")
    subprocess.call(TACKER_CHANGECLASSI, shell=True)

    # Start measuring the time it takes to implement the classification rules
    try:
        thread.start_new_thread(capture_time_log, (compute_clients,))
    except Exception, e:
        logger.error("Unable to start the thread that counts time %s" % e)

    logger.info("Wait for ODL to update the classification rules in OVS")
    time.sleep(100)

    logger.info("Test HTTP")
    if is_http_blocked(srv_prv_ip, client_ip):
        logger.info('\033[92mTEST 3 [PASSED] ==> HTTP Blocked\033[0m')
        update_json_results("Test 3: HTTP Blocked", "Passed")
    else:
        error = ('\033[91mTEST 3 [FAILED] ==> HTTP WORKS\033[0m')
        logger.error(error)
        capture_err_logs(controller_clients, compute_clients, error)
        update_json_results("Test 3: HTTP Blocked", "Failed")

    logger.info("Test SSH")
    if not is_ssh_blocked(srv_prv_ip, client_ip):
        logger.info('\033[92mTEST 4 [PASSED] ==> SSH Works\033[0m')
        update_json_results("Test 4: SSH Works", "Passed")
    else:
        error = ('\033[91mTEST 4 [FAILED] ==> SSH BLOCKED\033[0m')
        logger.error(error)
        capture_err_logs(controller_clients, compute_clients, error)
        update_json_results("Test 4: SSH Works", "Failed")

    if json_results["failures"]:
        status = "FAIL"
        logger.error('\033[91mSFC TESTS: %s :( FOUND %s FAIL \033[0m' % (
            status, json_results["failures"]))

    if args.report:
        stop_time = time.time()
        logger.debug("Promise Results json: " + str(json_results))
        ft_utils.push_results_to_db("sfc",
                                    "functest-odl-sfc",
                                    start_time,
                                    stop_time,
                                    status,
                                    json_results)

    if status == "PASS":
        logger.info('\033[92mSFC ALL TESTS: %s :)\033[0m' % status)
        sys.exit(0)

    sys.exit(1)

if __name__ == '__main__':
    main()
