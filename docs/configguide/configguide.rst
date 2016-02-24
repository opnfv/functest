.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


Functional testing Installation
-------------------------------

Pull the Functest Docker image from the Docker hub::

  $ docker pull opnfv/functest:brahmaputra.1.0


Check that the image is available::

 $ docker images

Run the docker container giving the environment variables::

 - INSTALLER_TYPE. Possible values are "apex", "compass", "fuel" or "joid".
 - INSTALLER_IP. each installer has its installation strategy.

Functest may need to know the IP of the installer to retrieve the credentials
(e.g. usually "10.20.0.2" for fuel, not neede for joid...).

The minimum command to create the Functest docker file can be described as
follows::

  docker run -it -e "INSTALLER_IP=10.20.0.2" -e "INSTALLER_TYPE=fuel" opnfv/functest:brahmaputra.1.0 /bin/bash

Optionally, it is possible to precise the container name through the option
--name::

  docker run --name "CONTAINER_NAME" -it -e "INSTALLER_IP=10.20.0.2" -e "INSTALLER_TYPE=fuel" opnfv/functest:brahmaputra.1.0 /bin/bash

It is also possible to to indicate the path of the OpenStack creds using -v::

  docker run  -it -e "INSTALLER_IP=10.20.0.2" -e "INSTALLER_TYPE=fuel" -v <path_to_your_local_creds_file>:/home/opnfv/functest/conf/openstack.creds opnfv/functest:brahmaputra.1.0 /bin/bash

The local file will be mounted in the container under
/home/opnfv/functest/conf/openstack.creds

After the run command the prompt appears which means that we are inside the
container and ready to run Functest.

Inside the container, the following directory structure should be in place::

  `-- home
      `-- opnfv
        |-- functest
        |   |-- conf
        |   |-- data
        |   `-- results
        `-- repos
            |-- bgpvpn
            |-- functest
            |-- odl_integration
            |-- rally
            |-- releng
            `-- vims-test


Basically the container includes:

  * Functest directory to store the configuration (the OpenStack creds are paste
    in /home/opngb/functest/conf), the data (images neede for test for offline
    testing), results (some temporary artifacts may be stored here)
  * Repositories: the functest repository will be used to prepare the
    environment, run the tests. Other repositories are used for the installation
    of the tooling (e.g. rally) and/or the retrieval of feature projects
    scenarios (e.g. bgpvpn)

The arborescence under the functest repo can be described as follow::

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
    |   |-- functest.rst
    |   |-- images
    |   `-- userguide
    `-- testcases
        |-- Controllers
        |-- VIM
        |-- __init__.py
        |-- config_functest.py
        |-- config_functest.yaml
        |-- functest_utils.py
        |-- functest_utils.pyc
        |-- vIMS
        `-- vPing

We may distinguish 4 different folders:

  * commons: it is a folder dedicated to store traffic profile or any test
    inputs that could be reused by any test project
  * docker: this folder includes the scripts that will be used to setup the
    environment and run the tests
  * docs: this folder includes the user and installation/configuration guide
  * testcases: this folder includes the scripts required by Functest internal
    test cases


Firstly run the script to install functest environment::

 $ ${repos_dir}/functest/docker/prepare_env.sh

NOTE: ${repos_dir} is a default environment variable inside the docker
container, which points to /home/opnfv/repos

Run the script to start the tests::

 $ ${repos_dir}/functest/docker/run_tests.sh
