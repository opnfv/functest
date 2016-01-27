#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# valentin.boucher@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import json
import os
import os.path
import re
import requests
import shutil
import socket
import subprocess
import sys
import urllib2
import yaml
from git import Repo


# ----------------------------------------------------------
#
#               OPENSTACK UTILS
#
# -----------------------------------------------------------


#*********************************************
#   CREDENTIALS
#*********************************************
def check_credentials():
    """
    Check if the OpenStack credentials (openrc) are sourced
    """
    env_vars = ['OS_AUTH_URL', 'OS_USERNAME', 'OS_PASSWORD', 'OS_TENANT_NAME']
    return all(map(lambda v: v in os.environ and os.environ[v], env_vars))

def get_credentials(service):
    """Returns a creds dictionary filled with the following keys:
    * username
    * password/api_key (depending on the service)
    * tenant_name/project_id (depending on the service)
    * auth_url
    :param service: a string indicating the name of the service
                    requesting the credentials.
    """
    creds = {}
    # Unfortunately, each of the OpenStack client will request slightly
    # different entries in their credentials dict.
    if service.lower() in ("nova", "cinder"):
        password = "api_key"
        tenant = "project_id"
    else:
        password = "password"
        tenant = "tenant_name"

    # The most common way to pass these info to the script is to do it through
    # environment variables.
    creds.update({
        "username": os.environ.get('OS_USERNAME', "admin"),
        password: os.environ.get("OS_PASSWORD", 'admin'),
        "auth_url": os.environ.get("OS_AUTH_URL",
                                   "http://192.168.20.71:5000/v2.0"),
        tenant: os.environ.get("OS_TENANT_NAME", "admin"),
    })
    return creds



#*********************************************
#   NOVA
#*********************************************
def get_instances(nova_client):
    try:
        instances = nova_client.servers.list(search_opts={'all_tenants': 1})
        return instances
    except Exception, e:
        print "Error [get_instances(nova_client)]:", e
        return None


def get_instance_status(nova_client, instance):
    try:
        instance = nova_client.servers.get(instance.id)
        return instance.status
    except Exception, e:
        print "Error [get_instance_status(nova_client, '%s')]:" % \
            str(instance), e
        return None


def get_instance_by_name(nova_client, instance_name):
    try:
        instance = nova_client.servers.find(name=instance_name)
        return instance
    except Exception, e:
        print "Error [get_instance_by_name(nova_client, '%s')]:" % \
            instance_name, e
        return None


def get_flavor_id(nova_client, flavor_name):
    flavors = nova_client.flavors.list(detailed=True)
    id = ''
    for f in flavors:
        if f.name == flavor_name:
            id = f.id
            break
    return id


def get_flavor_id_by_ram_range(nova_client, min_ram, max_ram):
    flavors = nova_client.flavors.list(detailed=True)
    id = ''
    for f in flavors:
        if min_ram <= f.ram and f.ram <= max_ram:
            id = f.id
            break
    return id


def get_floating_ips(nova_client):
    try:
        floating_ips = nova_client.floating_ips.list()
        return floating_ips
    except Exception, e:
        print "Error [get_floating_ips(nova_client)]:", e
        return None


def create_flavor(nova_client, flavor_name, ram, disk, vcpus):
    try:
        flavor = nova_client.flavors.create(flavor_name,ram,vcpus,disk)
    except Exception, e:
        print "Error [create_flavor(nova_client, '%s', '%s', '%s', "\
            "'%s')]:" %(flavor_name,ram, disk, vcpus), e
        return None
    return flavor.id


def create_floating_ip(neutron_client):
    extnet_id = get_external_net_id(neutron_client)
    props = {'floating_network_id': extnet_id}
    try:
        ip_json = neutron_client.create_floatingip({'floatingip': props})
        floating_ip = ip_json['floatingip']['floating_ip_address']
    except Exception, e:
        print "Error [create_floating_ip(neutron_client)]:", e
        return None
    return floating_ip


def add_floating_ip(nova_client, server_id, floatingip_id):
    try:
        nova_client.servers.add_floating_ip(server_id,floatingip_id)
        return True
    except Exception, e:
        print "Error [add_floating_ip(nova_client, '%s', '%s')]:" % \
            (server_id, floatingip_id), e
        return False


def delete_instance(nova_client, instance_id):
    try:
        nova_client.servers.force_delete(instance_id)
        return True
    except Exception, e:
        print "Error [delete_instance(nova_client, '%s')]:" % instance_id, e
        return False


def delete_floating_ip(nova_client, floatingip_id):
    try:
        nova_client.floating_ips.delete(floatingip_id)
        return True
    except Exception, e:
        print "Error [delete_floating_ip(nova_client, '%s')]:" % floatingip_id, e
        return False




#*********************************************
#   NEUTRON
#*********************************************
def get_network_list(neutron_client):
    network_list = neutron_client.list_networks()['networks']
    if len(network_list) == 0:
        return None
    else:
        return network_list


def get_router_list(neutron_client):
    router_list = neutron_client.list_routers()['routers']
    if len(router_list) == 0:
        return None
    else:
        return router_list


def get_port_list(neutron_client):
    port_list = neutron_client.list_ports()['ports']
    if len(port_list) == 0:
        return None
    else:
        return port_list


def get_network_id(neutron_client, network_name):
    networks = neutron_client.list_networks()['networks']
    id = ''
    for n in networks:
        if n['name'] == network_name:
            id = n['id']
            break
    return id


def get_private_net(neutron_client):
    # Checks if there is an existing shared private network
    networks = neutron_client.list_networks()['networks']
    if len(networks) == 0:
        return None
    for net in networks:
        if (net['router:external'] is False) and (net['shared'] is True):
            return net
    return None


def get_external_net(neutron_client):
    for network in neutron_client.list_networks()['networks']:
        if network['router:external']:
            return network['name']
    return False


def get_external_net_id(neutron_client):
    for network in neutron_client.list_networks()['networks']:
        if network['router:external']:
            return network['id']
    return False


def check_neutron_net(neutron_client, net_name):
    for network in neutron_client.list_networks()['networks']:
        if network['name'] == net_name:
            for subnet in network['subnets']:
                return True
    return False


def create_neutron_net(neutron_client, name):
    json_body = {'network': {'name': name,
                             'admin_state_up': True}}
    try:
        network = neutron_client.create_network(body=json_body)
        network_dict = network['network']
        return network_dict['id']
    except Exception, e:
        print "Error [create_neutron_net(neutron_client, '%s')]:" % name, e
        return False


def create_neutron_subnet(neutron_client, name, cidr, net_id):
    json_body = {'subnets': [{'name': name, 'cidr': cidr,
                              'ip_version': 4, 'network_id': net_id}]}
    try:
        subnet = neutron_client.create_subnet(body=json_body)
        return subnet['subnets'][0]['id']
    except Exception, e:
        print "Error [create_neutron_subnet(neutron_client, '%s', '%s', "\
            "'%s')]:" %(name,cidr, net_id), e
        return False


def create_neutron_router(neutron_client, name):
    json_body = {'router': {'name': name, 'admin_state_up': True}}
    try:
        router = neutron_client.create_router(json_body)
        return router['router']['id']
    except Exception, e:
        print "Error [create_neutron_router(neutron_client, name)]:" % name, e
        return False


def create_neutron_port(neutron_client, name, network_id, ip):
    json_body = {'port': {
                 'admin_state_up': True,
                 'name': name,
                 'network_id': network_id,
                 'fixed_ips': [{"ip_address": ip}]
                 }}
    try:
        port = neutron_client.create_port(body=json_body)
        return port['port']['id']
    except Exception, e:
        print "Error [create_neutron_port(neutron_client, '%s', '%s', "\
            "'%s')]:" %(name,network_id, ip), e
        return False


def update_neutron_net(neutron_client, network_id, shared=False):
    json_body = {'network': {'shared': shared}}
    try:
        neutron_client.update_network(network_id, body=json_body)
        return True
    except Exception, e:
        print "Error [update_neutron_net(neutron_client, '%s', '%s')]:" % \
            (network_id,str(shared)), e
        return False


def update_neutron_port(neutron_client, port_id, device_owner):
    json_body = {'port': {
                 'device_owner': device_owner,
                 }}
    try:
        port = neutron_client.update_port(port=port_id,
                                          body=json_body)
        return port['port']['id']
    except Exception, e:
        print "Error [update_neutron_port(neutron_client, '%s', '%s')]:" % \
            (port_id,device_owner), e
        return False


def add_interface_router(neutron_client, router_id, subnet_id):
    json_body = {"subnet_id": subnet_id}
    try:
        neutron_client.add_interface_router(router=router_id, body=json_body)
        return True
    except Exception, e:
        print "Error [add_interface_router(neutron_client, '%s', '%s')]:" % \
            (router_id,subnet_id), e
        return False

def add_gateway_router(neutron_client, router_id):
    ext_net_id = get_external_net_id(neutron_client)
    router_dict = {'network_id': ext_net_id}
    try:
        neutron_client.add_gateway_router(router_id,router_dict)
        return True
    except Exception, e:
        print "Error [add_gateway_router(neutron_client, '%s')]:" % router_id, e
        return False


def delete_neutron_net(neutron_client, network_id):
    try:
        neutron_client.delete_network(network_id)
        return True
    except Exception, e:
        print "Error [delete_neutron_net(neutron_client, '%s')]:" % network_id, e
        return False


def delete_neutron_subnet(neutron_client, subnet_id):
    try:
        neutron_client.delete_subnet(subnet_id)
        return True
    except Exception, e:
        print "Error [delete_neutron_subnet(neutron_client, '%s')]:" % subnet_id, e
        return False


def delete_neutron_router(neutron_client, router_id):
    json_body = {'router': {'id': router_id}}
    try:
        neutron_client.delete_router(router=router_id)
        return True
    except Exception, e:
        print "Error [delete_neutron_router(neutron_client, '%s')]:" % \
            router_id, e
        return False


def delete_neutron_port(neutron_client, port_id):
    try:
        neutron_client.delete_port(port_id)
        return True
    except Exception, e:
        print "Error [delete_neutron_port(neutron_client, '%s')]:" % port_id, e
        return False


def remove_interface_router(neutron_client, router_id, subnet_id):
    json_body = {"subnet_id": subnet_id}
    try:
        neutron_client.remove_interface_router(router=router_id,
                                               body=json_body)
        return True
    except Exception, e:
        print "Error [remove_interface_router(neutron_client, '%s', '%s')]:" % \
            (router_id,subnet_id), e
        return False


def remove_gateway_router(neutron_client, router_id):
    try:
        neutron_client.remove_gateway_router(router_id)
        return True
    except Exception, e:
        print "Error [remove_gateway_router(neutron_client, '%s')]:" % router_id, e
        return False



#*********************************************
#   SEC GROUPS
#*********************************************
def get_security_groups(neutron_client):
    try:
        security_groups = neutron_client.list_security_groups()[
            'security_groups']
        return security_groups
    except Exception, e:
        print "Error [get_security_groups(neutron_client)]:", e
        return None


def update_sg_quota(neutron_client, tenant_id, sg_quota, sg_rule_quota):
    json_body = {"quota": {
        "security_group": sg_quota,
        "security_group_rule": sg_rule_quota
    }}

    try:
        quota = neutron_client.update_quota(tenant_id=tenant_id,
                                            body=json_body)
        return True
    except Exception, e:
        print "Error [update_sg_quota(neutron_client, '%s', '%s', "\
            "'%s')]:" %(tenant_id,sg_quota, sg_rule_quota), e
        return False


def delete_security_group(neutron_client, secgroup_id):
    try:
        neutron_client.delete_security_group(secgroup_id)
        return True
    except Exception, e:
        print "Error [delete_security_group(neutron_client, '%s')]:" % secgroup_id, e
        return False



#*********************************************
#   GLANCE
#*********************************************
def get_images(nova_client):
    try:
        images = nova_client.images.list()
        return images
    except Exception, e:
        print "Error [get_images]:", e
        return None


def get_image_id(glance_client, image_name):
    images = glance_client.images.list()
    id = ''
    for i in images:
        if i.name == image_name:
            id = i.id
            break
    return id


def create_glance_image(glance_client, image_name, file_path, public=True):
    if not os.path.isfile(file_path):
        print "Error: file " + file_path + " does not exist."
        return False
    try:
        with open(file_path) as fimage:
            image = glance_client.images.create(name=image_name,
                                                is_public=public,
                                                disk_format="qcow2",
                                                container_format="bare",
                                                data=fimage)
        return image.id
    except Exception, e:
        print "Error [create_glance_image(glance_client, '%s', '%s', "\
            "'%s')]:" %(image_name,file_path, str(public)), e
        return False


def delete_glance_image(nova_client, image_id):
    try:
        nova_client.images.delete(image_id)
        return True
    except Exception, e:
        print "Error [delete_glance_image(nova_client, image_id)]:" % image_id, e
        return False



#*********************************************
#   CINDER
#*********************************************
def get_volumes(cinder_client):
    try:
        volumes = cinder_client.volumes.list(search_opts={'all_tenants': 1})
        return volumes
    except Exception, e:
        print "Error [get_volumes(cinder_client)]:", e
        return None


def update_cinder_quota(cinder_client, tenant_id, vols_quota,
                        snapshots_quota, gigabytes_quota):
    quotas_values = {"volumes": vols_quota,
                     "snapshots": snapshots_quota,
                     "gigabytes": gigabytes_quota}

    try:
        quotas_default = cinder_client.quotas.update(tenant_id,
                                                      **quotas_values)
        return True
    except Exception, e:
        print "Error [update_cinder_quota(cinder_client, '%s', '%s', '%s'" \
            "'%s')]:" %(tenant_id, vols_quota, snapshots_quota, gigabytes_quota), e
        return False


def delete_volume(cinder_client, volume_id, forced=False):
    try:
        if forced:
            try:
                cinder_client.volumes.detach(volume_id)
            except:
                print "Error:", sys.exc_info()[0]
            cinder_client.volumes.force_delete(volume_id)
        else:
            cinder_client.volumes.delete(volume_id)
        return True
    except Exception, e:
        print "Error [delete_volume(cinder_client, '%s', '%s')]:" % \
            (volume_id, str(forced)), e
        return False



#*********************************************
#   KEYSTONE
#*********************************************
def get_tenants(keystone_client):
    try:
        tenants = keystone_client.tenants.list()
        return tenants
    except Exception, e:
        print "Error [get_tenants(keystone_client)]:", e
        return None


def get_users(keystone_client):
    try:
        users = keystone_client.users.list()
        return users
    except Exception, e:
        print "Error [get_users(keystone_client)]:", e
        return None


def get_tenant_id(keystone_client, tenant_name):
    tenants = keystone_client.tenants.list()
    id = ''
    for t in tenants:
        if t.name == tenant_name:
            id = t.id
            break
    return id


def get_user_id(keystone_client, user_name):
    users = keystone_client.users.list()
    id = ''
    for u in users:
        if u.name == user_name:
            id = u.id
            break
    return id


def get_role_id(keystone_client, role_name):
    roles = keystone_client.roles.list()
    id = ''
    for r in roles:
        if r.name == role_name:
            id = r.id
            break
    return id


def create_tenant(keystone_client, tenant_name, tenant_description):
    try:
        tenant = keystone_client.tenants.create(tenant_name,
                                                tenant_description,
                                                enabled=True)
        return tenant.id
    except Exception, e:
        print "Error [create_tenant(cinder_client, '%s', '%s')]:" % \
            (tenant_name, tenant_description), e
        return False


def create_user(keystone_client, user_name, user_password,
                user_email, tenant_id):
    try:
        user = keystone_client.users.create(user_name, user_password,
                                            user_email, tenant_id,
                                            enabled=True)
        return user.id
    except Exception, e:
        print "Error [create_user(keystone_client, '%s', '%s', '%s'" \
            "'%s')]:" %(user_name, user_password, user_email, tenant_id), e
        return False


def add_role_user(keystone_client, user_id, role_id, tenant_id):
    try:
        keystone_client.roles.add_user_role(user_id, role_id, tenant_id)
        return True
    except Exception, e:
        print "Error [add_role_user(keystone_client, '%s', '%s'" \
            "'%s')]:" %(user_id, role_id, tenant_id), e
        return False


def delete_tenant(keystone_client, tenant_id):
    try:
        tenant = keystone_client.tenants.delete(tenant_id)
        return True
    except Exception, e:
        print "Error [delete_tenant(keystone_client, '%s')]:" % tenant_id, e
        return False


def delete_user(keystone_client, user_id):
    try:
        tenant = keystone_client.users.delete(user_id)
        return True
    except Exception, e:
        print "Error [delete_user(keystone_client, '%s')]:" % user_id, e
        return False







# ----------------------------------------------------------
#
#               INTERNET UTILS
#
# -----------------------------------------------------------
def check_internet_connectivity(url='http://www.opnfv.org/'):
    """
    Check if there is access to the internet
    """
    try:
        urllib2.urlopen(url, timeout=5)
        return True
    except urllib2.URLError:
        return False


def download_url(url, dest_path):
    """
    Download a file to a destination path given a URL
    """
    name = url.rsplit('/')[-1]
    dest = dest_path + "/" + name
    try:
        response = urllib2.urlopen(url)
    except (urllib2.HTTPError, urllib2.URLError):
        return False

    with open(dest, 'wb') as f:
        shutil.copyfileobj(response, f)
    return True




# ----------------------------------------------------------
#
#               CI UTILS
#
# -----------------------------------------------------------
def get_git_branch(repo_path):
    """
    Get git branch name
    """
    repo = Repo(repo_path)
    branch = repo.active_branch
    return branch.name


def get_installer_type(logger=None):
    """
    Get installer type (fuel, apex, joid, compass)
    """
    try:
        installer = os.environ['INSTALLER_TYPE']
    except KeyError:
        if logger:
            logger.error("Impossible to retrieve the installer type")
        installer = "Unknown_installer"

    return installer


def get_scenario(logger=None):
    """
    Get scenario
    """
    try:
        scenario = os.environ['DEPLOY_SCENARIO']
    except KeyError:
        if logger:
            logger.error("Impossible to retrieve the scenario")
        scenario = "Unknown_scenario"

    return scenario


def get_pod_name(logger=None):
    """
    Get PoD Name from env variable NODE_NAME
    """
    try:
        return os.environ['NODE_NAME']
    except KeyError:
        if logger:
            logger.error(
                "Unable to retrieve the POD name from environment.Using pod name 'unknown-pod'")
        return "unknown-pod"


def push_results_to_db(db_url, case_name, logger, pod_name,
                       version, payload):
    """
    POST results to the Result target DB
    """
    url = db_url + "/results"
    installer = get_installer_type(logger)
    params = {"project_name": "functest", "case_name": case_name,
              "pod_name": pod_name, "installer": installer,
              "version": version, "details": payload}

    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(url, data=json.dumps(params), headers=headers)
        if logger:
            logger.debug(r)
        return True
    except Exception, e:
        print "Error []:", e
        return False


def get_resolvconf_ns():
    """
    Get nameservers from current resolv.conf
    """
    nameservers = []
    rconf = open("/etc/resolv.conf", "r")
    line = rconf.readline()
    while line:
        ip = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ip:
            result = sock.connect_ex((ip.group(),53))
            if result == 0:
                nameservers.append(ip.group())
        line = rconf.readline()
    return nameservers


def getTestEnv(test, functest_yaml):
    """
    Get the config of the testcase based on functest_config.yaml
      2 options
        - test = test project e.g; ovno
        - test = testcase e.g. functest/odl
       look for the / to see if it is a test project or a testcase
    """
    try:
        TEST_ENV = functest_yaml.get("test-dependencies")

        if test.find("/") < 0:
            config_test = TEST_ENV[test]
        else:
            test_split = test.split("/")
            testproject = test_split[0]
            testcase = test_split[1]
            config_test = TEST_ENV[testproject][testcase]
    except KeyError:
        # if not defined in dependencies => no dependencies
        config_test = ""
    except Exception, e:
        print "Error []:", e

    return config_test


def get_ci_envvars():
    """
    Get the CI env variables
    """
    ci_env_var = {
        "installer": os.environ.get('INSTALLER_TYPE'),
        "scenario": os.environ.get('DEPLOY_SCENARIO')}
    return ci_env_var


def isTestRunnable(test, functest_yaml):
    """
    Return True if the test is runnable in the current scenario
    """
    # By default we assume that all the tests are always runnable...
    is_runnable = True
    # Retrieve CI environment
    ci_env = get_ci_envvars()
    # Retrieve test environement from config file
    test_env = getTestEnv(test, functest_yaml)

    # if test_env not empty => dependencies to be checked
    if test_env is not None and len(test_env) > 0:
        # possible criteria = ["installer", "scenario"]
        # consider test criteria from config file
        # compare towards CI env through CI en variable
        for criteria in test_env:
            if re.search(test_env[criteria], ci_env[criteria]) is None:
                # print "Test "+ test + " cannot be run on the environment"
                is_runnable = False
    return is_runnable


def generateTestcaseList(functest_yaml):
    """
    Generate a test file with the runnable test according to
    the current scenario
    """
    test_list = ""
    # get testcases
    testcase_list = functest_yaml.get("test-dependencies")
    projects = testcase_list.keys()

    for project in projects:
        testcases = testcase_list[project]
        # 1 or 2 levels for testcases project[/case]l
        # if only project name without controller or scenario
        # => shall be runnable on any controller/scenario
        if testcases is None:
            test_list += project + " "
        else:
            for testcase in testcases:
                if testcase == "installer" or testcase == "scenario":
                    # project (1 level)
                    if isTestRunnable(project, functest_yaml):
                        test_list += project + " "
                else:
                    # project/testcase (2 levels)
                    thetest = project + "/" + testcase
                    if isTestRunnable(thetest, functest_yaml):
                        test_list += testcase + " "

    # sort the list to execute the test in the right order
    test_order_list = functest_yaml.get("test_exec_priority")
    test_sorted_list = ""
    for test in test_order_list:
        if test_order_list[test] in test_list:
            test_sorted_list += test_order_list[test] + " "

    # create a file that could be consumed by run-test.sh
    # this method is used only for CI
    # so it can be run only in container
    # reuse default conf directory to store the list of runnable tests
    file = open("/home/opnfv/functest/conf/testcase-list.txt", 'w')
    file.write(test_sorted_list)
    file.close()

    return test_sorted_list


def execute_command(cmd, logger=None, exit_on_error=True):
    """
    Execute Linux command
        prints stdout to a file and depending on if there
        is a logger defined, it will print it or not.
    """
    if logger:
        logger.debug('Executing command : {}'.format(cmd))
    output_file = "output.txt"
    f = open(output_file, 'w+')
    p = subprocess.call(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT)
    f.close()
    f = open(output_file, 'r')
    result = f.read()
    if result != "" and logger:
        logger.debug(result)
    if p == 0:
        return True
    else:
        if logger:
            logger.error("Error when executing command %s" % cmd)
        if exit_on_error:
            exit(-1)
        return False
