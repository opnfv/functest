import os
import pprint
import sys
import time

import functest.utils.openstack_utils as os_utils
import yaml

REPO_PATH = os.environ['repos_dir'] + '/functest/'

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)
f.close()

NAME_VM_1 = functest_yaml.get("vping").get("vm_name_1")
NAME_VM_2 = functest_yaml.get("vping").get("vm_name_2")

VM_BOOT_TIMEOUT = 180
VM_DELETE_TIMEOUT = 100
PING_TIMEOUT = functest_yaml.get("vping").get("ping_timeout")

GLANCE_IMAGE_NAME = functest_yaml.get("vping").get("image_name")
GLANCE_IMAGE_FILENAME = functest_yaml.get("general").get(
    "openstack").get("image_file_name")
GLANCE_IMAGE_FORMAT = functest_yaml.get("general").get(
    "openstack").get("image_disk_format")
GLANCE_IMAGE_PATH = functest_yaml.get("general").get("directories").get(
    "dir_functest_data") + "/" + GLANCE_IMAGE_FILENAME

FLAVOR = functest_yaml.get("vping").get("vm_flavor")

# NEUTRON Private Network parameters
PRIVATE_NET_NAME = functest_yaml.get("vping").get(
    "vping_private_net_name")
PRIVATE_SUBNET_NAME = functest_yaml.get("vping").get(
    "vping_private_subnet_name")
PRIVATE_SUBNET_CIDR = functest_yaml.get("vping").get(
    "vping_private_subnet_cidr")
ROUTER_NAME = functest_yaml.get("vping").get(
    "vping_router_name")

SECGROUP_NAME = functest_yaml.get("vping").get("vping_sg_name")
SECGROUP_DESCR = functest_yaml.get("vping").get("vping_sg_descr")

pp = pprint.PrettyPrinter(indent=4)


def pMsg(value):
    """pretty printing"""
    pp.pprint(value)


def check_repo_exist(logger):
    if not os.path.exists(REPO_PATH):
        logger.error("Functest repository directory not found '%s'" % REPO_PATH)
        exit(-1)


def get_vmname_1():
    return NAME_VM_1


def get_vmname_2():
    return NAME_VM_2


def waitVmActive(nova, vm, logger):

    # sleep and wait for VM status change
    sleep_time = 3
    count = VM_BOOT_TIMEOUT / sleep_time
    while True:
        status = os_utils.get_instance_status(nova, vm)
        logger.debug("Status: %s" % status)
        if status == "ACTIVE":
            return True
        if status == "ERROR" or status == "error":
            return False
        if count == 0:
            logger.debug("Booting a VM timed out...")
            return False
        count -= 1
        time.sleep(sleep_time)
    return False


def create_security_group(logger):
    neutron_client = os_utils.get_neutron_client()

    sg_id = os_utils.get_security_group_id(neutron_client,
                                           SECGROUP_NAME)
    if sg_id != '':
        logger.info("Using existing security group '%s'..." % SECGROUP_NAME)
    else:
        logger.info("Creating security group  '%s'..." % SECGROUP_NAME)
        SECGROUP = os_utils.create_security_group(neutron_client,
                                                  SECGROUP_NAME,
                                                  SECGROUP_DESCR)
        if not SECGROUP:
            logger.error("Failed to create the security group...")
            return False

        sg_id = SECGROUP['id']

        logger.debug("Security group '%s' with ID=%s created successfully."
                     % (SECGROUP['name'], sg_id))

        logger.debug("Adding ICMP rules in security group '%s'..."
                     % SECGROUP_NAME)
        if not os_utils.create_secgroup_rule(neutron_client, sg_id,
                                             'ingress', 'icmp'):
            logger.error("Failed to create the security group rule...")
            return False

        logger.debug("Adding SSH rules in security group '%s'..."
                     % SECGROUP_NAME)
        if not os_utils.create_secgroup_rule(neutron_client, sg_id,
                                             'ingress', 'tcp',
                                             '22', '22'):
            logger.error("Failed to create the security group rule...")
            return False

        if not os_utils.create_secgroup_rule(
                neutron_client, sg_id, 'egress', 'tcp', '22', '22'):
            logger.error("Failed to create the security group rule...")
            return False
    return sg_id


def create_image(logger):
    EXIT_CODE = -1
    glance_client = os_utils.get_glance_client()

    # Check if the given image exists
    image_id = os_utils.get_image_id(glance_client, GLANCE_IMAGE_NAME)
    if image_id != '':
        logger.info("Using existing image '%s'..." % GLANCE_IMAGE_NAME)
        image_exists = True
    else:
        logger.info("Creating image '%s' from '%s'..." % (GLANCE_IMAGE_NAME,
                                                          GLANCE_IMAGE_PATH))
        image_id = os_utils.create_glance_image(glance_client,
                                                GLANCE_IMAGE_NAME,
                                                GLANCE_IMAGE_PATH,
                                                GLANCE_IMAGE_FORMAT)
        if not image_id:
            logger.error("Failed to create a Glance image...")
            exit(EXIT_CODE)
        logger.debug("Image '%s' with ID=%s created successfully."
                     % (GLANCE_IMAGE_NAME, image_id))
    return image_exists, image_id


def get_flavor(logger):
    nova_client = os_utils.get_nova_client()
    EXIT_CODE = -1

    # Check if the given flavor exists
    try:
        flavor = nova_client.flavors.find(name=FLAVOR)
        logger.info("Using existing Flavor '%s'..." % FLAVOR)
        return flavor
    except:
        logger.error("Flavor '%s' not found." % FLAVOR)
        logger.info("Available flavors are: ")
        pMsg(nova_client.flavor.list())
        exit(EXIT_CODE)


def create_network_full(logger):
    neutron_client = os_utils.get_neutron_client()
    EXIT_CODE = -1

    network_dic = os_utils.create_network_full(neutron_client,
                                               PRIVATE_NET_NAME,
                                               PRIVATE_SUBNET_NAME,
                                               ROUTER_NAME,
                                               PRIVATE_SUBNET_CIDR)


    if not network_dic:
        logger.error(
            "There has been a problem when creating the neutron network")
        exit(EXIT_CODE)
    network_id = network_dic["net_id"]
    return network_id


def delete_exist_vms(logger):
    nova_client = os_utils.get_nova_client()

    # Deleting instances if they exist
    servers = nova_client.servers.list()
    for server in servers:
        if server.name == NAME_VM_1 or server.name == NAME_VM_2:
            logger.info("Instance %s found. Deleting..." % server.name)
            server.delete()


def is_userdata(case):
    return case == 'vping_userdata'


def boot_vm(case, vmname, image_id, flavor, network_id, test_ip, logger):
    nova_client = os_utils.get_nova_client()
    EXIT_CODE = -1

    config = dict()
    config['name'] = vmname
    config['flavor'] = flavor
    config['image'] = image_id
    config['nics'] = [{"net-id": network_id}]
    if is_userdata(case):
        config['config_drive'] = True
        if vmname == NAME_VM_2:
            u = ("#!/bin/sh\n\nwhile true; do\n ping -c 1 %s 2>&1 >/dev/null\n "
                 "RES=$?\n if [ \"Z$RES\" = \"Z0\" ] ; then\n  echo 'vPing OK'\n "
                 "break\n else\n  echo 'vPing KO'\n fi\n sleep 1\ndone\n" % test_ip)
            config['userdata'] = u

    logger.info("Creating instance '%s'..." % vmname)
    logger.debug("Configuration: %s" % config)
    vm = nova_client.servers.create(**config)

    # wait until VM status is active
    if not waitVmActive(nova_client, vm, logger):

        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (
            vmname, os_utils.get_instance_status(nova_client, vm)))
        exit(EXIT_CODE)
    else:
        logger.info("Instance '%s' is ACTIVE." % vmname)

    return vm


def get_test_ip(vm, logger):
    test_ip = vm.networks.get(PRIVATE_NET_NAME)[0]
    logger.debug("Instance '%s' got %s" % (vm.name, test_ip))
    return test_ip


def do_vping_userdata(vm, test_ip, logger):
    logger.info("Waiting for ping...")
    EXIT_CODE = -1
    sec = 0
    metadata_tries = 0

    while True:
        time.sleep(1)
        console_log = vm.get_console_output()
        # print "--"+console_log
        # report if the test is failed
        if "vPing OK" in console_log:
            logger.info("vPing detected!")
            EXIT_CODE = 0
            break
        elif ("failed to read iid from metadata" in console_log or
              metadata_tries > 5):
            EXIT_CODE = -2
            break
        elif sec == PING_TIMEOUT:
            logger.info("Timeout reached.")
            break
        elif sec % 10 == 0:
            if "request failed" in console_log:
                logger.debug("It seems userdata is not supported in "
                             "nova boot. Waiting a bit...")
                metadata_tries += 1
            else:
                logger.debug("Pinging %s. Waiting for response..." % test_ip)
        sec += 1

    return EXIT_CODE, time.time()


def do_vping(case, vm, test_ip, logger):
    if is_userdata(case):
        return do_vping_userdata(vm, test_ip, logger)
    else:
        logger.info('ssh to be added')
        exit(-1)
        #TODO ssh


def check_result(code, start_time, stop_time, logger):
    test_status = "FAIL"
    if code == 0:
        logger.info("vPing OK")
        duration = round(stop_time - start_time, 1)
        logger.info("vPing duration:'%s'" % duration)
        test_status = "PASS"
    elif code == -2:
        duration = 0
        logger.info("Userdata is not supported in nova boot. Aborting test...")
    else:
        duration = 0
        logger.error("vPing FAILED")

    details = {'timestart': start_time,
               'duration': duration,
               'status': test_status}

    return test_status, details


def push_result(report, case, logger, start_time, stop_time, status, details):
    if report:
        try:
            logger.debug("Pushing vPing %s results into DB..." % case)
            os_utils.push_results_to_db("functest",
                                        case,
                                        logger,
                                        start_time,
                                        stop_time,
                                        status,
                                        details=details)
        except:
            logger.error("Error pushing results into Database '%s'"
                         % sys.exc_info()[0])
