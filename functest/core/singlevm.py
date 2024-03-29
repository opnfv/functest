#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Ease deploying a single VM reachable via ssh

It offers a simple way to create all tenant network resources + a VM for
advanced testcases (e.g. deploying an orchestrator).
"""

import logging
import re
import tempfile
import time

import paramiko
from xtesting.core import testcase

from functest.core import tenantnetwork
from functest.utils import config
from functest.utils import env
from functest.utils import functest_utils


class VmReady1(tenantnetwork.TenantNetwork1):
    """Prepare a single VM (scenario1)

    It inherits from TenantNetwork1 which creates all network resources and
    prepares a future VM attached to that network.

    It ensures that all testcases inheriting from SingleVm1 could work
    without specific configurations (or at least read the same config data).
    """
    # pylint: disable=too-many-instance-attributes

    __logger = logging.getLogger(__name__)
    filename = '/home/opnfv/functest/images/cirros-0.6.1-x86_64-disk.img'
    image_format = 'qcow2'
    extra_properties = {}
    filename_alt = filename
    image_alt_format = image_format
    extra_alt_properties = extra_properties
    visibility = 'private'
    flavor_ram = 512
    flavor_vcpus = 1
    flavor_disk = 1
    flavor_extra_specs = {}
    flavor_alt_ram = 1024
    flavor_alt_vcpus = 1
    flavor_alt_disk = 1
    flavor_alt_extra_specs = flavor_extra_specs
    create_server_timeout = 180

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'vmready1'
        super().__init__(**kwargs)
        self.image = None
        self.flavor = None

    def publish_image(self, name=None):
        """Publish image

        It allows publishing multiple images for the child testcases. It forces
        the same configuration for all subtestcases.

        Returns: image

        Raises: expection on error
        """
        assert self.cloud
        extra_properties = self.extra_properties.copy()
        if env.get('IMAGE_PROPERTIES'):
            extra_properties.update(
                functest_utils.convert_ini_to_dict(
                    env.get('IMAGE_PROPERTIES')))
        extra_properties.update(
            getattr(config.CONF, f'{self.case_name}_extra_properties', {}))
        image = self.cloud.create_image(
            name if name else f'{self.case_name}-img_{self.guid}',
            filename=getattr(
                config.CONF, f'{self.case_name}_image',
                self.filename),
            meta=extra_properties,
            disk_format=getattr(
                config.CONF, f'{self.case_name}_image_format',
                self.image_format),
            visibility=getattr(
                config.CONF, f'{self.case_name}_visibility',
                self.visibility),
            wait=True)
        self.__logger.debug("image: %s", image)
        return image

    def publish_image_alt(self, name=None):
        """Publish alternative image

        It allows publishing multiple images for the child testcases. It forces
        the same configuration for all subtestcases.

        Returns: image

        Raises: expection on error
        """
        assert self.cloud
        extra_alt_properties = self.extra_alt_properties.copy()
        if env.get('IMAGE_PROPERTIES'):
            extra_alt_properties.update(
                functest_utils.convert_ini_to_dict(
                    env.get('IMAGE_PROPERTIES')))
        extra_alt_properties.update(
            getattr(config.CONF, f'{self.case_name}_extra_alt_properties', {}))
        image = self.cloud.create_image(
            name if name else f'{self.case_name}-img_alt_{self.guid}',
            filename=getattr(
                config.CONF, f'{self.case_name}_image_alt',
                self.filename_alt),
            meta=extra_alt_properties,
            disk_format=getattr(
                config.CONF, f'{self.case_name}_image_alt_format',
                self.image_format),
            visibility=getattr(
                config.CONF, f'{self.case_name}_visibility',
                self.visibility),
            wait=True)
        self.__logger.debug("image: %s", image)
        return image

    def create_flavor(self, name=None):
        """Create flavor

        It allows creating multiple flavors for the child testcases. It forces
        the same configuration for all subtestcases.

        Returns: flavor

        Raises: expection on error
        """
        assert self.orig_cloud
        flavor = self.orig_cloud.create_flavor(
            name if name else f'{self.case_name}-flavor_{self.guid}',
            getattr(config.CONF, f'{self.case_name}_flavor_ram',
                    self.flavor_ram),
            getattr(config.CONF, f'{self.case_name}_flavor_vcpus',
                    self.flavor_vcpus),
            getattr(config.CONF, f'{self.case_name}_flavor_disk',
                    self.flavor_disk))
        self.__logger.debug("flavor: %s", flavor)
        flavor_extra_specs = self.flavor_extra_specs.copy()
        if env.get('FLAVOR_EXTRA_SPECS'):
            flavor_extra_specs.update(
                functest_utils.convert_ini_to_dict(
                    env.get('FLAVOR_EXTRA_SPECS')))
        flavor_extra_specs.update(
            getattr(config.CONF,
                    f'{self.case_name}_flavor_extra_specs', {}))
        self.orig_cloud.set_flavor_specs(flavor.id, flavor_extra_specs)
        return flavor

    def create_flavor_alt(self, name=None):
        """Create flavor

        It allows creating multiple alt flavors for the child testcases. It
        forces the same configuration for all subtestcases.

        Returns: flavor

        Raises: expection on error
        """
        assert self.orig_cloud
        flavor = self.orig_cloud.create_flavor(
            name if name else f'{self.case_name}-flavor_alt_{self.guid}',
            getattr(config.CONF, f'{self.case_name}_flavor_alt_ram',
                    self.flavor_alt_ram),
            getattr(config.CONF, f'{self.case_name}_flavor_alt_vcpus',
                    self.flavor_alt_vcpus),
            getattr(config.CONF, f'{self.case_name}_flavor_alt_disk',
                    self.flavor_alt_disk))
        self.__logger.debug("flavor: %s", flavor)
        flavor_alt_extra_specs = self.flavor_alt_extra_specs.copy()
        if env.get('FLAVOR_EXTRA_SPECS'):
            flavor_alt_extra_specs.update(
                functest_utils.convert_ini_to_dict(
                    env.get('FLAVOR_EXTRA_SPECS')))
        flavor_alt_extra_specs.update(
            getattr(config.CONF,
                    f'{self.case_name}_flavor_alt_extra_specs', {}))
        self.orig_cloud.set_flavor_specs(
            flavor.id, flavor_alt_extra_specs)
        return flavor

    def boot_vm(self, name=None, **kwargs):
        """Boot the virtual machine

        It allows booting multiple machines for the child testcases. It forces
        the same configuration for all subtestcases.

        Returns: vm

        Raises: expection on error
        """
        assert self.cloud
        vm1 = self.cloud.create_server(
            name if name else f'{self.case_name}-vm_{self.guid}',
            image=self.image.id, flavor=self.flavor.id,
            auto_ip=False,
            network=self.network.id if self.network else env.get(
                "EXTERNAL_NETWORK"),
            timeout=self.create_server_timeout, wait=True, **kwargs)
        self.__logger.debug("vm: %s", vm1)
        return vm1

    def check_regex_in_console(self, name, regex=' login: ', loop=6):
        """Wait for specific message in console

        Returns: True or False on errors
        """
        assert self.cloud
        for iloop in range(loop):
            console = self.cloud.get_server_console(name)
            self.__logger.debug("console: \n%s", console)
            if re.search(regex, console):
                self.__logger.debug(
                    "regex found: '%s' in console\n%s", regex, console)
                return True
            self.__logger.debug(
                "try %s: cannot find regex '%s' in console\n%s",
                iloop + 1, regex, console)
            time.sleep(10)
        self.__logger.error("cannot find regex '%s' in console", regex)
        return False

    def clean_orphan_security_groups(self):
        """Clean all security groups which are not owned by an existing tenant

        It lists all orphan security groups in use as debug to avoid
        misunderstanding the testcase results (it could happen if cloud admin
        removes accounts without cleaning the virtual machines)
        """
        sec_groups = self.orig_cloud.list_security_groups()
        for sec_group in sec_groups:
            if not sec_group.tenant_id:
                continue
            if not self.orig_cloud.get_project(sec_group.tenant_id):
                self.__logger.debug("Cleaning security group %s", sec_group.id)
                try:
                    self.orig_cloud.delete_security_group(sec_group.id)
                except Exception:  # pylint: disable=broad-except
                    self.__logger.debug(
                        "Orphan security group %s in use", sec_group.id)

    def count_hypervisors(self):
        """Count hypervisors."""
        if env.get('SKIP_DOWN_HYPERVISORS').lower() == 'false':
            return len(self.orig_cloud.list_hypervisors())
        return self.count_active_hypervisors()

    def count_active_hypervisors(self):
        """Count all hypervisors which are up."""
        compute_cnt = 0
        for hypervisor in self.orig_cloud.list_hypervisors():
            if hypervisor['state'] == 'up':
                compute_cnt += 1
            else:
                self.__logger.warning(
                    "%s is down", hypervisor['hypervisor_hostname'])
        return compute_cnt

    def run(self, **kwargs):
        """Boot the new VM

        Here are the main actions:
        - publish the image
        - create the flavor

        Returns:
        - TestCase.EX_OK
        - TestCase.EX_RUN_ERROR on error
        """
        status = testcase.TestCase.EX_RUN_ERROR
        try:
            assert self.cloud
            assert super().run(
                **kwargs) == testcase.TestCase.EX_OK
            self.image = self.publish_image()
            self.flavor = self.create_flavor()
            self.result = 100
            status = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception('Cannot run %s', self.case_name)
            self.result = 0
        finally:
            self.stop_time = time.time()
        return status

    def clean(self):
        try:
            assert self.orig_cloud
            assert self.cloud
            super().clean()
            if self.image:
                self.cloud.delete_image(self.image.id)
            if self.flavor:
                self.orig_cloud.delete_flavor(self.flavor.id)
            if env.get('CLEAN_ORPHAN_SECURITY_GROUPS').lower() == 'true':
                self.clean_orphan_security_groups()
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot clean all resources")


class VmReady2(VmReady1):
    """Deploy a single VM reachable via ssh (scenario2)

    It creates new user/project before creating and configuring all tenant
    network resources, flavors, images, etc. required by advanced testcases.

    It ensures that all testcases inheriting from SingleVm2 could work
    without specific configurations (or at least read the same config data).
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'vmready2'
        super().__init__(**kwargs)
        try:
            assert self.orig_cloud
            self.project = tenantnetwork.NewProject(
                self.orig_cloud, self.case_name, self.guid)
            self.project.create()
            self.cloud = self.project.cloud
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot create user or project")
            self.cloud = None
            self.project = None

    def clean(self):
        try:
            super().clean()
            assert self.project
            self.project.clean()
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot clean all resources")


class SingleVm1(VmReady1):
    """Deploy a single VM reachable via ssh (scenario1)

    It inherits from TenantNetwork1 which creates all network resources and
    completes it by booting a VM attached to that network.

    It ensures that all testcases inheriting from SingleVm1 could work
    without specific configurations (or at least read the same config data).
    """
    # pylint: disable=too-many-instance-attributes

    __logger = logging.getLogger(__name__)
    username = 'cirros'
    ssh_connect_timeout = 1
    ssh_connect_loops = 6
    create_floating_ip_timeout = 120
    check_console_loop = 6
    check_console_regex = ' login: '

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'singlevm1'
        super().__init__(**kwargs)
        self.sshvm = None
        self.sec = None
        self.fip = None
        self.keypair = None
        self.ssh = None
        (_, self.key_filename) = tempfile.mkstemp()

    def prepare(self):
        """Create the security group and the keypair

        It can be overriden to set other rules according to the services
        running in the VM

        Raises: Exception on error
        """
        assert self.cloud
        self.keypair = self.cloud.create_keypair(
            f'{self.case_name}-kp_{self.guid}')
        self.__logger.debug("keypair: %s", self.keypair)
        self.__logger.debug("private_key:\n%s", self.keypair.private_key)
        with open(
                self.key_filename, 'w', encoding='utf-8') as private_key_file:
            private_key_file.write(self.keypair.private_key)
        self.sec = self.cloud.create_security_group(
            f'{self.case_name}-sg_{self.guid}',
            f'created by OPNFV Functest ({self.case_name})')
        self.cloud.create_security_group_rule(
            self.sec.id, port_range_min='22', port_range_max='22',
            protocol='tcp', direction='ingress')
        self.cloud.create_security_group_rule(
            self.sec.id, protocol='icmp', direction='ingress')

    def connect(self, vm1):
        """Connect to a virtual machine via ssh

        It first adds a floating ip to the virtual machine and then establishes
        the ssh connection.

        Returns:
        - (fip, ssh)
        - None on error
        """
        assert vm1
        fip = None
        if env.get('NO_TENANT_NETWORK').lower() != 'true':
            fip = self.cloud.create_floating_ip(
                network=self.ext_net.id, server=vm1, wait=True,
                timeout=self.create_floating_ip_timeout)
            self.__logger.debug("floating_ip: %s", fip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        for loop in range(self.ssh_connect_loops):
            try:
                p_console = self.cloud.get_server_console(vm1)
                self.__logger.debug("vm console: \n%s", p_console)
                ssh.connect(
                    fip.floating_ip_address if fip else vm1.public_v4,
                    username=getattr(
                        config.CONF,
                        f'{self.case_name}_image_user', self.username),
                    key_filename=self.key_filename,
                    timeout=getattr(
                        config.CONF,
                        f'{self.case_name}_vm_ssh_connect_timeout',
                        self.ssh_connect_timeout))
                break
            except Exception as exc:  # pylint: disable=broad-except
                self.__logger.debug(
                    "try %s: cannot connect to %s: %s", loop + 1,
                    fip.floating_ip_address if fip else vm1.public_v4, exc)
                time.sleep(9)
        else:
            self.__logger.error(
                "cannot connect to %s", fip.floating_ip_address)
            return None
        return (fip, ssh)

    def execute(self):
        """Say hello world via ssh

        It can be overriden to execute any command.

        Returns: echo exit codes
        """
        (_, stdout, stderr) = self.ssh.exec_command('echo Hello World')
        self.__logger.debug("output:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("error:\n%s", stderr.read().decode("utf-8"))
        return stdout.channel.recv_exit_status()

    def run(self, **kwargs):
        """Boot the new VM

        Here are the main actions:
        - add a new ssh key
        - boot the VM
        - create the security group
        - execute the right command over ssh

        Returns:
        - TestCase.EX_OK
        - TestCase.EX_RUN_ERROR on error
        """
        status = testcase.TestCase.EX_RUN_ERROR
        try:
            assert self.cloud
            assert super().run(
                **kwargs) == testcase.TestCase.EX_OK
            self.result = 0
            self.prepare()
            self.sshvm = self.boot_vm(
                key_name=self.keypair.id, security_groups=[self.sec.id])
            if self.check_regex_in_console(
                    self.sshvm.name, regex=self.check_console_regex,
                    loop=self.check_console_loop):
                (self.fip, self.ssh) = self.connect(self.sshvm)
                if not self.execute():
                    self.result = 100
                    status = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception('Cannot run %s', self.case_name)
        finally:
            self.stop_time = time.time()
        return status

    def clean(self):
        try:
            assert self.orig_cloud
            assert self.cloud
            if self.fip:
                self.cloud.delete_floating_ip(self.fip.id)
            if self.sshvm:
                self.cloud.delete_server(self.sshvm, wait=True)
            if self.sec:
                self.cloud.delete_security_group(self.sec.id)
            if self.keypair:
                self.cloud.delete_keypair(self.keypair.name)
            super().clean()
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot clean all resources")


class SingleVm2(SingleVm1):
    """Deploy a single VM reachable via ssh (scenario2)

    It creates new user/project before creating and configuring all tenant
    network resources and vms required by advanced testcases.

    It ensures that all testcases inheriting from SingleVm2 could work
    without specific configurations (or at least read the same config data).
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'singlevm2'
        super().__init__(**kwargs)
        try:
            assert self.orig_cloud
            self.project = tenantnetwork.NewProject(
                self.orig_cloud, self.case_name, self.guid)
            self.project.create()
            self.cloud = self.project.cloud
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot create user or project")
            self.cloud = None
            self.project = None

    def clean(self):
        try:
            super().clean()
            assert self.project
            self.project.clean()
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot clean all resources")
