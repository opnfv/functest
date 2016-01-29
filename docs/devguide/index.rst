******************************
OPNFV FUNCTEST developer guide
******************************

.. toctree::
   :numbered:
   :maxdepth: 2


============
Introduction
============

This document describes how feature projects aiming to run functional tests can be integrated into FuncTest framework.


================================
Functest High level architecture
================================

Functest is project delivering a test container dedicated to OPNFV.
It includes the tools, the scripts and the test scenarios.

Functest can be described as follow::

 +----------------------+
 |                      |
 |   +--------------+   |                  +-------------------+
 |   |              |   |    Public        |                   |
 |   | Tools        |   +------------------+      OPNFV        |
 |   | Scripts      |   |                  | System Under Test |
 |   | Scenarios    |   +------------------+                   |
 |   |              |   |    Management    |                   |
 |   +--------------+   |                  +-------------------+
 |                      |
 |    Functest Docker   |
 |                      |
 +----------------------+

Functest deals with internal and external test cases.
The Internal test cases in Brahmaputra are:

 * vPing
 * ODL
 * Tempest
 * vIMS
 * Rally

see `[2]`_ for details.

Functest can also be considered as a framework that may include external OPNFV projects.
This framework will ease the integration of the feature test suite to the CI.

==================
How Functest works
==================

The installation and the launch of the Functest docker image is described in `[1]`_.

The Functest docker directories are::

 home
    |
    `-- opnfv
        |-- functest
        |   |-- conf
        |   |-- data
        |   `-- results
        `-- repos
            |-- bgpvpn
            |-- doctor
            |-- functest
            |-- odl_integration
            |-- onos
            |-- ovno
            |-- promise
            |-- rally
            |-- releng
            `-- vims-test


+--------------+-------------------+---------------------------------------------------------+
| Directory    | Subdirectory      | Comments                                                |
+--------------+-------------------+---------------------------------------------------------+
|              | <project>/conf    | All the useful configuration file(s) for <project>      |
|              |                   | the openstack creds are put there for CI                |
|              |                   | It is recommended to push it there when passing the     |
|              |                   | credentials to container through the -v option          |
|              +-------------------+---------------------------------------------------------+
|    opnfv     | <project>/data    | Usefull data, images for <projects>                     |
|              |                   | By default we put an image cirros-0.3.4-x86_64-disk.img |
|              |                   | This image can be used by any projects                  |
|              +-------------------+---------------------------------------------------------+
|              | <project>/results | Local result directory of project <project>             |
+--------------+-------------------+---------------------------------------------------------+
|              | bgpvpn            |                                                         |
|              +-------------------+                                                         +
| repos        | doctor            |                                                         |
|              +-------------------+                                                         +
|              | functest          |                                                         |
|              +-------------------+                                                         +
|              | odl_integration   |                                                         |
|              +-------------------+    Clone of the useful repositories                     +
|              | onos              |     These repositories may include:                     |
|              +-------------------+                - tooling                                +
|              | promise           |                - scenario                               |
|              +-------------------+                - scripts                                +
|              | rally             |                                                         |
|              +-------------------+                                                         +
|              | releng            |                                                         |
|              +-------------------+                                                         +
|              | vims-test         |                                                         |
|              +-------------------+                                                         +
|              | <your project>    |                                                         |
+--------------+-------------------+---------------------------------------------------------+

Before running the test suite, you must prepare the environement by running::

 $ /home/opnfv/repos/functest/docker/prepare_env.sh

By running prepare_env.sh, you build the test environement required by the tests including the retrieval and sourcing of OpenStack credentials.
This is an example of the env variables we have in the docker container:

 * HOSTNAME=373f77816eb0
 * INSTALLER_TYPE=fuel
 * repos_dir=/home/opnfv/repos
 * INSTALLER_IP=10.20.0.2
 * PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
 * PWD=/home/opnfv
 * SHLVL=1
 * HOME=/home/opnfv
 * NODE_NAME=opnfv-jump-2
 * creds=/home/opnfv/functest/conf/openstack.creds
 * _=/usr/bin/env

The prepare_env.sh will source the credentials, so once run you should have access to the following env variables::

 root@373f77816eb0:~# env|grep OS_
 OS_REGION_NAME=RegionOne
 OS_PROJECT_NAME=admin
 OS_PASSWORD=admin
 OS_AUTH_STRATEGY=keystone
 OS_AUTH_URL=http://172.30.10.70:5000/v2.0
 OS_USERNAME=admin
 OS_TENANT_NAME=admin
 OS_ENDPOINT_TYPE=internalURL
 OS_NO_CACHE=true


Then you may run the test suite by running::

 $ /home/opnfv/repos/functest/docker/run_tests.sh -t <your project>

see `[2]`_ for details.



=========================
How to integrate Functest
=========================

The files of the Functest repository you must modify to integrate Functest are:

 * functest/docker/Dockerfile
 * functest/docker/common.sh
 * functest/docker/requirements.pip
 * functest/docker/run_tests.sh
 * functest/docker/prepare_env.sh
 * functest/config_funtest.yaml


Dockerfile
==========

This file lists the repositories to be cloned in the Functest container. The repositories can be internal or external::

 RUN git clone https://gerrit.opnfv.org/gerrit/<your porject> ${repos_dir}/<your project>


Common.sh
==========

This file can be used to declare the branch and commit  variables of your projects::

 <YOUR_PROJECT>_BRANCH=$(cat $config_file | grep -w <your project>_branch | awk 'END {print $NF}')
 <YOUR_PROJECT>_COMMIT=$(cat $config_file | grep -w <your project>_commit | awk 'END {print $NF}')

 echo "<YOUR_PROJECT>_BRANCH=${<YOUR_PROJECT>_BRANCH}"
 echo "<YOUR_PROJECT>_COMMIT=${<YOUR_PROJECT>_COMMIT}"


requirements.pip
================

This file can be used to preloaded all the needed Python libraries (and avoid that each project does it)
The current libraries used in Functest container are::

 # cat requirements.pip
 pyyaml==3.10
 gitpython==1.0.1
 python-neutronclient==2.6.0
 python-novaclient==2.28.1
 python-glanceclient==1.1.0
 python-cinderclient==1.4.0
 python-ceilometerclient==1.5.1
 python-keystoneclient==1.6.0
 virtualenv==1.11.4
 pexpect==4.0
 requests==2.8.0
 robotframework==2.9.1
 robotframework-requests==0.3.8
 robotframework-sshlibrary==2.1.1
 configObj==5.0.6
 Flask==0.10.1


prepare_env.sh
==============

This script can be adapted if you need to set up a specific environment before running the tests.

run_tests.sh
============

This script is used to run the tests. You must thus complete the cases with you own project::

 ;;
    "promise")
        info "Running PROMISE test case..."
        # TODO
    ;;
    "doctor")
        info "Running Doctor test..."
        python ${FUNCTEST_REPO_DIR}/testcases/features/doctor.py
    ;;
    "<your project>")
        info "Running <your project> test..."
        # your script that launchs your tests...
    ;;

And do not forget to update also the help line::

 -t|--test         run specific set of tests
      <test_name>     one or more of the following: vping,odl,rally,tempest,vims,onos, promise. Separated by comma.


config_funtest.yaml
===================

This file is the main configuration file of Functest. You must add the references to your project::

 general:
    directories:
        dir_repo_<your project>:      /home/opnfv/repos/<your project>
     repositories:
        # branch and commit ID to which the repos will be reset (HEAD)
        <your project>_branch:   master
        <your project>_commit:   latest


==========
References
==========

.. _`[1]`: Functest configuration guide URL
.. _`[2]`: functest user guide URL


OPNFV main site: opnfvmain_.

OPNFV functional test page: opnfvfunctest_.

IRC support chan: #opnfv-testperf

.. _opnfvmain: http://www.opnfv.org
.. _opnfvfunctest: https://wiki.opnfv.org/opnfv_functional_testing
.. _`OpenRC`: http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html
.. _`Rally installation procedure`: https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html
.. _`config_test.py` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.py
.. _`config_functest.yaml` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.yaml

