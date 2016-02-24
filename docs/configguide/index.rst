===============================================
OPNFV FUNCTEST configuration/installation guide
===============================================

.. toctree::
   :numbered:
   :maxdepth: 2

Introduction
============

** DOCUMENT IS IN PROGRESS FOR BRAHMAPUTRA **

This document describes how to install and configure Functest in OPNFV.

Prerequisites
=============

The OPNFV deployment is out of the scope of this document but it can be found in
XXX. The OPNFV platform is considered as the System Under Test (SUT) in this
document.

Several prerequisites are needed for functest:

    #. A Jumphost to run Functest on
    #. Docker daemon shall be installed on the Jumphost
    #. A public/external network created on the SUT
    #. Connectivity from the Jumphost to the SUT public/external network
    #. Connectivity from the Jumphost to the SUT management network

NOTE: “Jumphost” refers to any server which meets the previous requirements.
Normally it is the same server from where the OPNFV deployment has been
triggered.

Docker installation
-------------------

.. _Ubuntu: https://docs.docker.com/installation/ubuntulinux/
.. _RHEL: https://docs.docker.com/installation/rhel/

Log on your jumphost then install docker (e.g. for Ubuntu)::

 curl -sSL https://get.docker.com/ | sh

Add your user to docker group to be able to run commands without sudo::

 sudo usermod -aG docker <your_user>


References:

  * Ubuntu_
  * RHEL_

Connectivity to OPNFV management network
----------------------------------------

Some of the Functest tools need to have access to the OpenStack management
network of the controllers `[1]`_.

For this reason, an interface shall be configured in the Jumphost in the
OpenStack management network range.

Example::

 The OPNFV Fuel installation uses VLAN tagged 300 and subnet 192.168.1.0/24 as
 Openstack Management network.
 .
 Supposing that eth1 is the physical interface with access to that subnet:
 $ ip link add name eth1.300 link eth1 type vlan id 300
 $ ip link set eth1.300 up
 $ ip addr add 192.168.1.66/24 dev eth1.300


External network on SUT
-----------------------

Some of the tests against the VIM (Virtual Infrastructure Manager) need an
existing public network to succeed. This is needed, for example, to create
floating IPs to access instances from the public network (i.e. Jumphost).

By default, any of the four OPNFV installers provide a fresh installation with
an external network created along with a router.



High level architecture
=======================

The high level architecture of Functest within OPNFV can be described as follow::

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
 |        +-+ |  opnfv         |               |         |         |        |
 |          | |     SUT        +-----------------------------------+        |
 |          +-+                |               |         |         |        |
 |            |                +--------------------------------------------+
 |            +----------------+               |         |         |        |
 |                                             |         |         |        |
 |                                             +         +         +        +

All the libraries and dependencies needed by all the Functest tools are
pre-installed in the Docker image.
This allows running Functest on any platform with any Operating System.

The Docker image will:

  * retrieve OpenStack credentials
  * prepare the environment according to the SUT
  * perform the appropriate tests
  * push the results into the OPNFV test result database



This Docker image can be integrated into CI or deployed **independently** of the CI.
A description of the Brahmaputra testcases can be retrieved in the Functest user
guide `[2]`_

Please note that the Functest container has been designed for OPNFV, however, it
would be possible to adapt it to any VIM+controller environment as most of the
testcases are upstream testcases.

.. include:: ./configguide.rst

NOTE: This will run ALL the tests by default, see `[2]`_ for details

Focus on the OpenStack credentials
----------------------------------

The OpenStack credentials are needed to test the VIM. There are 3 ways to
provide them to Functest:

  * using the -v option when running the Docker container
  * create an empty file in /home/opnfv/functest/conf/openstack.creds and paste
    the needed info in it.
  * automatically retrieved using the following script::
         $repos_dir/releng/utils/fetch_os_creds.sh

Once the credentials are there, they shall be sourced before running the tests::

    source /home/opnfv/functest/conf/openstack.creds

Additional Options
------------------

In case you need to provide different configuration parameters to Functest (e.g.
 commit IDs or branches for the repositories, ...) copy the config_functest.yaml
 from the repository to your current directory and run docker with a volume::

    $ wget https://git.opnfv.org/cgit/functest/plain/testcases/config_functest.yaml
    $ cmd1 = "/home/opnfv/repos/functest/docker/prepare_env.sh"
    $ cmd2 = "/home/opnfv/repos/functest/docker/run_tests.sh"
    $ docker run -t -e "INSTALLER_TYPE=fuel" -e "INSTALLER_IP=10.20.0.2" opnfv/functest \
        -v $(pwd)/config_functest.yaml:/home/opnfv/functest/conf/config_functest.yaml \
        "${cmd1} && ${cmd2}"


Integration in CI
=================

In CI we use the docker file and execute commande within the container from
Jenkins.

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


Configuration
=============

Everything is preconfigured in the docker file.
It is however possible to customize the list of tests, see `[2]` for details.

Errors
======





References
==========
.. _`[1]`: https://ask.openstack.org/en/question/68144/keystone-unable-to-use-the-public-endpoint/
.. _`[2]`: url functest user guide
.. _`[3]`: https://git.opnfv.org/cgit/releng/tree/jjb/functest/functest-ci-jobs.yml


OPNFV main site: opnfvmain_.

OPNFV functional test page: opnfvfunctest_.

IRC support channel: #opnfv-testperf

.. _opnfvmain: http://www.opnfv.org
.. _opnfvfunctest: https://wiki.opnfv.org/opnfv_functional_testing
.. _`OpenRC`: http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html
.. _`Rally installation procedure`: https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html
.. _`config_test.py` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.py
.. _`config_functest.yaml` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.yaml
