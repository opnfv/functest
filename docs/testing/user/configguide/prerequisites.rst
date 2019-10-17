.. SPDX-License-Identifier: CC-BY-4.0

Prerequisites
=============
The OPNFV deployment is out of the scope of this document but it can be
found in https://docs.opnfv.org/en/stable-hunter/.
The OPNFV platform is considered as the SUT in this document.

Several prerequisites are needed for Functest:

    #. A Jumphost to run Functest on
    #. A Docker daemon shall be installed on the Jumphost
    #. A public/external network created on the SUT
    #. An admin/management network created on the SUT
    #. Connectivity from the Jumphost to the SUT public/external network

WARNING: Connectivity from Jumphost is essential and it is of paramount
importance to make sure it is working before even considering to install
and run Functest. Make also sure you understand how your networking is
designed to work.

NOTE: **Jumphost** refers to any server which meets the previous
requirements. Normally it is the same server from where the OPNFV
deployment has been triggered previously, but it could be any server
with proper connectivity to the SUT.

NOTE: If your Jumphost is operating behind a company http proxy and/or
firewall, please consult first the section :ref:`Proxy support`, towards
the end of this document. The section details some tips/tricks which
*may* be of help in a proxified environment.

Docker installation
-------------------
Docker installation and configuration is only needed to be done once
through the life cycle of Jumphost.

If your Jumphost is based on Ubuntu, SUSE, RHEL or CentOS linux, please
consult the references below for more detailed instructions. The
commands below are offered as a short reference.

*Tip:* For running docker containers behind the proxy, you need first
some extra configuration which is described in section
:ref:`Docker Installation on CentOS behind http proxy`. You should follow that
section before installing the docker engine.

Docker installation needs to be done as root user. You may use other
userid's to create and run the actual containers later if so desired.
Log on to your Jumphost as root user and install the Docker Engine
(e.g. for CentOS family)::

 curl -sSL https://get.docker.com/ | sh
 systemctl start docker

 *Tip:* If you are working through proxy, please set the https_proxy
 environment variable first before executing the curl command.

Add your user to docker group to be able to run commands without sudo::

 sudo usermod -aG docker <your_user>

A reconnection is needed. There are 2 ways for this:
    #. Re-login to your account
    #. su - <username>

References - Installing Docker Engine on different Linux Operating Systems:
  * Ubuntu_
  * RHEL_
  * CentOS_
  * SUSE_

.. _Ubuntu: https://docs.docker.com/engine/installation/linux/ubuntulinux/
.. _RHEL:   https://docs.docker.com/engine/installation/linux/rhel/
.. _CentOS: https://docs.docker.com/engine/installation/linux/centos/
.. _SUSE: https://docs.docker.com/engine/installation/linux/suse/

Public/External network on SUT
------------------------------
Some of the tests against the VIM (Virtual Infrastructure Manager) need
connectivity through an existing public/external network in order to
succeed. This is needed, for example, to create floating IPs to access
VM instances through the public/external network (i.e. from the Docker
container).

By default, the five OPNFV installers provide a fresh installation with
a public/external network created along with a router. Make sure that
the public/external subnet is reachable from the Jumphost and an external
router exists.

*Hint:* For the given OPNFV Installer in use, the IP sub-net address
used for the public/external network is usually a planning item and
should thus be known. Ensure you can reach each node in the SUT, from the
Jumphost using the 'ping' command using the respective IP address on the
public/external network for each node in the SUT. The details of how to
determine the needed IP addresses for each node in the SUT may vary according
to the used installer and are therefore omitted here.
