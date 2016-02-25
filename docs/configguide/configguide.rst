.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


Preparing the Docker container
------------------------------

Pull the Functest Docker image from the Docker hub::

  docker pull opnfv/functest:brahmaputra.1.0


Check that the image is available::

  docker images

Run the docker container giving the environment variables:

 * INSTALLER_TYPE : possible values are "apex", "compass", "fuel" or "joid".
 * INSTALLER_IP : IP of the installer node/VM.

Functest may need to know the IP of the installer to retrieve the credentials from
the installer node/VM or even from the actual controllers.

The minimum command to create the Functest Docker container can be described as
follows::

  docker run -it -e "INSTALLER_IP=10.20.0.2" -e "INSTALLER_TYPE=fuel" opnfv/functest:brahmaputra.1.0 /bin/bash

Optionally, it is possible to precise the container name through the option
--name::

  docker run --name "CONTAINER_NAME" -it -e "INSTALLER_IP=10.20.0.2" -e "INSTALLER_TYPE=fuel" opnfv/functest:brahmaputra.1.0 /bin/bash

It is also possible to to indicate the path of the OpenStack credentials using -v::

  docker run  -it -e "INSTALLER_IP=10.20.0.2" -e "INSTALLER_TYPE=fuel" -v <path_to_your_local_creds_file>:/home/opnfv/functest/conf/openstack.creds opnfv/functest:brahmaputra.1.0 /bin/bash

The local file will be mounted in the container under
/home/opnfv/functest/conf/openstack.creds

If the intention is to run Functest against any of the supported OPNFV scenarios,
it is recommended to include also the environment variable **DEPLOY_SCENARIO**,
For instance::

  docker run -it -e "INSTALLER_IP=10.20.0.2" -e "INSTALLER_TYPE=fuel" -e "DEPLOY_SCENARIO=os-odl_l2-nofeature-ha" opnfv/functest:brahmaputra.1.0 /bin/bash

Inside the container, the following directory structure should be in place::

  `-- home
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
            |-- promise
            |-- rally
            |-- releng
            `-- vims-test


Basically the container includes:

  * Functest directory to store the configuration (the OpenStack creds are stored
    in /home/opngb/functest/conf/openstack.creds), the data (cirros image needed for
    some tests), results (some temporary result logs may be stored here)
  * Repositories: the functest repository will be used to prepare the
    environment and run the tests. Other repositories are used for the installation
    of the needed tooling (e.g. rally) and/or the retrieval of feature projects
    scenarios (e.g. promise)

The structure under the Functest repository can be described as follows::

  .
    |-- INFO
    |-- LICENSE
    |-- commons
    |   |-- ims
    |   |-- mobile
    |   `-- traffic-profile-guidelines.rst
    |-- docker
    |   |-- Dockerfile
    |   |-- common.sh
    |   |-- prepare_env.sh
    |   |-- requirements.pip
    |   `-- run_tests.sh
    |-- docs
    |   |-- configguide
    |   |-- devguide
    |   |-- images
    |   |-- results
    |   `-- userguide
    `-- testcases
        |-- Controllers
        |-- features
        |-- tests
        |-- VIM
        |-- vIMS
        |-- vPing
        |-- __init__.py
        |-- config_functest.py
        |-- config_functest.yaml
        `-- functest_utils.py

We may distinguish 4 different folders:

  * **commons**: it is a folder dedicated to store traffic profile or any test
    inputs that could be reused by any test project
  * **docker**: this folder includes the scripts that will be used to setup the
    environment and run the tests
  * **docs**: this folder includes the user and installation/configuration guide
  * **testcases**: this folder includes the scripts required by Functest internal
    test cases and other feature projects test cases.

After the *run* command, a new prompt appears which means that we are inside the
container and ready to move to the next step.


Useful Docker commands
----------------------

When typing **exit** in the container prompt, this will cause sometimes
exiting the container and stopping it. When stopping a running Docker container
all the changes will be lost when it is started again. There is a shortcut to
quit the container without stopping it. Type CTRL+P+Q to keep the changes.
To reconnect to the running container **DO NOT** use the *run* command again
(since it will create a new container) use *exec* instead::

  docker ps
  <copy the container ID>
  docker exec -ti <CONTAINER_ID> bash

or simply::

  docker exec -ti $(docker ps|grep functest|awk '{print $1}') bash

There are other useful Docker commands that might be needed to manage possible
issues with the containers.

 * List the running containers::

  docker ps

 * List all the containers including the stopped ones::

  docker ps -a

 * It is useful sometimes to remove a container if there are some problems::

  docker rm <CONTAINER_ID>

 * Use the *-f* option if the container is still running, it will force to destroy it::

  docker -f rm <CONTAINER_ID>

The Docker image is named **opnfv/functest** and it is stored in the public
Docker registry under the OPNFV account: dockerhub_.
The are many different tags that have been created automatically by the CI
mechanisms, but the one that this document refers to is **brahmaputra.1.0**.
Other tags might cause some problems while running the tests.

Check the Docker documentation dockerdocs_ for more information.


Preparing the Functest environment
----------------------------------

Once the docker container is up and running, execute the following command in the
prompt::

 ${repos_dir}/functest/docker/prepare_env.sh

NOTE: **${repos_dir}** is a default environment variable inside the docker
container, which points to */home/opnfv/repos/*

This script will make sure that the requirements to run the tests are met and will
install the needed libraries and tools by all Functest test cases. It must be run
only once every time the docker is started.


Focus on the OpenStack credentials
----------------------------------

The OpenStack credentials are needed to run the tests against the VIM.
There are 3 ways to provide them to Functest:

  * using the -v option when running the Docker container
  * create an empty file in /home/opnfv/functest/conf/openstack.creds and paste
    the credentials in it.
  * automatically retrieved using the following script::
         $repos_dir/releng/utils/fetch_os_creds.sh

Once the credentials are there, they shall be sourced before running the tests::

    source /home/opnfv/functest/conf/openstack.creds

or simply using the environment variable **$creds**::

    . $creds

After this, try to run any OpenStack command to see if you get any output,
for instance::

    openstack user list

This will return a list of the actual users in the OpenStack deployment. In any
other case, check that the credentials are sourced::

    env|grep OS_

This command must show a set of environment variables starting with *OS_*, for example::

    OS_REGION_NAME=RegionOne
    OS_DEFAULT_DOMAIN=default
    OS_PROJECT_NAME=admin
    OS_PASSWORD=admin
    OS_AUTH_STRATEGY=keystone
    OS_AUTH_URL=http://172.30.10.3:5000/v2.0
    OS_USERNAME=admin
    OS_TENANT_NAME=admin
    OS_ENDPOINT_TYPE=internalURL
    OS_NO_CACHE=true

If still the OpenStack command does not show anything or complains about
connectivity issues, it could be due to an incorrect url given to the OS_AUTH_URL
environment variable. Check the deployment settings.

Additional Options
------------------

In case you need to provide different configuration parameters to Functest (e.g.
 commit IDs or branches for the repositories, ...) copy the config_functest.yaml
 from the repository to your current directory and run docker with a volume::

    wget https://git.opnfv.org/cgit/functest/plain/testcases/config_functest.yaml

    <modify the file accordingly>

    docker run -ti -e \
    "INSTALLER_TYPE=fuel" -e "INSTALLER_IP=10.20.0.2" \
    opnfv/functest:brahmaputra.1.0 \
    -v $(pwd)/config_functest.yaml:/home/opnfv/functest/conf/config_functest.yaml \
    /bin/bash\

However, this is not recommended since most of the test cases rely on static
parameters read from this file, and changing them might cause problems.

.. _dockerdocs: https://docs.docker.com/
.. _dockerhub: https://hub.docker.com/r/opnfv/functest/
