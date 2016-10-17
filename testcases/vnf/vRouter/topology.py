#!/usr/bin/python
# coding: utf8
#######################################################################
#
# Copyright (c) 2016 Okinawa Open Laboratory
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
########################################################################


class topology:

    def __init__(self, inputs={}, orchestrator=None, logger=None):
        self.config = inputs
        self.orchestrator = orchestrator
        self.logger = logger
        self.deploy = False

    def set_orchestrator(self, orchestrator):
        self.orchestrator = orchestrator

    def set_target_vnf_image_id(self, image_id):
        self.config['target_vnf_image_id'] = image_id

    def set_reference_vnf_image_id(self, image_id):
        self.config['reference_vnf_image_id'] = image_id

    def set_target_vnf_flavor_id(self, flavor_id):
        self.config['target_vnf_flavor_id'] = flavor_id

    def set_reference_vnf_flavor_id(self, flavor_id):
        self.config['reference_vnf_flavor_id'] = flavor_id

    def set_region(self, region_name):
        self.config['region'] = region_name

    def set_agent_user(self, agent_user):
        self.config['agent_user'] = agent_user

    def set_external_network_name(self, external_network_name):
        self.config['external_network_name'] = external_network_name

    def set_public_domain(self, public_domain):
        self.config['public_domain'] = public_domain

    def set_credentials(self, username, password, tenant_name, auth_url):
        self.config['keystone_username'] = username
        self.config['keystone_password'] = password
        self.config['keystone_url'] = auth_url
        self.config['keystone_tenant_name'] = tenant_name

    def deploy_vnf(self, blueprint, bp_name='vnftopology',
                   dep_name='vnftest'):
        if self.orchestrator:
            self.dep_name = dep_name
            error = self.orchestrator.download_upload_and_deploy_blueprint(
                                                                   blueprint,
                                                                   self.config,
                                                                   bp_name,
                                                                   dep_name)
            if error:
                return error

            self.deploy = True

        else:
            if self.logger:
                self.logger.error("Cloudify manager is down or not provide...")

    def undeploy_vnf(self):
        if self.orchestrator:
            if self.deploy:
                self.deploy = False
                self.orchestrator.undeploy_deployment(self.dep_name)
            else:
                if self.logger:
                    self.logger.error(" %s isn't already deploy..."
                                      %(self.dep_name))
        else:
            if self.logger:
                self.logger.error("Cloudify manager is down or not provide...")
