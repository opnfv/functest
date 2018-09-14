.. SPDX-License-Identifier: CC-BY-4.0

Installation and configuration
==============================

Alpine containers have been introduced in Euphrates.
Alpine allows Functest testing in several very light containers and thanks to
the refactoring on dependency management should allow the creation of light and
fully customized docker images.


Functest Dockers for OpenStack deployment
-----------------------------------------
Docker images are available on the dockerhub:

  * opnfv/functest-core
  * opnfv/functest-healthcheck
  * opnfv/functest-smoke
  * opnfv/functest-benchmarking
  * opnfv/functest-features
  * opnfv/functest-components
  * opnfv/functest-vnf


Preparing your environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

cat env::

  EXTERNAL_NETWORK=XXX
  DEPLOY_SCENARIO=XXX  # if not os-nosdn-nofeature-noha scenario
  NAMESERVER=XXX  # if not 8.8.8.8

See section on environment variables for details.

cat env_file::

  export OS_AUTH_URL=XXX
  export OS_USER_DOMAIN_NAME=XXX
  export OS_PROJECT_DOMAIN_NAME=XXX
  export OS_USERNAME=XXX
  export OS_PROJECT_NAME=XXX
  export OS_PASSWORD=XXX
  export OS_IDENTITY_API_VERSION=3

See section on OpenStack credentials for details.

Create a directory for the different images (attached as a Docker volume)::

  mkdir -p images && wget -q -O- https://git.opnfv.org/functest/plain/functest/ci/download_images.sh?h=stable/fraser | bash -s -- images && ls -1 images/*

  images/CentOS-7-aarch64-GenericCloud.qcow2
  images/CentOS-7-aarch64-GenericCloud.qcow2.xz
  images/CentOS-7-x86_64-GenericCloud.qcow2
  images/cirros-0.4.0-x86_64-disk.img
  images/cirros-0.4.0-x86_64-lxc.tar.gz
  images/cloudify-manager-premium-4.0.1.qcow2
  images/shaker-image-arm64.qcow2
  images/shaker-image.qcow
  images/ubuntu-14.04-server-cloudimg-amd64-disk1.img
  images/ubuntu-14.04-server-cloudimg-arm64-uefi1.img
  images/ubuntu-16.04-server-cloudimg-amd64-disk1.img
  images/vyos-1.1.7.img

Testing healthcheck suite
^^^^^^^^^^^^^^^^^^^^^^^^^

Run healthcheck suite::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
      -v $(pwd)/images:/home/opnfv/functest/images \
      opnfv/functest-healthcheck

Results shall be displayed as follows::

  +----------------------------+------------------+---------------------+------------------+----------------+
  |         TEST CASE          |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +----------------------------+------------------+---------------------+------------------+----------------+
  |      connection_check      |     functest     |     healthcheck     |      00:09       |      PASS      |
  |       tenantnetwork1       |     functest     |     healthcheck     |      00:14       |      PASS      |
  |       tenantnetwork2       |     functest     |     healthcheck     |      00:11       |      PASS      |
  |          vmready1          |     functest     |     healthcheck     |      00:19       |      PASS      |
  |          vmready2          |     functest     |     healthcheck     |      00:16       |      PASS      |
  |         singlevm1          |     functest     |     healthcheck     |      00:41       |      PASS      |
  |         singlevm2          |     functest     |     healthcheck     |      00:36       |      PASS      |
  |         vping_ssh          |     functest     |     healthcheck     |      00:46       |      PASS      |
  |       vping_userdata       |     functest     |     healthcheck     |      00:41       |      PASS      |
  |        cinder_test         |     functest     |     healthcheck     |      01:18       |      PASS      |
  |         api_check          |     functest     |     healthcheck     |      10:33       |      PASS      |
  |     snaps_health_check     |     functest     |     healthcheck     |      00:44       |      PASS      |
  |            odl             |     functest     |     healthcheck     |      00:00       |      SKIP      |
  +----------------------------+------------------+---------------------+------------------+----------------+

NOTE: the duration is a reference and it might vary depending on your SUT.

Testing smoke suite
^^^^^^^^^^^^^^^^^^^

Run smoke suite::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
      -v $(pwd)/images:/home/opnfv/functest/images \
      opnfv/functest-smoke

Results shall be displayed as follows::

  +------------------------------------+------------------+---------------+------------------+----------------+
  |             TEST CASE              |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +------------------------------------+------------------+---------------+------------------+----------------+
  |           tempest_smoke            |     functest     |     smoke     |      06:13       |      PASS      |
  |     neutron-tempest-plugin-api     |     functest     |     smoke     |      09:32       |      PASS      |
  |            rally_sanity            |     functest     |     smoke     |      29:34       |      PASS      |
  |             rally_jobs             |     functest     |     smoke     |      24:02       |      PASS      |
  |          refstack_defcore          |     functest     |     smoke     |      13:07       |      PASS      |
  |              patrole               |     functest     |     smoke     |      05:17       |      PASS      |
  |            snaps_smoke             |     functest     |     smoke     |      90:13       |      PASS      |
  |           neutron_trunk            |     functest     |     smoke     |      00:00       |      SKIP      |
  |         networking-bgpvpn          |     functest     |     smoke     |      00:00       |      SKIP      |
  |           networking-sfc           |     functest     |     smoke     |      00:00       |      SKIP      |
  |              barbican              |     functest     |     smoke     |      05:01       |      PASS      |
  +------------------------------------+------------------+---------------+------------------+----------------+

Note: if the scenario does not support some tests, they are indicated as SKIP.
See User guide for details.

Testing benchmarking suite
^^^^^^^^^^^^^^^^^^^^^^^^^^

Run benchmarking suite::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
      -v $(pwd)/images:/home/opnfv/functest/images \
      opnfv/functest-benchmarking

Results shall be displayed as follows::

  +-------------------+------------------+----------------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +-------------------+------------------+----------------------+------------------+----------------+
  |        vmtp       |     functest     |     benchmarking     |      18:43       |      PASS      |
  |       shaker      |     functest     |     benchmarking     |      29:45       |      PASS      |
  +-------------------+------------------+----------------------+------------------+----------------+

Note: if the scenario does not support some tests, they are indicated as SKIP.
See User guide for details.

Testing features suite
^^^^^^^^^^^^^^^^^^^^^^

Run features suite::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
      -v $(pwd)/images:/home/opnfv/functest/images \
      opnfv/functest-features

Results shall be displayed as follows::

  +-----------------------------+------------------------+------------------+------------------+----------------+
  |          TEST CASE          |        PROJECT         |       TIER       |     DURATION     |     RESULT     |
  +-----------------------------+------------------------+------------------+------------------+----------------+
  |     doctor-notification     |         doctor         |     features     |      00:00       |      SKIP      |
  |            bgpvpn           |         sdnvpn         |     features     |      00:00       |      SKIP      |
  |       functest-odl-sfc      |          sfc           |     features     |      00:00       |      SKIP      |
  |      barometercollectd      |       barometer        |     features     |      00:00       |      SKIP      |
  |             fds             |     fastdatastacks     |     features     |      00:00       |      SKIP      |
  |             vgpu            |        functest        |     features     |      00:00       |      SKIP      |
  |         stor4nfv_os         |        stor4nfv        |     features     |      00:00       |      SKIP      |
  +-----------------------------+------------------------+------------------+------------------+----------------+

Note: if the scenario does not support some tests, they are indicated as SKIP.
See User guide for details.

Testing components suite
^^^^^^^^^^^^^^^^^^^^^^^^

Run components suite::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
      -v $(pwd)/images:/home/opnfv/functest/images \
      opnfv/functest-components

Results shall be displayed as follows::

  +--------------------------+------------------+--------------------+------------------+----------------+
  |        TEST CASE         |     PROJECT      |        TIER        |     DURATION     |     RESULT     |
  +--------------------------+------------------+--------------------+------------------+----------------+
  |       tempest_full       |     functest     |     components     |      49:51       |      PASS      |
  |     tempest_scenario     |     functest     |     components     |      18:50       |      PASS      |
  |        rally_full        |     functest     |     components     |      167:13      |      PASS      |
  +--------------------------+------------------+--------------------+------------------+----------------+

Testing vnf suite
^^^^^^^^^^^^^^^^^

Run vnf suite::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
      -v $(pwd)/images:/home/opnfv/functest/images \
      opnfv/functest-vnf

Results shall be displayed as follows::

  +----------------------+------------------+--------------+------------------+----------------+
  |      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +----------------------+------------------+--------------+------------------+----------------+
  |       cloudify       |     functest     |     vnf      |      04:05       |      PASS      |
  |     cloudify_ims     |     functest     |     vnf      |      24:07       |      PASS      |
  |       heat_ims       |     functest     |     vnf      |      18:15       |      PASS      |
  |     vyos_vrouter     |     functest     |     vnf      |      15:48       |      PASS      |
  |       juju_epc       |     functest     |     vnf      |      29:38       |      PASS      |
  +----------------------+------------------+--------------+------------------+----------------+

Functest Dockers for Kubernetes deployment
------------------------------------------
Docker images are available on the dockerhub:

  * opnfv/functest-kubernetes-core
  * opnfv/functest-kubernetest-healthcheck
  * opnfv/functest-kubernetest-smoke
  * opnfv/functest-kubernetest-features

Preparing your environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

cat env::

  DEPLOY_SCENARIO=k8s-XXX

Testing healthcheck suite
^^^^^^^^^^^^^^^^^^^^^^^^^

Run healthcheck suite::

  sudo docker run -it --env-file env \
      -v $(pwd)/config:/root/.kube/config \
      opnfv/functest-kubernetes-healthcheck

A config file in the current dir 'config' is also required, which should be
volume mapped to ~/.kube/config inside kubernetes container.

Results shall be displayed as follows::

  +-------------------+------------------+---------------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +-------------------+------------------+---------------------+------------------+----------------+
  |     k8s_smoke     |     functest     |     healthcheck     |      02:27       |      PASS      |
  +-------------------+------------------+---------------------+------------------+----------------+

Testing smoke suite
^^^^^^^^^^^^^^^^^^^

Run smoke suite::

  sudo docker run -it --env-file env \
      -v $(pwd)/config:/root/.kube/config \
      opnfv/functest-kubernetes-smoke

Results shall be displayed as follows::

  +-------------------------+------------------+---------------+------------------+----------------+
  |        TEST CASE        |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +-------------------------+------------------+---------------+------------------+----------------+
  |     k8s_conformance     |     functest     |     smoke     |      57:14       |      PASS      |
  +-------------------------+------------------+---------------+------------------+----------------+

Testing features suite
^^^^^^^^^^^^^^^^^^^^^^

Run features suite::

  sudo docker run -it --env-file env \
      -v $(pwd)/config:/root/.kube/config \
      opnfv/functest-kubernetes-features

Results shall be displayed as follows::

  +----------------------+------------------+------------------+------------------+----------------+
  |      TEST CASE       |     PROJECT      |       TIER       |     DURATION     |     RESULT     |
  +----------------------+------------------+------------------+------------------+----------------+
  |     stor4nfv_k8s     |     stor4nfv     |     stor4nfv     |      00:00       |      SKIP      |
  |      clover_k8s      |      clover      |      clover      |      00:00       |      SKIP      |
  +----------------------+------------------+------------------+------------------+----------------+

Environment variables
=====================

Several environement variables may be specified:

  * INSTALLER_IP=<Specific IP Address>
  * DEPLOY_SCENARIO=<vim>-<controller>-<nfv_feature>-<ha_mode>
  * NAMESERVER=XXX  # if not 8.8.8.8
  * VOLUME_DEVICE_NAME=XXX  # if not vdb
  * EXTERNAL_NETWORK=XXX # if not first network with router:external=True
  * NEW_USER_ROLE=XXX # if not member

INSTALLER_IP is required by Barometer in order to access the installer node and
the deployment.

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
run on 'nosdn' scenarios). If not set, Functest will try to run the default
test cases that might not include SDN controller or a specific feature.

**NOTE:** An HA scenario means that 3 OpenStack controller nodes are
deployed. It does not necessarily mean that the whole system is HA. See
installer release notes for details.

Finally, three additional environment variables can also be passed in
to the Functest Docker Container, using the -e
"<EnvironmentVariable>=<Value>" mechanism. The first two parameters are
only relevant to Jenkins CI invoked testing and **should not be used**
when performing manual test scenarios:

  * INSTALLER_TYPE=(apex|compass|daisy|fuel)
  * NODE_NAME=<Test POD Name>
  * BUILD_TAG=<Jenkins Build Tag>

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


Openstack credentials
=====================
OpenStack credentials are mandatory and must be provided to Functest.
When running the command "functest env prepare", the framework  will
automatically look for the Openstack credentials file
"/home/opnfv/functest/conf/env_file" and will exit with
error if it is not present or is empty.

There are 2 ways to provide that file:

  * by using a Docker volume with -v option when creating the Docker container.
    This is referred to in docker documentation as "Bind Mounting".
    See the usage of this parameter in the following chapter.
  * or creating manually the file '/home/opnfv/functest/conf/env_file'
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


Logs
====
By default all the logs are put un /home/opnfv/functest/results/functest.log.
If you want to have more logs in console, you may edit the logging.ini file
manually.
Connect on the docker then edit the file located in
/usr/lib/python2.7/site-packages/xtesting/ci/logging.ini

Change wconsole to console in the desired module to get more traces.


Configuration
=============

You may also directly modify the python code or the configuration file (e.g.
testcases.yaml used to declare test constraints) under
/usr/lib/python2.7/site-packages/xtesting and
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

  source /home/opnfv/functest/conf/env_file

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

.. _`Proxy support`:

Proxy support
-------------
If your Jumphost node is operating behind a http proxy, then there are
2 places where some special actions may be needed to make operations
succeed:

  #. Initial installation of docker engine First, try following the
     official Docker documentation for Proxy settings. Some issues were
     experienced on CentOS 7 based Jumphost. Some tips are documented
     in section: :ref:`Docker Installation on CentOS behind http proxy`
     below.

If that is the case, make sure the resolv.conf and the needed
http_proxy and https_proxy environment variables, as well as the
'no_proxy' environment variable are set correctly::

  # Make double sure that the 'no_proxy=...' line in the
  # 'env_file' file is commented out first. Otherwise, the
  # values set into the 'no_proxy' environment variable below will
  # be ovewrwritten, each time the command
  # 'source ~/functest/conf/env_file' is issued.

  cd ~/functest/conf/
  sed -i 's/export no_proxy/#export no_proxy/' env_file
  source ./env_file

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

.. _`Docker Installation on CentOS behind http proxy`:

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


.. _`[4]`: :ref:`<functest-install-guide>`
.. _`dockerdocs`: https://docs.docker.com/
.. _`Proxy`: https://docs.docker.com/engine/admin/systemd/#http-proxy
.. _`Install Docker on CentOS`: https://docs.docker.com/engine/installation/linux/centos/
.. _`Functest User Guide`: http://docs.opnfv.org/en/stable-danube/submodules/functest/docs/testing/user/userguide/index.html
.. _`images/CentOS-7-x86_64-GenericCloud.qcow2`: https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
.. _`images/cirros-0.4.0-x86_64-disk.img`: http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
.. _`images/ubuntu-14.04-server-cloudimg-amd64-disk1.img`: https://cloud-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img
