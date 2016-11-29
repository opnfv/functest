#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import os
import sys

import cinderclient.client as cinder_client

import utils
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("cinder").getLogger()

DEFAULT_API_VERSION = '2'
API_NAME = 'volume'


def get_client_version():
    api_version = os.getenv('OS_VOLUME_API_VERSION')
    if api_version is not None:
        logger.info("OS_VOLUME_API_VERSION is set in env as '%s'",
                    api_version)
        return api_version
    return DEFAULT_API_VERSION


def get_cinder_client():
    creds_cinder = utils.get_credentials("cinder")
    creds_cinder.update({
        "service_type": "volume"
    })
    return cinder_client.Client(get_client_version(), **creds_cinder)


def get_volumes(cinder_client):
    try:
        volumes = cinder_client.volumes.list(search_opts={'all_tenants': 1})
        return volumes
    except Exception, e:
        logger.error("Error [get_volumes(cinder_client)]: %s" % e)
        return None


def list_volume_types(cinder_client, public=True, private=True):
    try:
        volume_types = cinder_client.volume_types.list()
        if not public:
            volume_types = [vt for vt in volume_types if not vt.is_public]
        if not private:
            volume_types = [vt for vt in volume_types if vt.is_public]
        return volume_types
    except Exception, e:
        logger.error("Error [list_volume_types(cinder_client)]: %s" % e)
        return None


def create_volume_type(cinder_client, name):
    try:
        volume_type = cinder_client.volume_types.create(name)
        return volume_type
    except Exception, e:
        logger.error("Error [create_volume_type(cinder_client, '%s')]: %s"
                     % (name, e))
        return None


def update_cinder_quota(cinder_client, tenant_id, vols_quota,
                        snapshots_quota, gigabytes_quota):
    quotas_values = {"volumes": vols_quota,
                     "snapshots": snapshots_quota,
                     "gigabytes": gigabytes_quota}

    try:
        cinder_client.quotas.update(tenant_id, **quotas_values)
        return True
    except Exception, e:
        logger.error("Error [update_cinder_quota(cinder_client, '%s', '%s', "
                     "'%s' '%s')]: %s" % (tenant_id, vols_quota,
                                          snapshots_quota, gigabytes_quota, e))
        return False


def delete_volume(cinder_client, volume_id, forced=False):
    try:
        if forced:
            try:
                cinder_client.volumes.detach(volume_id)
            except:
                logger.error(sys.exc_info()[0])
            cinder_client.volumes.force_delete(volume_id)
        else:
            cinder_client.volumes.delete(volume_id)
        return True
    except Exception, e:
        logger.error("Error [delete_volume(cinder_client, '%s', '%s')]: %s"
                     % (volume_id, str(forced), e))
        return False


def delete_volume_type(cinder_client, volume_type):
    try:
        cinder_client.volume_types.delete(volume_type)
        return True
    except Exception, e:
        logger.error("Error [delete_volume_type(cinder_client, '%s')]: %s"
                     % (volume_type, e))
        return False
