#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import os

import utils
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("keystone").getLogger()

DEFAULT_API_VERSION = '2'
API_NAME = 'identity'
API_VERSIONS = {
    '2': 'keystoneclient.v2_0.client',
    '3': 'keystoneclient.v3.client'
}


def get_client_version():
    api_version = os.getenv('OS_IDENTITY_API_VERSION')
    if api_version is not None:
        logger.info("OS_IDENTITY_API_VERSION is set in env as '%s'",
                    api_version)
        return api_version
    return DEFAULT_API_VERSION


def get_keystone_client():
    creds_keystone = utils.get_credentials('keystone')
    keystone_client_cls = utils.get_client_class(
        API_NAME,
        get_client_version(),
        API_VERSIONS)
    logger.debug('Instantiating identity client: %s', keystone_client_cls)
    return keystone_client_cls.Client(**creds_keystone)


def get_tenants(keystone_client):
    try:
        tenants = keystone_client.tenants.list()
        return tenants
    except Exception, e:
        logger.error("Error [get_tenants(keystone_client)]: %s" % e)
        return None


def get_users(keystone_client):
    try:
        users = keystone_client.users.list()
        return users
    except Exception, e:
        logger.error("Error [get_users(keystone_client)]: %s" % e)
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
        logger.error("Error [create_tenant(keystone_client, '%s', '%s')]: %s"
                     % (tenant_name, tenant_description, e))
        return None


def create_user(keystone_client, user_name, user_password,
                user_email, tenant_id):
    try:
        user = keystone_client.users.create(user_name, user_password,
                                            user_email, tenant_id,
                                            enabled=True)
        return user.id
    except Exception, e:
        logger.error("Error [create_user(keystone_client, '%s', '%s', '%s'"
                     "'%s')]: %s" % (user_name, user_password,
                                     user_email, tenant_id, e))
        return None


def add_role_user(keystone_client, user_id, role_id, tenant_id):
    try:
        keystone_client.roles.add_user_role(user_id, role_id, tenant_id)
        return True
    except Exception, e:
        logger.error("Error [add_role_user(keystone_client, '%s', '%s'"
                     "'%s')]: %s " % (user_id, role_id, tenant_id, e))
        return False


def delete_tenant(keystone_client, tenant_id):
    try:
        keystone_client.tenants.delete(tenant_id)
        return True
    except Exception, e:
        logger.error("Error [delete_tenant(keystone_client, '%s')]: %s"
                     % (tenant_id, e))
        return False


def delete_user(keystone_client, user_id):
    try:
        keystone_client.users.delete(user_id)
        return True
    except Exception, e:
        logger.error("Error [delete_user(keystone_client, '%s')]: %s"
                     % (user_id, e))
        return False
