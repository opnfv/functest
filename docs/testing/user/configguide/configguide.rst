.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

Installation and configuration
==============================

Alpine containers have been introduced in Euphrates.
Alpine allows Functest testing in several very light containers and thanks to
the refactoring on dependency management should allow the creation of light and
fully customized docker images.


Functest Dockers
----------------
Docker images are available on the dockerhub:

  * opnfv/functest-core
  * opnfv/functest-healthcheck
  * opnfv/functest-smoke
  * opnfv/functest-features
  * opnfv/functest-components
  * opnfv/functest-vnf
  * opnfv/functest-parser
  * opnfv/functest-restapi

The tag "opnfv-5.0.0" is the official release image in Euphrates, but you can also pull "euphrates"
tag as it is being maintained by Functest team and might include bugfixes.

The Functest docker container environment can -in principle- be also
used with non-OPNFV official installers (e.g. 'devstack'), with the
**disclaimer** that support for such environments is outside of the
scope and responsibility of the OPNFV project.


Preparing your environment
--------------------------

cat env::

  INSTALLER_TYPE=XXX
  INSTALLER_IP=XXX
  EXTERNAL_NETWORK=XXX
  DEPLOY_SCENARIO=XXX

See section on environment variables for details.

cat openstack.creds::

  export OS_AUTH_URL=XXX
  export OS_USER_DOMAIN_NAME=XXX
  export OS_PROJECT_DOMAIN_NAME=XXX
  export OS_USERNAME=XXX
  export OS_TENANT_NAME=XXX
  export OS_PROJECT_NAME=XXX
  export OS_PASSWORD=XXX
  export OS_VOLUME_API_VERSION=XXX
  export OS_IDENTITY_API_VERSION=XXX
  export OS_IMAGE_API_VERSION=XXX

See section on OpenStack credentials for details.

Create a directory for the different images (attached as a Docker volume)::

  mkdir -p images && wget -q -O- https://git.opnfv.org/functest/plain/functest/ci/download_images.sh?h=stable/euphrates | bash -s -- images && ls -1 images/*

  images/CentOS-7-aarch64-GenericCloud.qcow2
  images/CentOS-7-aarch64-GenericCloud.qcow2.xz
  images/CentOS-7-x86_64-GenericCloud.qcow2
  images/cirros-0.4.0-x86_64-disk.img
  images/cirros-0.4.0-x86_64-lxc.tar.gz
  images/cirros-d161201-aarch64-disk.img
  images/cirros-d161201-aarch64-initramfs
  images/cirros-d161201-aarch64-kernel
  images/cloudify-manager-premium-4.0.1.qcow2
  images/img
  images/trusty-server-cloudimg-amd64-disk1.img
  images/ubuntu-14.04-server-cloudimg-amd64-disk1.img
  images/ubuntu-14.04-server-cloudimg-arm64-uefi1.img
  images/ubuntu-16.04-server-cloudimg-amd64-disk1.img
  images/vyos-1.1.7.img


Testing healthcheck suite
--------------------------

Run healthcheck suite::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/openstack.creds  \
      -v $(pwd)/images:/home/opnfv/functest/images  \
      opnfv/functest-healthcheck

Results shall be displayed as follows::

  +----------------------------+------------------+---------------------+------------------+----------------+
  |         TEST CASE          |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +----------------------------+------------------+---------------------+------------------+----------------+
  |      connection_check      |     functest     |     healthcheck     |      00:02       |      PASS      |
  |         api_check          |     functest     |     healthcheck     |      04:57       |      PASS      |
  |     snaps_health_check     |     functest     |     healthcheck     |      00:51       |      PASS      |
  +----------------------------+------------------+---------------------+------------------+----------------+
  NOTE: the duration is a reference and it might vary depending on your SUT.

Testing smoke suite
-------------------

Run smoke suite::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/openstack.creds  \
      -v $(pwd)/images:/home/opnfv/functest/images  \
      opnfv/functest-smoke

Results shall be displayed as follows::

  +------------------------------+------------------+---------------+------------------+----------------+
  |          TEST CASE           |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +------------------------------+------------------+---------------+------------------+----------------+
  |          vping_ssh           |     functest     |     smoke     |      01:19       |      PASS      |
  |        vping_userdata        |     functest     |     smoke     |      01:56       |      PASS      |
  |     tempest_smoke_serial     |     functest     |     smoke     |      26:30       |      PASS      |
  |         rally_sanity         |     functest     |     smoke     |      19:42       |      PASS      |
  |       refstack_defcore       |     functest     |     smoke     |      22:00       |      PASS      |
  |         snaps_smoke          |     functest     |     smoke     |      41:14       |      PASS      |
  |             odl              |     functest     |     smoke     |      00:16       |      PASS      |
  |         odl_netvirt          |     functest     |     smoke     |      00:00       |      SKIP      |
  |             fds              |     functest     |     smoke     |      00:00       |      SKIP      |
  +------------------------------+------------------+---------------+------------------+----------------+
  Note: if the scenario does not support some tests, they are indicated as SKIP.
  See User guide for details.

Testing features suite
----------------------

Run features suite::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/openstack.creds  \
      -v $(pwd)/images:/home/opnfv/functest/images  \
      opnfv/functest-features

Results shall be displayed as follows::

  +---------------------------+--------------------------+------------------+------------------+----------------+
  |         TEST CASE         |         PROJECT          |       TIER       |     DURATION     |     RESULT     |
  +---------------------------+--------------------------+------------------+------------------+----------------+
  |          promise          |         promise          |     features     |      00:00       |      SKIP      |
  |           bgpvpn          |          sdnvpn          |     features     |      00:00       |      SKIP      |
  |       security_scan       |     securityscanning     |     features     |      00:00       |      SKIP      |
  |      functest-odl-sfc     |           sfc            |     features     |      00:00       |      SKIP      |
  |      domino-multinode     |          domino          |     features     |      00:00       |      SKIP      |
  |     barometercollectd     |        barometer         |     features     |      00:00       |      SKIP      |
  +---------------------------+--------------------------+------------------+------------------+----------------+
  Note: if the scenario does not support some tests, they are indicated as SKIP.
  See User guide for details.

Testing components suite
------------------------

Run components suite::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/openstack.creds  \
      -v $(pwd)/images:/home/opnfv/functest/images  \
      opnfv/functest-components

Results shall be displayed as follows::

  +-------------------------------+------------------+--------------------+------------------+----------------+
  |           TEST CASE           |     PROJECT      |        TIER        |     DURATION     |     RESULT     |
  +-------------------------------+------------------+--------------------+------------------+----------------+
  |     tempest_full_parallel     |     functest     |     components     |      102:48      |      PASS      |
  |           rally_full          |     functest     |     components     |      160:58      |      PASS      |
  +-------------------------------+------------------+--------------------+------------------+----------------+

Testing vnf suite
-----------------

Run vnf suite::

sudo docker run --env-file env \
    -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/openstack.creds  \
    -v $(pwd)/images:/home/opnfv/functest/images  \
    opnfv/functest-vnf

Results shall be displayed as follows::

  +---------------------------------+------------------+--------------+------------------+----------------+
  |            TEST CASE            |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +---------------------------------+------------------+--------------+------------------+----------------+
  |           cloudify_ims          |     functest     |     vnf      |      21:25       |      PASS      |
  |        orchestra_openims        |     functest     |     vnf      |      11:02       |      FAIL      |
  |     orchestra_clearwaterims     |     functest     |     vnf      |      09:13       |      FAIL      |
  +---------------------------------+------------------+--------------+------------------+----------------+


Environment variables
=====================

Several environement variables may be specified:
  * INSTALLER_TYPE=(apex|compass|daisy|fuel|joid)
  * INSTALLER_IP=<Specific IP Address>
  * DEPLOY_SCENARIO=<vim>-<controller>-<nfv_feature>-<ha_mode>


INSTALLER IP may be required by some test cases like SFC or Barometer in order
to access the installer node and the deployment.

The format for the DEPLOY_SCENARIO env variable can be described as follows:
  * vim: (os|k8s) = OpenStack or Kubernetes
  * controller is one of ( nosdn | odl )
  * nfv_feature is one or more of ( ovs | kvm | sfc | bgpvpn | nofeature )
  * ha_mode (high availability) is one of ( ha | noha )

If several features are pertinent then use the underscore character '_' to
separate each feature (e.g. ovs_kvm). 'nofeature' indicates that no OPNFV
feature is deployed.

The list of supported scenarios per release/installer is indicated in the
release note.

**NOTE:** The scenario name is mainly used to automatically detect
if a test suite is runnable or not (e.g. it will prevent ODL test suite to be
run on 'nosdn' scenarios). If not set, Functest will try to run the default test
cases that might not include SDN controller or a specific feature

**NOTE:** An HA scenario means that 3 OpenStack controller nodes are
deployed. It does not necessarily mean that the whole system is HA. See
installer release notes for details.

Finally, three additional environment variables can also be passed in
to the Functest Docker Container, using the -e
"<EnvironmentVariable>=<Value>" mechanism. The first two parameters are
only relevant to Jenkins CI invoked testing and **should not be used**
when performing manual test scenarios:

  * NODE_NAME = <Test POD Name>
  * BUILD_TAG = <Jenkins Build Tag>
  * CI_DEBUG = <DebugTraceValue>

where:

  * <Test POD Name> = Symbolic name of the POD where the tests are run.
                      Visible in test results files, which are stored
                      to the database. This option is only used when
                      tests are activated under Jenkins CI control.
                      It indicates the POD/hardware where the test has
                      been run. If not specified, then the POD name is
                      defined as "Unknown" by default.
                      DO NOT USE THIS OPTION IN MANUAL TEST SCENARIOS.
  * <Jenkins Build tag> = Symbolic name of the Jenkins Build Job.
                         Visible in test results files, which are stored
                         to the database. This option is only set when
                         tests are activated under Jenkins CI control.
                         It enables the correlation of test results,
                         which are independently pushed to the results database
                         from different Jenkins jobs.
                         DO NOT USE THIS OPTION IN MANUAL TEST SCENARIOS.
  * <DebugTraceValue> = "true" or "false"
                       Default = "false", if not specified
                       If "true" is specified, then additional debug trace
                       text can be sent to the test results file / log files
                       and also to the standard console output.


Openstack credentials
=====================
OpenStack credentials are mandatory and must be provided to Functest.
When running the command "functest env prepare", the framework  will
automatically look for the Openstack credentials file
"/home/opnfv/functest/conf/openstack.creds" and will exit with
error if it is not present or is empty.

There are 2 ways to provide that file:

  * by using a Docker volume with -v option when creating the Docker container.
    This is referred to in docker documentation as "Bind Mounting".
    See the usage of this parameter in the following chapter.
  * or creating manually the file '/home/opnfv/functest/conf/openstack.creds'
    inside the running container and pasting the credentials in it. Consult
    your installer guide for further details. This is however not
    instructed in this document.

In proxified environment you may need to change the credentials file.
There are some tips in chapter: `Proxy support`_

SSL Support
-----------
If you need to connect to a server that is TLS-enabled (the auth URL
begins with "https") and it uses a certificate from a private CA or a
self-signed certificate, then you will need to specify the path to an
appropriate CA certificate to use, to validate the server certificate
with the environment variable OS_CACERT::

  echo $OS_CACERT
  /etc/ssl/certs/ca.crt

However, this certificate does not exist in the container by default.
It has to be copied manually from the OpenStack deployment. This can be
done in 2 ways:

  #. Create manually that file and copy the contents from the OpenStack
     controller.
  #. (Recommended) Add the file using a Docker volume when starting the
     container::

       -v <path_to_your_cert_file>:/etc/ssl/certs/ca.cert

You might need to export OS_CACERT environment variable inside the
credentials file::

  export OS_CACERT=/etc/ssl/certs/ca.crt

Certificate verification can be turned off using OS_INSECURE=true. For
example, Fuel uses self-signed cacerts by default, so an pre step would
be::

  export OS_INSECURE=true

Functest docker container directory structure
=============================================
Inside the Functest docker container, the following directory structure
should now be in place::

  `--
    |- home
    |   |-- opnfv
    |   |     `- functest
    |   |          |-- conf
    |   |          `-- results
    |    `-- repos
    |       `-- vnfs
    |- src
    |   |-- tempest
    |   |-- vims-test
    |   |-- odl_test
    |   `-- fds
    `- usr
        `- lib
           `- python2.7
              `- site-packages
                 `- functest
                      |-- ...

Underneath the '/home/opnfv/functest' directory, the Functest docker container
includes two main directories:

  * The **conf** directory stores configuration files (e.g. the
    OpenStack creds are stored in path '/home/opnfv/functest/conf/openstack.creds'),
  * the **results** directory stores some temporary result log files

src and repos directories are used to host third party code used for the tests.

The structure of functest repo can be described as follows::

  |-- INFO
  |-- LICENSE
  |-- api
  |  `-- apidoc
  |-- build.sh
  |-- commons
  |-- docker
  |  |-- components
  |  |-- core
  |  |-- features
  |  |-- healthcheck
  |  |-- smoke
  |  |-- vnf
  |  |-- parser
  |  |-- restapi
  |  |-- thirdparty-requirements.txt
  |-- docs
  |  |-- com
  |  |-- images
  |  |-- release
  |  |  `-- release-notes
  |  |-- results
  |  | testing
  |  |  |-- developer
  |  |    `-- user
  |  |      |-- configguide
  |  |      `-- userguide
  `-- functest
    |-- api
    |  |-- base.py
    |  |-- server.py
    |  |-- urls.py
    |  |-- common
    |  |  |-- api_utils.py
    |  |  |-- thread.py
    |  `-- resources
    |     `-- v1
    |        |-- creds.py
    |        |-- envs.py
    |        |-- testcases.py
    |        |-- tiers.py
    |        |-- tasks.py
    |  `-- database
    |     |-- db.py
    |     `-- v1
    |        |-- handlers.py
    |        |-- models.py
    |  `-- swagger
    |-- ci
    │   |-- check_deployment.py
    │   |-- config_aarch64_patch.yaml
    │   |-- config_functest.yaml
    │   |-- config_patch.yaml
    │   |-- download_images.sh
    │   |-- logging.ini
    │   |-- rally_aarch64_patch.conf
    │   |-- run_tests.py
    │   |-- testcases.yaml
    │   |-- tier_builder.py
    │   |-- tier_handler.py
    |-- cli
    │   |-- cli_base.py
    │   |-- commands
    │   │   |-- cli_env.py
    │   │   |-- cli_os.py
    │   │   |-- cli_testcase.py
    │   │   |-- cli_tier.py
    │   |-- functest-complete.sh
    |-- core
    │   |-- feature.py
    │   |-- robotframework.py
    │   |-- testcase.py
    │   |-- unit.py
    │   |-- vnf.py
    |-- energy
    │   |-- energy.py
    |-- opnfv_tests
    │   `-- openstack
    │       |-- rally
    │       |-- refstack_client
    │       |-- snaps
    │       |-- tempest
    │       |-- vping
    │   `-- sdn
    │   │    `-- odl
    │   `-- vnf
    │       |-- ims
    │       `-- router
    |-- tests
    │   `-- unit
    │       |-- ci
    │       |-- cli
    │       |-- core
    │       |-- energy
    │       |-- features
    │       |-- odl
    │       |-- openstack
    │       |-- opnfv_tests
    │       |-- test_utils.py
    │       |-- utils
    │       `-- vnf
    |-- utils
    |    |-- config.py
    |    |-- constants.py
    |    |-- decorators.py
    |    |-- env.py
    |    |-- functest_utils.py
    |    |-- functest_vacation.py
    |    |-- openstack_clean.py
    |    |-- openstack_tacker.py
    |    `-- openstack_utils.py
  |-- requirements.txt
  |-- setup.cfg
  |-- setup.py
  |-- test-requirements.txt
  |-- tox.ini
  |-- upper-constraints.txt

  (Note: All *.pyc files removed from above list for brevity...)

We may distinguish several directories, the first level has 5 directories:

* **api**: This directory is dedicated to the API (framework) documentations.
* **commons**: This directory is dedicated for storage of traffic profile or
  any other test inputs that could be reused by any test project.
* **docker**: This directory includes the needed files and tools to
  build the Functest Docker images.
* **docs**: This directory includes documentation: Release Notes,
  User Guide, Configuration Guide and Developer Guide.
* **functest**: This directory contains all the code needed to run
  functest internal cases and OPNFV onboarded feature or VNF test cases.

Functest directory has 7 sub-directories, which is located under
/usr/lib/python2.7/site-packages/functest:
  * **api**: This directory is dedicated for the internal Functest API.
  * **ci**: This directory contains test structure definition files
    (e.g <filename>.yaml) and bash shell/python scripts used to
    configure and execute Functional tests. The test execution script
    can be executed under the control of Jenkins CI jobs.
  * **cli**: This directory holds the python based Functest CLI utility
    source code, which is based on the Python 'click' framework.
  * **core**: This directory holds the python based Functest core
      source code. Three abstraction classes have been created to ease
      the integration of internal, feature or vnf cases.
  * **opnfv_tests**: This directory includes the scripts required by
    Functest internal test cases and other feature projects test cases.
  * **tests**: This directory includes the functest unit tests.
  * **utils**: this directory holds Python source code for some general
    purpose helper utilities, which testers can also re-use in their
    own test code. See for an example the Openstack helper utility:
    'openstack_utils.py'.


Logs
====
By default all the logs are put un /home/opnfv/functest/results/functest.log.
If you want to have more logs in console, you may edit the logging.ini file
manually.
Connect on the docker then edit the file located in
/usr/lib/python2.7/site-packages/functest/ci/logging.ini

Change wconsole to console in the desired module to get more traces.


Configuration
=============

You may also directly modify the python code or the configuration file (e.g.
testcases.yaml used to declare test constraints) under
/usr/lib/python2.7/site-packages/functest


Tips
====

Docker
------
When typing **exit** in the container prompt, this will cause exiting
the container and probably stopping it. When stopping a running Docker
container all the changes will be lost, there is a keyboard shortcut
to quit the container without stopping it: <CTRL>-P + <CTRL>-Q. To
reconnect to the running container **DO NOT** use the *run* command
again (since it will create a new container), use the *exec* or *attach*
command instead::

  docker ps  # <check the container ID from the output>
  docker exec -ti <CONTAINER_ID> /bin/bash

There are other useful Docker commands that might be needed to manage possible
issues with the containers.

List the running containers::

  docker ps

List all the containers including the stopped ones::

  docker ps -a

Start a stopped container named "FunTest"::

  docker start FunTest

Attach to a running container named "StrikeTwo"::

  docker attach StrikeTwo

It is useful sometimes to remove a container if there are some problems::

  docker rm <CONTAINER_ID>

Use the *-f* option if the container is still running, it will force to
destroy it::

  docker rm -f <CONTAINER_ID>

Check the Docker documentation [`dockerdocs`_] for more information.


Checking Openstack and credentials
----------------------------------
It is recommended and fairly straightforward to check that Openstack
and credentials are working as expected.

Once the credentials are there inside the container, they should be
sourced before running any Openstack commands::

  source /home/opnfv/functest/conf/openstack.creds

After this, try to run any OpenStack command to see if you get any
output, for instance::

  openstack user list

This will return a list of the actual users in the OpenStack
deployment. In any other case, check that the credentials are sourced::

  env|grep OS_

This command must show a set of environment variables starting with
*OS_*, for example::

  OS_REGION_NAME=RegionOne
  OS_USER_DOMAIN_NAME=Default
  OS_PROJECT_NAME=admin
  OS_AUTH_VERSION=3
  OS_IDENTITY_API_VERSION=3
  OS_PASSWORD=da54c27ae0d10dfae5297e6f0d6be54ebdb9f58d0f9dfc
  OS_AUTH_URL=http://10.1.0.9:5000/v3
  OS_USERNAME=admin
  OS_TENANT_NAME=admin
  OS_ENDPOINT_TYPE=internalURL
  OS_INTERFACE=internalURL
  OS_NO_CACHE=1
  OS_PROJECT_DOMAIN_NAME=Default


If the OpenStack command still does not show anything or complains
about connectivity issues, it could be due to an incorrect url given to
the OS_AUTH_URL environment variable. Check the deployment settings.

Proxy support
-------------
If your Jumphost node is operating behind a http proxy, then there are
2 places where some special actions may be needed to make operations
succeed:

  #. Initial installation of docker engine First, try following the
     official Docker documentation for Proxy settings. Some issues were
     experienced on CentOS 7 based Jumphost. Some tips are documented
     in section: `Docker Installation on CentOS behind http proxy`_
     below.

If that is the case, make sure the resolv.conf and the needed
http_proxy and https_proxy environment variables, as well as the
'no_proxy' environment variable are set correctly::

  # Make double sure that the 'no_proxy=...' line in the
  # 'openstack.creds' file is commented out first. Otherwise, the
  # values set into the 'no_proxy' environment variable below will
  # be ovewrwritten, each time the command
  # 'source ~/functest/conf/openstack.creds' is issued.

  cd ~/functest/conf/
  sed -i 's/export no_proxy/#export no_proxy/' openstack.creds
  source ./openstack.creds

  # Next calculate some IP addresses for which http_proxy
  # usage should be excluded:

  publicURL_IP=$(echo $OS_AUTH_URL | grep -Eo "([0-9]+\.){3}[0-9]+")

  adminURL_IP=$(openstack catalog show identity | \
  grep adminURL | grep -Eo "([0-9]+\.){3}[0-9]+")

  export http_proxy="<your http proxy settings>"
  export https_proxy="<your https proxy settings>"
  export no_proxy="127.0.0.1,localhost,$publicURL_IP,$adminURL_IP"

  # Ensure that "git" uses the http_proxy
  # This may be needed if your firewall forbids SSL based git fetch
  git config --global http.sslVerify True
  git config --global http.proxy <Your http proxy settings>

For example, try to use the **nc** command from inside the functest
docker container::

  nc -v opnfv.org 80
  Connection to opnfv.org 80 port [tcp/http] succeeded!

  nc -v opnfv.org 443
  Connection to opnfv.org 443 port [tcp/https] succeeded!

Note: In a Jumphost node based on the CentOS family OS, the **nc**
commands might not work. You can use the **curl** command instead.

  curl http://www.opnfv.org:80

  <HTML><HEAD><meta http-equiv="content-type"
  .
  .
  </BODY></HTML>

  curl https://www.opnfv.org:443

  <HTML><HEAD><meta http-equiv="content-type"
  .
  .
  </BODY></HTML>

  (Ignore the content. If command returns a valid HTML page, it proves
  the connection.)

Docker Installation on CentOS behind http proxy
-----------------------------------------------
This section is applicable for CentOS family OS on Jumphost which
itself is behind a proxy server. In that case, the instructions below
should be followed **before** installing the docker engine::

  1) # Make a directory '/etc/systemd/system/docker.service.d'
     # if it does not exist
     sudo mkdir /etc/systemd/system/docker.service.d

  2) # Create a file called 'env.conf' in that directory with
     # the following contents:
     [Service]
     EnvironmentFile=-/etc/sysconfig/docker

  3) # Set up a file called 'docker' in directory '/etc/sysconfig'
     # with the following contents:
     HTTP_PROXY="<Your http proxy settings>"
     HTTPS_PROXY="<Your https proxy settings>"
     http_proxy="${HTTP_PROXY}"
     https_proxy="${HTTPS_PROXY}"

  4) # Reload the daemon
     systemctl daemon-reload

  5) # Sanity check - check the following docker settings:
     systemctl show docker | grep -i env

     Expected result:
     ----------------
     EnvironmentFile=/etc/sysconfig/docker (ignore_errors=yes)
     DropInPaths=/etc/systemd/system/docker.service.d/env.conf

Now follow the instructions in [`Install Docker on CentOS`_] to download
and install the **docker-engine**. The instructions conclude with a
"test pull" of a sample "Hello World" docker container. This should now
work with the above pre-requisite actions.


.. _`[4]`: http://docs.opnfv.org/en/latest/submodules/functest/docs/testing/user/configguide/index.html
.. _`dockerdocs`: https://docs.docker.com/
.. _`Proxy`: https://docs.docker.com/engine/admin/systemd/#http-proxy
.. _`Install Docker on CentOS`: https://docs.docker.com/engine/installation/linux/centos/
.. _`Functest User Guide`: http://docs.opnfv.org/en/stable-danube/submodules/functest/docs/testing/user/userguide/index.html
.. _`images/CentOS-7-x86_64-GenericCloud.qcow2` http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
.. _`images/cirros-0.4.0-x86_64-disk.img` https://cloud-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img
.. _`images/ubuntu-14.04-server-cloudimg-amd64-disk1.img` https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
