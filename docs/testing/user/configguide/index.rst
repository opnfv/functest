.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

==================================
OPNFV FUNCTEST Configuration Guide
==================================

.. toctree::
   :numbered:
   :maxdepth: 2

Version history
===============

+------------+----------+------------------+----------------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**                      |
|            |          |                  |                                  |
+------------+----------+------------------+----------------------------------+
| 2016-08-17 | 1.0.0    | Juha Haapavirta  | Colorado release                 |
|            |          | Column Gaynor    |                                  |
+------------+----------+------------------+----------------------------------+
| 2017-01-19 | 1.0.1    | Morgan Richomme  | Adaptations for Danube           |
|            |          |                  | * update testcase list           |
|            |          |                  | * update docker command          |
+------------+----------+------------------+----------------------------------+

Introduction
============
This document describes how to install and configure Functest in OPNFV.
The Functest CLI is used during the Functest environment preparation
phase. The given example commands should work in both virtual and bare
metal cases alike.

High level architecture
-----------------------

The high level architecture of Functest within OPNFV can be described as
follows::

 CIMC/Lights+out management               Admin  Mgmt/API  Public  Storage Private
                                           PXE
 +                                           +       +        +       +       +
 |                                           |       |        |       |       |
 |     +----------------------------+        |       |        |       |       |
 |     |                            |        |       |        |       |       |
 +-----+       Jumphost             |        |       |        |       |       |
 |     |                            +--------+       |        |       |       |
 |     |                            |        |       |        |       |       |
 |     |   +--------------------+   |        |       |        |       |       |
 |     |   |                    |   |        |       |        |       |       |
 |     |   | Tools              |   +----------------+        |       |       |
 |     |   | - Rally            |   |        |       |        |       |       |
 |     |   | - Robot            |   |        |       |        |       |       |
 |     |   | - TestON           |   |        |       |        |       |       |
 |     |   | - RefStack         |   |        |       |        |       |       |
 |     |   |                    |   |-------------------------+       |       |
 |     |   | Testcases          |   |        |       |        |       |       |
 |     |   | - VIM              |   |        |       |        |       |       |
 |     |   |                    |   |        |       |        |       |       |
 |     |   | - SDN Controller   |   |        |       |        |       |       |
 |     |   |                    |   |        |       |        |       |       |
 |     |   | - Features         |   |        |       |        |       |       |
 |     |   |                    |   |        |       |        |       |       |
 |     |   | - VNF              |   |        |       |        |       |       |
 |     |   |                    |   |        |       |        |       |       |
 |     |   +--------------------+   |        |       |        |       |       |
 |     |     Functest Docker        +        |       |        |       |       |
 |     |                            |        |       |        |       |       |
 |     |                            |        |       |        |       |       |
 |     |                            |        |       |        |       |       |
 |     +----------------------------+        |       |        |       |       |
 |                                           |       |        |       |       |
 |    +----------------+                     |       |        |       |       |
 |    |             1  |                     |       |        |       |       |
 +----+ +--------------+-+                   |       |        |       |       |
 |    | |             2  |                   |       |        |       |       |
 |    | | +--------------+-+                 |       |        |       |       |
 |    | | |             3  |                 |       |        |       |       |
 |    | | | +--------------+-+               |       |        |       |       |
 |    | | | |             4  |               |       |        |       |       |
 |    +-+ | | +--------------+-+             |       |        |       |       |
 |      | | | |             5  +-------------+       |        |       |       |
 |      +-+ | |  nodes for     |             |       |        |       |       |
 |        | | |  deploying     +---------------------+        |       |       |
 |        +-+ |  OPNFV         |             |       |        |       |       |
 |          | |                +------------------------------+       |       |
 |          +-+     SUT        |             |       |        |       |       |
 |            |                +--------------------------------------+       |
 |            |                |             |       |        |       |       |
 |            |                +----------------------------------------------+
 |            +----------------+             |       |        |       |       |
 |                                           |       |        |       |       |
 +                                           +       +        +       +       +
              SUT = System Under Test

All the libraries and dependencies needed by all of the Functest tools
are pre-installed into the Docker image. This allows running Functest
on any platform on any Operating System.

The automated mechanisms inside the Functest Docker container will:

  * Retrieve OpenStack credentials
  * Prepare the environment according to the System Under Test (SUT)
  * Perform the appropriate functional tests
  * Push the test results into the OPNFV test result database

This Docker image can be integrated into CI or deployed independently.

Please note that the Functest Docker container has been designed for OPNFV,
however, it would be possible to adapt it to any OpenStack based VIM +
controller environment, since most of the test cases are integrated from
upstream communities.

The functional test cases are described in the Functest User Guide `[2]`_


Prerequisites
=============
The OPNFV deployment is out of the scope of this document but it can be
found in http://docs.opnfv.org.
The OPNFV platform is considered as the SUT in this document.

Several prerequisites are needed for Functest:

    #. A Jumphost to run Functest on
    #. A Docker daemon shall be installed on the Jumphost
    #. A public/external network created on the SUT
    #. An admin/management network created on the SUT
    #. Connectivity from the Jumphost to the SUT public/external network
    #. Connectivity from the Jumphost to the SUT admin/management network

WARNING: Connectivity from Jumphost is essential and it is of paramount
importance to make sure it is working before even considering to install
and run Functest. Make also sure you understand how your networking is
designed to work.

NOTE: **Jumphost** refers to any server which meets the previous
requirements. Normally it is the same server from where the OPNFV
deployment has been triggered previously.

NOTE: If your Jumphost is operating behind a company http proxy and/or
firewall, please consult first the section `Proxy Support`_, towards
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
`Docker Installation on CentOS behind http proxy`_. You should follow
that section before installing the docker engine.

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

By default, the four OPNFV installers provide a fresh installation with
a public/external network created along with a router. Make sure that
the public/external subnet is reachable from the Jumphost.

*Hint:* For the given OPNFV Installer in use, the IP sub-net address
used for the public/external network is usually a planning item and
should thus be known. Consult the OPNFV Configuration guide `[4]`_, and
ensure you can reach each node in the SUT, from the Jumphost using the
'ping' command using the respective IP address on the public/external
network for each node in the SUT. The details of how to determine the
needed IP addresses for each node in the SUT may vary according to the
used installer and are therefore ommitted here.

Connectivity to Admin/Management network on SUT
-----------------------------------------------
Some of the Functest tools need to have access to the OpenStack
admin/management network of the controllers `[1]`_.

For this reason, check the connectivity from the Jumphost to all the
controllers in cluster in the OpenStack admin/management network range.

Installation and configuration
==============================

.. include:: ./configguide.rst

Integration in CI
=================
In CI we use the Docker image and execute the appropriate commands within the
container from Jenkins.

Docker creation in set-functest-env builder `[3]`_::

    envs="-e INSTALLER_TYPE=${INSTALLER_TYPE} -e INSTALLER_IP=${INSTALLER_IP} -e NODE_NAME=${NODE_NAME}"
    [...]
    docker pull opnfv/functest:$DOCKER_TAG >/dev/null
    cmd="sudo docker run -id ${envs} ${volumes} ${custom_params} ${TESTCASE_OPTIONS} opnfv/functest:${DOCKER_TAG} /bin/bash"
    echo "Functest: Running docker run command: ${cmd}"
    ${cmd} >${redirect}
    sleep 5
    container_id=$(docker ps | grep "opnfv/functest:${DOCKER_TAG}" | awk '{print $1}' | head -1)
    echo "Container ID=${container_id}"
    if [ -z ${container_id} ]; then
        echo "Cannot find opnfv/functest container ID ${container_id}. Please check if it is existing."
        docker ps -a
        exit 1
    fi
    echo "Starting the container: docker start ${container_id}"
    docker start ${container_id}
    sleep 5
    docker ps >${redirect}
    if [ $(docker ps | grep "opnfv/functest:${DOCKER_TAG}" | wc -l) == 0 ]; then
        echo "The container opnfv/functest with ID=${container_id} has not been properly started. Exiting..."
        exit 1
    fi

    cmd="python ${FUNCTEST_REPO_DIR}/functest/ci/prepare_env.py start"
    echo "Executing command inside the docker: ${cmd}"
    docker exec ${container_id} ${cmd}


Test execution in functest-all builder `[3]`_::

    branch=${GIT_BRANCH##*/}
    echo "Functest: run $FUNCTEST_SUITE_NAME on branch ${branch}"
    cmd="functest testcase run $FUNCTEST_SUITE_NAME"
    fi
    container_id=$(docker ps -a | grep opnfv/functest | awk '{print $1}' | head -1)
    docker exec $container_id $cmd
    ret_value=$?
    exit $ret_value

Docker clean in functest-cleanup builder `[3]`_ calling docker rm and docker rmi


References
==========
.. _`[1]`: https://ask.openstack.org/en/question/68144/keystone-unable-to-use-the-public-endpoint/
.. _`[2]`: http://artifacts.opnfv.org/functest/docs/userguide/index.html
.. _`[3]`: https://git.opnfv.org/cgit/releng/tree/jjb/functest/functest-ci-jobs.yml
.. _`[4]`: http://artifacts.opnfv.org/functest/danube/docs/configguide/index.html


`OPNFV main site`_

`Functest page`_

IRC support channel: #opnfv-functest

.. _`OPNFV main site`: http://www.opnfv.org
.. _`Functest page`: https://wiki.opnfv.org/functest
