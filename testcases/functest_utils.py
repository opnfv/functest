#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# valentin.boucher@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#


import os
import urllib2
import subprocess
import sys
import requests
import json
from git import Repo


# ############ CREDENTIALS OPENSTACK #############
def check_credentials():
    """
    Check if the OpenStack credentials (openrc) are sourced
    """
    # TODO: there must be a short way to do this
    # doing if os.environ["something"] == "" throws an error
    try:
        os.environ['OS_AUTH_URL']
    except KeyError:
        return False
    try:
        os.environ['OS_USERNAME']
    except KeyError:
        return False
    try:
        os.environ['OS_PASSWORD']
    except KeyError:
        return False
    try:
        os.environ['OS_TENANT_NAME']
    except KeyError:
        return False
    return True


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


# ################ NOVA #################
def get_instances(nova_client):
    try:
        instances = nova_client.servers.list()
        return instances
    except:
        return None

def get_instance_status(nova_client, instance):
    try:
        instance = nova_client.servers.get(instance.id)
        return instance.status
    except:
        return None

def get_instance_by_name(nova_client, instance_name):
    try:
        instance = nova_client.servers.find(name=instance_name)
        return instance
    except:
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


# ################ NEUTRON #################
def create_neutron_net(neutron_client, name):
    json_body = {'network': {'name': name,
                             'admin_state_up': True}}
    try:
        network = neutron_client.create_network(body=json_body)
        network_dict = network['network']
        return network_dict['id']
    except:
        print "Error:", sys.exc_info()[0]
        return False


def delete_neutron_net(neutron_client, network_id):
    try:
        neutron_client.delete_network(network_id)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False


def create_neutron_subnet(neutron_client, name, cidr, net_id):
    json_body = {'subnets': [{'name': name, 'cidr': cidr,
                             'ip_version': 4, 'network_id': net_id}]}
    try:
        subnet = neutron_client.create_subnet(body=json_body)
        return subnet['subnets'][0]['id']
    except:
        print "Error:", sys.exc_info()[0]
        return False


def delete_neutron_subnet(neutron_client, subnet_id):
    try:
        neutron_client.delete_subnet(subnet_id)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False


def create_neutron_router(neutron_client, name):
    json_body = {'router': {'name': name, 'admin_state_up': True}}
    try:
        router = neutron_client.create_router(json_body)
        return router['router']['id']
    except:
        print "Error:", sys.exc_info()[0]
        return False


def delete_neutron_router(neutron_client, router_id):
    json_body = {'router': {'id': router_id}}
    try:
        neutron_client.delete_router(router=router_id)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False


def add_interface_router(neutron_client, router_id, subnet_id):
    json_body = {"subnet_id": subnet_id}
    try:
        neutron_client.add_interface_router(router=router_id, body=json_body)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False


def remove_interface_router(neutron_client, router_id, subnet_id):
    json_body = {"subnet_id": subnet_id}
    try:
        neutron_client.remove_interface_router(router=router_id,
                                               body=json_body)
        return True
    except:
        print "Error:", sys.exc_info()[0]
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
    except:
        print "Error:", sys.exc_info()[0]
        return False

def delete_neutron_port(neutron_client, port_id):
    try:
        neutron_client.delete_port(port_id)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False

def get_network_id(neutron_client, network_name):
    networks = neutron_client.list_networks()['networks']
    id = ''
    for n in networks:
        if n['name'] == network_name:
            id = n['id']
            break
    return id


def check_neutron_net(neutron_client, net_name):
    for network in neutron_client.list_networks()['networks']:
        if network['name'] == net_name:
            for subnet in network['subnets']:
                return True
    return False


def get_network_list(neutron_client):
    network_list = neutron_client.list_networks()['networks']
    if len(network_list) == 0:
        return None
    else:
        return network_list


def get_external_net(neutron_client):
    for network in neutron_client.list_networks()['networks']:
        if network['router:external']:
            return network['name']
    return False


def update_sg_quota(neutron_client, tenant_id, sg_quota, sg_rule_quota):
    json_body = {"quota": {
        "security_group": sg_quota,
        "security_group_rule": sg_rule_quota
    }}

    try:
        quota = neutron_client.update_quota(tenant_id=tenant_id,
                                            body=json_body)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False

# ################ GLANCE #################
def get_images(glance_client):
    try:
        images = nova_client.images.list()
        return images
    except:
        return None


def get_image_id(glance_client, image_name):
    images = glance_client.images.list()
    id = ''
    for i in images:
        if i.name == image_name:
            id = i.id
            break
    return id


def create_glance_image(glance_client, image_name, file_path, is_public=True):
    try:
        with open(file_path) as fimage:
            image = glance_client.images.create(name=image_name,
                                                is_public=is_public,
                                                disk_format="qcow2",
                                                container_format="bare",
                                                data=fimage)
        return image.id
    except:
        return False


# ################ KEYSTONE #################
def get_tenants(keystone_client):
    try:
        tenants = keystone_client.tenants.list()
        return tenants
    except:
        return None


def get_tenant_id(keystone_client, tenant_name):
    tenants = keystone_client.tenants.list()
    id = ''
    for t in tenants:
        if t.name == tenant_name:
            id = t.id
            break
    return id

def get_users(keystone_client):
    try:
        users = keystone_client.users.list()
        return users
    except:
        return None

def get_role_id(keystone_client, role_name):
    roles = keystone_client.roles.list()
    id = ''
    for r in roles:
        if r.name == role_name:
            id = r.id
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


def create_tenant(keystone_client, tenant_name, tenant_description):
    try:
        tenant = keystone_client.tenants.create(tenant_name,
                                                tenant_description,
                                                enabled=True)
        return tenant.id
    except:
        print "Error:", sys.exc_info()[0]
        return False


def delete_tenant(keystone_client, tenant_id):
    try:
        tenant = keystone_client.tenants.delete(tenant_id)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False


def create_user(keystone_client, user_name, user_password,
                user_email, tenant_id):
    try:
        user = keystone_client.users.create(user_name, user_password,
                                            user_email, tenant_id,
                                            enabled=True)
        return user.id
    except:
        print "Error:", sys.exc_info()[0]
        return False


def delete_user(keystone_client, user_id):
    try:
        tenant = keystone_client.users.delete(user_id)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False


def add_role_user(keystone_client, user_id, role_id, tenant_id):
    try:
        keystone_client.roles.add_user_role(user_id, role_id, tenant_id)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False


# ################ UTILS #################
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
        f.write(response.read())
    return True


def execute_command(cmd, logger=None):
    """
    Execute Linux command
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
        exit(-1)


def get_git_branch(repo_path):
    """
    Get git branch name
    """
    repo = Repo(repo_path)
    branch = repo.active_branch
    return branch.name


def get_installer_type(logger=None):
    """
    Get installer type (fuel, foreman, apex, joid, compass)
    """
    try:
        installer = os.environ['INSTALLER_TYPE']
    except KeyError:
        if logger:
            logger.error("Impossible to retrieve the installer type")
        installer = "Unkown"

    return installer

def push_results_to_db(db_url, case_name, logger, pod_name, git_version, payload):
    url = db_url + "/results"
    installer = get_installer_type(logger)
    params = {"project_name": "functest", "case_name": case_name,
              "pod_name": pod_name, "installer": installer,
              "version": git_version, "details": payload}

    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(url, data=json.dumps(params), headers=headers)
        logger.debug(r)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False
