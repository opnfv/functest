.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

==================================
OPNFV FUNCTEST Configuration Guide
==================================

.. toctree::
   :numbered:
   :maxdepth: 2

Introduction
============
This document describes how to install and configure Functest in OPNFV.
The Functest CLI is utilized during the Functest environment preparation step.

High level architecture
-----------------------

The high level architecture of Functest within OPNFV can be described as
follows::

 CIMC/Lights+out management                 Admin     Private   Public   Storage
                                             PXE
                                                                   +
 +                                             +     IP_PRIV/24    |        |
 |                                             |         +         +        |
 |                                             |         |    IP_PUB/24     |
 |     +----------------------------+          |         |         +        |
 |     |                            |          |         |         |        |
 +-----+       Jumphost             |          |         |         |        |
 |     |                            +----------+         |         |        |
 |     |                            |          |         |         |        |
 |     |   +--------------------+   |          |         |         |        |
 |     |   |                    |   |          |         |         |        |
 |     |   | Tools              |   +--------------------+         |        |
 |     |   | - Rally            |   |          |         |         |        |
 |     |   | - Robot            |   |          |         |         |        |
 |     |   | - TestON           |   |          |         |         |        |
 |     |   |                    |   |          |         |         |        |
 |     |   | Testcases          |   |          |         |         |        |
 |     |   | - VIM              |   |          |         |         |        |
 |     |   |  -- vPing          |   |          |         |         |        |
 |     |   |  -- vPing_userdata |   |          |         |         |        |
 |     |   |  -- Tempest        |   |          |         |         |        |
 |     |   |  -- Rally          |   |          |         |         |        |
 |     |   | - Controller       |   |          |         |         |        |
 |     |   |  -- odl            |   |          |         |         |        |
 |     |   |  -- onos           |   |          |         |         |        |
 |     |   |  -- opencontrail   |   |          |         |         |        |
 |     |   |                    |   |          |         |         |        |
 |     |   | Features           |   |          |         |         |        |
 |     |   | - vIMS             |   |          |         |         |        |
 |     |   |                    |   |          |         |         |        |
 |     |   +--------------------+   |          |         |         |        |
 |     |                            +------------------------------+        |
 |     |    Functest Docker         |          |         |         |        |
 |     |                            +---------------------------------------+
 |     |                            |          |         |         |        |
 |     +----------------------------+          |         |         |        |
 |                                             |         |         |        |
 |    +----------------+                       |         |         |        |
 |    |             1  |                       |         |         |        |
 +----+ +--------------+-+                     |         |         |        |
 |    | |             2  |                     |         |         |        |
 |    | | +--------------+-+                   |         |         |        |
 |    | | |             3  |                   |         |         |        |
 |    | | | +--------------+-+                 |         |         |        |
 |    | | | |             4  |                 |         |         |        |
 |    +-+ | | +--------------+-+               |         |         |        |
 |      | | | |             5  +---------------+         |         |        |
 |      +-+ | |  nodes for     |               |         |         |        |
 |        | | |  deploying     +-------------------------+         |        |
 |        +-+ |  OPNFV         |               |         |         |        |
 |          | |                +-----------------------------------+        |
 |          +-+     SUT        |               |         |         |        |
 |            |                +--------------------------------------------+
 |            +----------------+               |         |         |        |
 |                                             |         |         |        |
 +                                             +         +         +        +
              SUT = System Under Test

All the libraries and dependencies needed by all of the Functest tools are
pre-installed into the Docker image. This allows running Functest on any
platform on any Operating System.

The automated mechanisms inside the Functest Docker container will:

  * retrieve OpenStack credentials
  * prepare the environment according to the SUT
  * perform the appropriate functional tests
  * push the test results into the OPNFV test result database

This Docker image can be integrated into CI or deployed independently.

Please note that the Functest Docker container has been designed for OPNFV,
however, it would be possible to adapt it to any VIM+controller environment,
since most of the test cases are integrated from upstream communities.

The test cases are described in the Functest User Guide `[2]`_


Prerequisites
=============
The OPNFV deployment is out of the scope of this document but it can be found
in `[4]`_. The OPNFV platform is considered as the System Under Test (SUT) in
this document.

Several prerequisites are needed for Functest:

    #. A Jumphost to run Functest on
    #. A Docker daemon shall be installed on the Jumphost
    #. A public/external network created on the SUT
    #. An admin/management network created on the SUT
    #. Connectivity from the Jumphost to the SUT public/external network
    #. Connectivity from the Jumphost to the SUT admin/management network

NOTE: **Jumphost** refers to any server which meets the previous requirements.
Normally it is the same server from where the OPNFV deployment has been
triggered previously.

Docker installation
-------------------
.. _Ubuntu: https://docs.docker.com/installation/ubuntulinux/
.. _RHEL: https://docs.docker.com/installation/rhel/
.. _CentOS: https://docs.docker.com/engine/installation/linux/centos/

*Tip:* If your Jumphost is operating behind a company http proxy and/or
Firewall, please consult first the section `Proxy Support`_, towards the end
of this document. The section details some tips/tricks which *may* be of help
in a proxified environment.

Log on to your Jumphost and install the Docker Engine (e.g. for Ubuntu)::

 curl -sSL https://get.docker.com/ | sh

Add your user to docker group to be able to run commands without sudo::

 sudo usermod -aG docker <your_user>

A reconnect is needed. There are 2 ways for this:
    #. Re-login to your account
    #. su - <username>

If your Jumphost is based on Red Hat Enterprise Linux, or CentOS 7 linux,
please consult the references below.

References - Installing Docker Engine on different Linux Operating Systems:

  * Ubuntu_
  * RHEL_
  * CentOS_

Public/External network on SUT
------------------------------
Some of the tests against the VIM (Virtual Infrastructure Manager) need
connectivity through an existing public/external network in order to succeed.
This is needed, for example, to create floating IPs to access VM instances
through the public/external network (i.e. from the Docker container).

By default, the four OPNFV installers provide a fresh installation with a
public/external network created along with a router. Make sure that the
public/external subnet is reachable from the Jumphost.

*Hint:* For the given OPNFV Installer in use, the IP sub-net address used for
the public/external network is usually a planning item and should thus be known.
Consult the OPNFV Configuration guide `[4]`_, and ensure you can reach each
node in the SUT, from the Jumphost using the 'ping' command using the
respective IP address on the public/external network for each node in the SUT.
(The details of how to determine the needed IP addresses for each node in the
SUT may vary according to the used installer and are therefore ommitted here.)

Connectivity to OPNFV admin/management network
----------------------------------------------
Some of the Functest tools need to have access to the OpenStack admin/management
network of the controllers `[1]`_.

For this reason, an interface shall be configured in the Jumphost in the OpenStack admin/management network range.

For example, if the admin/management network is using VLAN 300 and subnet 192.168.1.0/24 and assuming that eth1 is the
physical interface with access to that subnet::

    ip link add name eth1.300 link eth1 type vlan id 300
    ip link set eth1.300 up
    ip addr add 192.168.1.66/24 dev eth1.300

This is just an example about how to configure an interface with vlan, but it might differ depending on the deployment
settings on each installer. Check the corresponding installer instructions for more precise instructions.


Installation and configuration
==============================

.. include:: ./configguide.rst

Integration in CI
=================
In CI we use the Docker image and execute the appropriate commands within the
container from Jenkins.

Docker creation in set-functest-env builder `[3]`_::

    envs="INSTALLER_TYPE=${INSTALLER_TYPE} -e INSTALLER_IP=${INSTALLER_IP} -e NODE_NAME=${NODE_NAME}"
    [...]
    docker pull opnfv/functest:latest_stable
    cmd="docker run -id -e $envs ${labconfig} ${sshkey} ${res_volume} opnfv/functest:latest_stable /bin/bash"
    echo "Functest: Running docker run command: ${cmd}"
    ${cmd}
    docker ps -a
    sleep 5
    container_id=$(docker ps | grep 'opnfv/functest:latest_stable' | awk '{print $1}' | head -1)
    echo "Container ID=${container_id}"
    if [ -z ${container_id} ]; then
        echo "Cannot find opnfv/functest container ID ${container_id}. Please check if it is existing."
        docker ps -a
        exit 1
    fi
    echo "Starting the container: docker start ${container_id}"
    docker start ${container_id}
    sleep 5
    docker ps
    if [ $(docker ps | grep 'opnfv/functest:latest_stable' | wc -l) == 0 ]; then
        echo "The container opnfv/functest with ID=${container_id} has not been properly started. Exiting..."
        exit 1
    fi
    cmd="${FUNCTEST_REPO_DIR}/docker/prepare_env.sh"
    echo "Executing command inside the docker: ${cmd}"
    docker exec ${container_id} ${cmd}


Test execution in functest-all builder `[3]`_::

  echo "Functest: run $FUNCTEST_SUITE_NAME"
  cmd="${FUNCTEST_REPO_DIR}/docker/run_tests.sh --test $FUNCTEST_SUITE_NAME ${flag}"
  container_id=$(docker ps -a | grep opnfv/functest | awk '{print $1}' | head -1)
  docker exec $container_id $cmd

Docker clean in functest-cleanup builder `[3]`_::

    echo "Cleaning up docker containers/images..."
    # Remove previous running containers if exist
    if [[ ! -z $(docker ps -a | grep opnfv/functest) ]]; then
    echo "Removing existing opnfv/functest containers..."
    docker ps | grep opnfv/functest | awk '{print $1}' | xargs docker stop
    docker ps -a | grep opnfv/functest | awk '{print $1}' | xargs docker rm
    fi

    # Remove existing images if exist
    if [[ ! -z $(docker images | grep opnfv/functest) ]]; then
    echo "Docker images to remove:"
    docker images | head -1 && docker images | grep opnfv/functest
    image_tags=($(docker images | grep opnfv/functest | awk '{print $2}'))
    for tag in "${image_tags[@]}"; do
        echo "Removing docker image opnfv/functest:$tag..."
        docker rmi opnfv/functest:$tag
    done
    fi


References
==========
.. _`[1]`: https://ask.openstack.org/en/question/68144/keystone-unable-to-use-the-public-endpoint/
.. _`[2]`: http://artifacts.opnfv.org/functest/docs/userguide/index.html
.. _`[3]`: https://git.opnfv.org/cgit/releng/tree/jjb/functest/functest-ci-jobs.yml
.. _`[4]`: http://artifacts.opnfv.org/opnfvdocs/brahmaputra/docs/configguide/index.html


OPNFV main site: opnfvmain_.

OPNFV functional test page: opnfvfunctest_.

IRC support channel: #opnfv-testperf

.. _opnfvmain: http://www.opnfv.org
.. _opnfvfunctest: https://wiki.opnfv.org/opnfv_functional_testing
