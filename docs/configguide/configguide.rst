.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


Preparing the Docker container
------------------------------

Pull the Functest Docker image ('opnfv/functest') from the public dockerhub
registry under the OPNFV account: [dockerhub_], with the following docker
command::

  docker pull opnfv/functest:<TagIdentifier>

where <TagIdentifier> identifies a specifically tagged release of the Functest
docker container image in the public dockerhub registry. There are many
different tags created automatically by the CI mechanisms, but you must ensure
you pull an image with the **correct tag** to match the OPNFV software release
installed in your environment. All available tagged images can be seen from
location [FunctestDockerTags_]. For example, when running on the first official
release of the OPNFV Colorado system platform, tag "colorado.1.0" is needed.
Pulling other tags might cause some problems while running the tests. If you
need to specifically pull the latest Functest docker image, then omit the tag
argument::


  docker pull opnfv/functest

After pulling the Docker image, check that the pulled image is available with
the following docker command::

  [functester@jumphost ~]$ docker images

  REPOSITORY     TAG             IMAGE ID      CREATED      SIZE
  opnfv/functest latest          8cd6683c32ae  2 weeks ago  1.611 GB
  opnfv/functest brahmaputra.3.0 94b78faa94f7  4 weeks ago  874.9 MB
  hello-world    latest          94df4f0ce8a4  7 weeks ago    967 B

  (Docker images pulled without a tag specifier bear the implicitly
   assigned label "latest", as seen above.)

The Functest docker container environment can -in principle- be also used with
non-OPNFV official installers (e.g. 'devstack), with the **disclaimer** that
support for such environments is outside of the scope of responsibility of the
OPNFV project.

The minimum command to create the Functest Docker container can be described as
follows::

  docker run -it opnfv/functest:<TagIdentifier> /bin/bash

For OPNFV official installers, it is recommended (although no longer mandatory)
to provide two additional environment variables, in the 'docker run ...'
command nvocation:

 * **INSTALLER_TYPE** : possible values are **apex**, **compass**, **fuel** or
   **joid**.
 * **INSTALLER_IP** : IP of the installer node/VM.

Functest may need to know the IP of the installer to retrieve automatically the
credentials from the installer node/VM or even from the actual controllers.

Thus, the recommended minimum command to create the Functest Docker container
for OPNFV installer can be described (using installer 'fuel', and an invented
INSTALLER_IP of '10.20.0.2', for example), as follows::

  docker run -it \
  -e "INSTALLER_IP=10.20.0.2" \
  -e "INSTALLER_TYPE=fuel" \
  opnfv/functest:<TagIdentifier> /bin/bash

Optionally, it is possible to assign precisely a container name through the
**--name** option::

  docker run --name "CONTAINER_NAME" -it \
  -e "INSTALLER_IP=10.20.0.2" \
  -e "INSTALLER_TYPE=fuel" \
  opnfv/functest:<TagIdentifier> /bin/bash

It is also possible to to indicate the path of the OpenStack credentials using a
**-v** option::

  docker run -it \
  -e "INSTALLER_IP=10.20.0.2" \
  -e "INSTALLER_TYPE=fuel" \
  -v <path_to_your_local_creds_file>:/home/opnfv/functest/conf/openstack.creds \
  opnfv/functest:<TagIdentifier> /bin/bash

  NOTE: Make sure you have placed the needed credential file into the
        Jumphost local path <path_to_your_local_cred_file>. For the
        Apex Installer you will need to pre-copy the required OpenStack
        credentials file from the Instack/Undercloud Virtual Machine.
        See the section 'Apex Installer Tips' later in this document.

  Warning
  -------
  If you are using the Joid installer, you must use the method above
  to provide the required OpenStack credentials. See the section
  'Focus on the OpenStack credentials' later in this document.


The local openstack credential file will be mounted in the Docker container
under the path: '/home/opnfv/functest/conf/openstack.creds'

If the intention is to run Functest against any of the supported OPNFV
scenarios, it is recommended to include also the environment variable
**DEPLOY_SCENARIO**. The **DEPLOY_SCENARIO** environment variable is passed with the format::

  -e "DEPLOY_SCENARIO=os-<controller>-<nfv_feature>-<ha_mode>"

  where:
  os = OpenStack (No other VIM choices currently available)
  controller  is one of ( nosdn | odl_l2 | odl_l3 | onos | ocl )
  nfv_feature is one or more of ( ovs | kvm | sfc | bgpvpn | nofeature )
              If several features are pertinent then use the underscore
              character '_' to separate each feature (e.g. ovs_kvm)
              'nofeature' indicates no NFV feature is deployed
  ha_mode     is one of ( ha | noha )

For example::

  docker run -it \
  -e "INSTALLER_IP=10.20.0.2" \
  -e "INSTALLER_TYPE=fuel" \
  -e "DEPLOY_SCENARIO=os-odl_l2-ovs_kvm-ha" \
  opnfv/functest:<TagIdentifier> /bin/bash

**NOTE:** Not all possible combinations of "DEPLOY_SCENARIO" are supported.
The scenario name passed in to the Functest Docker container must match the
scenario used with the selected installer to create the actual OPNFV platform
deployment.

Finally, three additional environment variables can also be passed in to the
Functest Docker Container, using the -e "<EnvironmentVariableName>=<Value>"
mechanism. The first two of these are only relevant to Jenkins CI invoked
testing and **should not be used** when performing manual test scenarios::

  -e "NODE_NAME=<Test POD Name>" \
  -e "BUILD_TAG=<Jenkins Build Tag>" \
  -e "CI_DEBUG=<DebugTraceValue>"

  where:
  <Test POD Name> = Symbolic name of the POD where the tests are run.
                    Visible in test results files, which are stored
                    to the database. This option is only used when
                    tests are activated under Jenkins CI control.
                    It indicates the POD/hardware where the test has
                    been run. If not specified, then the POD name is
                    defined as "Unknown" by default.
                    DO NOT USE THIS OPTION IN MANUAL TEST SCENARIOS.

  <Jenkins Build tag> = Symbolic name of the Jenkins Build Job.
                        Visible in test results files, which are stored
                        to the database. This option is only set when
                        tests are activated under Jenkins CI control.
                        It enables the correlation of test results, which
                        are independently pushed to the results datbase
                        from different Jenkins jobs.
                        DO NOT USE THIS OPTION IN MANUAL TEST SCENARIOS.

  <DebugTraceValue> = "true" or "false"
                      Default = "false", if not specified
                      If "true" is specified, then additional debug trace
                      text can be sent to the test results file / log files
                      and also to the standard console output.

Apex Installer Tips
-------------------
Some specific tips are useful for the Apex Installer case. If not using Apex
Installer; ignore this section.

  #. The "INSTALLER_IP" environment variable should be set equal to the IP
     address of the so-called "Instack/undercloud Virtual Machine".

     In the Jumphost, execute the following command and note the returned
     IP address::

       sudo virsh domifaddr undercloud | grep -Eo "[0-9.]+{4}"

       NOTE: In releases prior to Colorado, the name 'instack' was
       used. From Colorado onward, the name 'undercloud' is used.
       If in doubt, then execute -from the Jumphost- the command
       "virsh list" to see which name is in use for the Installer
       Virtual Machine.

     You can now enter the <Specific IP Address> as learned in the above step in the
     -e option specification::

       -e "INSTALLER_IP=<Specific IP Address>"

  #. If you want to 'Bind mount' a local Openstack credentials file ("overcloudrc")
     to the Docker container, then you may need to first pre-copy that file from the
     'Instack/Undercloud VM' to the Jump host.

     As before, in the Jumphost, execute the following command and note the
     returned IP address::

       sudo virsh domifaddr undercloud | grep -Eo "[0-9.]+{4}"

     Using the <Specific IP Address> just learned above, execute the following
     shell commands **in the Jumphost**, before issuing the 'docker run ...' command
     invocation::

       scp stack@<Specific IP Address>:overcloudrc .
       sed -i 's/export no_proxy/#export no_proxy/' overcloudrc
       # The above 'sed' command is needed *only* in cases where
       # the Jumphost is operating behind a http proxy.
       # See the 'Proxy Support' section later on in this document

       NOTE: There are two Openstack credential files present in the
       Instack/Undercloud VM: 'overcloudrc' and 'stackrc'.
       Don't mix these up! The file 'stackrc' is intended for use with
       'Triple O Undercloud'; only. The SUT always requires OpenStack
       Overcloud Credentials.

     The file located at Jumphost path: '~/overcloudrc' is now 'Bind mounted'
     to the Docker path '/home/opnfv/functest/conf/openstack.creds'
     by specifying a **-v** option::

       -v ~/overcloudrc:/home/opnfv/functest/conf/openstack.creds

     in the argument list of the 'docker run ...' command invocation. In the
     Apex installer case, the Openstack Credential file has the name
     'overcloudrc' and is located in the home directory of the 'stack' user
     ( '/home/stack/' or '~/'] ) in the 'Instack/Undercloud VM'.

  #. In order that the docker container can access the Instack/Undercloud VM,
     even with 'stack' user, the SSH keys of the Jumphost root user **must be**
     'Bind mounted' to the docker container by the following **-v** option in
     the 'docker run ...' command invocation::

       -v /root/.ssh/id_rsa:/root/.ssh/id_rsa

  #. Here is an example of the docker command invocation for an Apex installed
     system, using latest Funtest docker container, for illustration purposes::

       docker run -it --name "ApexFuncTstODL" \
       -e "INSTALLER_IP=<Specific IP Address>" \
       -e "INSTALLER_TYPE=apex" \
       -e "DEPLOY_SCENARIO=os-odl_l2-nofeature-ha" \
       -v /root/.ssh/id_rsa:/root/.ssh/id_rsa \
       -v ~/overcloudrc:/home/opnfv/functest/conf/openstack.creds \
       opnfv/functest /bin/bash

Functest docker container directory structure
---------------------------------------------
Inside the Functest docker container, the following directory structure should
now be in place::

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
            |-- ovno
            |-- promise
            |-- rally
            |-- releng
            `-- vims-test

  (The sub-directory 'ovno' holds SDN controller functional tests
   for the OpenContrail SDN Controller, which should be available
   for Colorado release)

Underneath the '/home/opnfv/' directory, the Functest docker container
includes two main directories:

  * The **functest** directory stores configuration files (e.g. the OpenStack
    creds are stored in path '/home/opnfv/functest/conf/openstack.creds'), the
    **data** directory stores a 'cirros' test image used in some functional
    tests and the **results** directory stores some temporary result log files
  * The **repos** directory holds various repositories. The directory
    '/home/opnfv/repos/functest' is used to prepare the needed Functest
    environment and to run the tests. The other repository directories are
    used for the installation of the needed tooling (e.g. rally) or for the
    retrieval of feature projects scenarios (e.g. promise)

The structure under the **functest** repository can be described as follows::

  . |-- INFO
    |-- LICENSE
    |-- __init__.py
    |-- ci
    |   |-- __init__.py
    |   |-- check_os.sh
    |   |-- config_functest.yaml
    |   |-- exec_test.sh
    |   |-- prepare_env.py
    |   |-- run_tests.py
    |   |-- testcases.yaml
    |   |-- tier_builder.py
    |   `-- tier_handler.py
    |-- cli
    |   |-- __init__.py
    |   |-- cli_base.py
    |   |-- commands
    |   |-- functest-complete.sh
    |   `-- setup.py
    |-- commons
    |   |-- ims
    |   |-- mobile
    |   `--traffic-profile-guidelines.rst
    |-- docker
    |   |-- Dockerfile
    |   |-- config_install_env.sh
    |   `-- requirements.pip
    |-- docs
    |   |-- com
    |   |-- configguide
    |   |-- devguide
    |   |-- images
    |   |-- release-notes
    |   |-- results
    |   `--userguide
    |-- testcases
    |   |-- Controllers
    |   |-- OpenStack
    |   |-- __init__.py
    |   |-- features
    |   |-- security_scan
    |   `-- vIMS
    `-- utils
        |-- __init__.py
        |-- functest_logger.py
        |-- functest_utils.py
        |-- openstack_clean.py
        |-- openstack_snapshot.py
        `-- openstack_utils.py

    (Note: All *.pyc files removed from above list for brevity...)

We may distinguish 7 different directories:

  * **ci**: This directory contains test structure defintion files
    (e.g <filename>.yaml) and bash shell/python scripts used to configure and
    execute Functional tests. The test execution script can be executed under
    the control of Jenkins CI jobs.
  * **cli**: This directory holds the python based Functest CLI utility source
    code, which is based on the Python 'click' framework.
  * **commons**: This directory is dedicated for storage of traffic profile or
    any other test inputs that could be reused by any test project.
  * **docker**: This directory includes the needed files and tools to build the
    Funtest Docker container image.
  * **docs**: This directory includes documentation: Release Notes, User Guide,
    Configuration Guide and Developer Guide. Test results are also located in
    a sub--directory called 'results'.
  * **testcases**: This directory includes the scripts required by Functest
    internal test cases and other feature projects test cases.
  * **utils**: this directory holds Python source code for some general purpose
    helper utilities, which testers can also re-use in their own test code.
    See for an example the Openstack helper utility: 'openstack_utils.py'.

After the *run* command, a new prompt appears which means that we are inside
the container and ready to move to the next step.

Useful Docker commands
----------------------
When typing **exit** in the container prompt, this will cause exiting the
container and probably stopping it. When stopping a running Docker container
all the changes will be lost, there is a keyboard shortcut to quit the
container without stopping it: CTRL+P+Q. To reconnect to the running container
**DO NOT** use the *run* command again (since it will create a new container),
use the *exec* command instead::

  docker ps <copy the container ID> docker exec -ti \
  <CONTAINER_ID> /bin/bash

or simply::

  docker exec -ti \
  $(docker ps|grep functest|awk '{print $1}') /bin/bash

There are other useful Docker commands that might be needed to manage possible
issues with the containers.

List the running containers::

  docker ps

List all the containers including the stopped ones::

  docker ps -a

It is useful sometimes to remove a container if there are some problems::

  docker rm <CONTAINER_ID>

Use the *-f* option if the container is still running, it will force to
destroy it::

  docker -f rm <CONTAINER_ID>

The Docker image is called **opnfv/functest** and it is stored in the public
Docker registry under the OPNFV account: dockerhub_. The are many different
tags that have been created automatically by the CI mechanisms, but the one
that this document refers to is **brahmaputra.1.0**. Pulling other tags might
cause some problems while running the tests.

Check the Docker documentation dockerdocs_ for more information.

Preparing the Functest environment
----------------------------------
Once the Functest docker container is up and running, the required Functest
environment needs to be prepared. A custom built **functest** CLI utility is
availabe to perform the needed environment preparation action. Once the
enviroment is prepared, the **functest** CLI utility can be used to run
different functional tests. The usage of the **functest** CLI utility to run
tests is described further in the Functest User Guide `OPNFV_FuncTestUserGuide`_

Prior to commencing the Functest environment preparation, we can check the
initial status of the environment. Issue the **functest env status** command at
the prompt::

  functest env status
  Functest environment is not installed.

  Note: When the Funtest environment is prepared, the command will
  return the status: "Functest environment ready to run tests."

To prepare the Functest docker container for test case execution, issue the
**functest env prepare** command at the prompt::

  functest env prepare

This script will make sure that the requirements to run the tests are met and
will install the needed libraries and tools by all Functest test cases. It
should be run only once every time the Functest docker container is started
from scratch. If you try to run this command, on an already prepared
enviroment, you will be prompted whether you really want to continue or not::

  functest env prepare
  It seems that the environment has been already prepared.
  Do you want to do it again? [y|n]

  (Type 'n' to abort the request, or 'y' to repeat the
   environment preparation)


To list some basic information about an already prepared Functest docker
container environment, issue the **functest env show** at the prompt::

  functest env show
  +======================================================+
  | Functest Environment info                            |
  +======================================================+
  |  INSTALLER: apex, 192.168.122.89                     |
  |   SCENARIO: os-odl_l2-nofeature-ha                   |
  |        POD: localhost                                |
  | GIT BRANCH: master                                   |
  |   GIT HASH: 5bf1647dec6860464eeb082b2875798f0759aa91 |
  | DEBUG FLAG: false                                    |
  +------------------------------------------------------+
  |     STATUS: ready                                    |
  +------------------------------------------------------+

  Where:

  INSTALLER:  Displays the INSTALLER_TYPE value
              - here = "apex"
              and the INSTALLER_IP value
              - here = "192.168.122.89"
  SCENARIO:   Displays the DEPLOY_SCENARIO value
              - here = "os-odl_l2-nofeature-ha"
  POD:        Displays the value pass in NODE_NAME
              - here = "loclahost"
  GIT BRANCH: Displays the git branch of the OPNFV Functest
              project repository included in the Functest
              Docker Container.
              - here = "master"
                       (In first official colorado release
                        would be "colorado.1.0")
  GIT HASH:   Displays the git hash of the OPNFV Functest
              project repository included in the Functest
              Docker Container.
              - here = "5bf1647dec6860464eeb082b2875798f0759aa91"
  DEBUG FLAG: Displays the CI_DEBUG value
              - here = "false"

  NOTE: In Jenkins CI runs, an additional item "BUILD TAG"
        would also be listed. The valaue is set by Jenkins CI.

Finally, the **functest** CLI has a basic 'help' system with so called
**--help** options:

Some examples::

  functest --help Usage: functest [OPTIONS] COMMAND [ARGS]...

  Options:
    --version  Show the version and exit.
    -h, --help Show this message and exit.

  Commands:
    env
    openstack
    testcase
    tier

  functest env --help
  Usage: functest env [OPTIONS] COMMAND [ARGS]...

  Options:
    -h, --help Show this message and exit.

  Commands:
    prepare  Prepares the Functest environment.
    show     Shows information about the current...
    status   Checks if the Functest environment is ready...

Focus on the OpenStack credentials
----------------------------------
The OpenStack credentials are needed to run the tests against the VIM.
There are 3 ways to provide them to Functest:

  * using the -v option when running the Docker container
  * create an empty file in '/home/opnfv/functest/conf/openstack.creds' and
    paste the credentials into it. (Consult your installer guide to know from
    where you can retrieve credential files, which are set-up in the Openstack
    installation of the SUT)
  * automatically retrieved using the following script::

      $repos_dir/releng/utils/fetch_os_creds.sh \
      -d /home/opnfv/functest/conf/openstack.creds \
      -i fuel \
      -a 10.20.0.2"

      (-d specifies the full destination path where to place the
          copied Openstack credential file
       -i specifies the INSTALLER_TYPE
       -a specifies the INSTALLER_IP
       If the installer is of type "fuel" and a Virtualized
       deployment is used, then this should be indicated by
       adding an option '-v'. The -v option takes no arguments.
       It enables some needed special handling in the script.)

      Note: If you omit the -d <full destination path> option in
      the command invocation, then the script will create the
      credential file with name 'opnfv-openrc.sh' in directory
      '/home/opnfv'. In that case, you need to copy/edit the file
      into the correct target path:
      '/home/opnfv/functest/conf/openstack.creds'.

**Warning** If you are using the Joid installer, the 'fetch_os_cred-sh' shell
script **should not be used**. Use instead, the **-v** optin to Bind Mount a
suitably prepared local copy of the Openstack credentials for usage by the Functest
docker container

Once the credentials are there, they should be sourced **before** running the
tests::

  source /home/opnfv/functest/conf/openstack.creds

or simply using the environment variable **creds**::

  . $creds

After this, try to run any OpenStack command to see if you get any output, for
instance::

  openstack user list

This will return a list of the actual users in the OpenStack deployment. In any
other case, check that the credentials are sourced::

  env|grep OS_

This command must show a set of environment variables starting with *OS_*, for
example::

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

If the OpenStack command still does not show anything or complains about
connectivity issues, it could be due to an incorrect url given to the
OS_AUTH_URL environment variable. Check the deployment settings.

SSL Support
-----------
If you need to connect to a server that is TLS-enabled (the auth URL begins
with ‘https’) and it uses a certificate from a private CA or a self-signed
certificate, then you will need to specify the path to an appropriate CA
certificate to use, to validate the server certificate with the environment
variable OS_CACERT::

  echo $OS_CACERT
  /etc/ssl/certs/ca.crt

However, this certificate does not exist in the container by default. It has
to be copied manually from the OpenStack deployment. This can be done in 2 ways:

  #. Create manually that file and copy the contents from the OpenStack
     controller.
  #. (Recommended) Add the file using a Docker volume when starting the
     container::

       -v <path_to_your_cert_file>:/etc/ssl/certs/ca.cert

You might need to export OS_CACERT environment variable inside the container::

  export OS_CACERT=/etc/ssl/certs/ca.crt

Certificate verification can be turned off using OS_INSECURE=true. For example,
Fuel uses self-signed cacerts by default, so an pre step would be::

  export OS_INSECURE=true

Proxy support
-------------
If your Jumphost node is operating behind a http proxy, then there are 2 places
where some special actions may be needed to make operations succeed:

  #. Initial installation of docker engine First, try following the official
     Docker documentation for Proxy_ settings. Some issues were experienced on
     CentOS 7 based Jumphost. Some tips are documented in section:
     `Docker Installation on CentOS 7 behind http proxy`_ below.

  #. Execution of the Functest environment preparation inside the created
     docker container Functest needs internet access to download some resources
     for some test cases. For example to install the Rally environment. This might
     not work properly if the Jumphost is running through a http Proxy.

If that is the case, make sure the resolv.conf and the needed http_proxy and
https_proxy environment variables, as well as the 'no_proxy' environment
variable are set correctly::

  # Make double sure that the 'no_proxy=...' line in the
  # 'openstack.creds' file is commented out first. Otherwise, the
  # values set into the 'no_proxy' environment variable below will
  # be ovewrwritten, each time the command
  # 'source ~/functest/conf/openstack.creds' is issued.

  sed -i 's/export no_proxy/#export no_proxy/' \
  ~/functest/conf/openstack.creds

  source ~/functest/conf/openstack.creds

  # Next calculate some IP addresses for which http_proxy
  # usage should be excluded:

  publicURL_IP=$(echo $OS_AUTH_URL| \
  grep -Eo "([0-9]+\.){3}[0-9]+")

  adminURL_IP=$(openstack catalog show identity | \
  grep adminURL | grep -Eo "([0-9]+\.){3}[0-9]+")

  export http_proxy="<your http proxy settings>"
  export https_proxy="<your httpsproxy settings>"
  export no_proxy="127.0.0.1,localhost,$publicURL_IP,$adminURL_IP"

  # Ensure that "git" uses the http_proxy
  # This may be needed if your firewall forbids SSL based git fetch
  git config --global http.sslVerify True
  git config --global http.proxy <Your http proxy settings>

Validation check: Before running **'functest env prepare'** CLI command,
make sure you can reach http and https sites from inside the Functest docker
container.

For example, try to use the **nc** command from inside the functest docker
container::

  nc -v google.com 80
  Connection to google.com 80 port [tcp/http] succeeded!

  nc -v google.com 443
  Connection to google.com 443 port [tcp/https] succeeded!

Note: In a Jumphost node based on the CentOS 7, enviroment, it was observed that
the **nc** commands did not function as described in the section above. You can
however try using the **curl** command instead, if you encounter any issues
with the **nc** command::

  curl http://www.google.com:80

  <HTML><HEAD><meta http-equiv="content-type"
  content="text/html;charset=utf-8">
  <TITLE>302 Moved</TITLE>
  </HEAD>
  <BODY>
  <H1>302 Moved</H1>
  :
  :
  </BODY></HTML>

  curl https://www.google.com:443

  <HTML><HEAD><meta http-equiv="content-type"
  content="text/html;charset=utf-8">
  <TITLE>302 Moved</TITLE>
  </HEAD>
  <BODY>
  <H1>302 Moved</H1>
  :
  :
  </BODY></HTML>

  (Even Google complained the URL used, it proves the http and https
   protocols are working correctly through the http / https proxy.)

Docker Installation on CentOS 7 behind http proxy
-------------------------------------------------
There are good instructions in [`InstallDockerCentOS7`_] for the installation
of **docker** on CentOS 7. However, if your Jumphost is behind a http proxy,
then the following steps are needed **before** following the instructions in
the above reference::

  1) # Make a directory '/etc/systemd/system/docker.service.d'
     # if it does not exist
     sudo mkdir /etc/systemd/system/docker.service.d

     # Create a file called 'env.conf' in that directory with
     # the following contents:
     [Service]
     EnvironmentFile=-/etc/sysconfig/docker

  2) # Set up a file called 'docker' in directory '/etc/sysconfig'
     # with the following contents:

     HTTP_PROXY="<Your http proxy settings>"
     HTTPS_PROXY="<Your https proxy settings>"
     http_proxy="${HTTP_PROXY}"
     https_proxy="${HTTPS_PROXY}"

  3) # Reload the daemon
     systemctl daemon-reload

  4) # Sanity check - check the following docker settings:
     systemctl show docker | grep -i env

     Expected result:
     ----------------
     EnvironmentFile=/etc/sysconfig/docker (ignore_errors=yes)
     DropInPaths=/etc/systemd/system/docker.service.d/env.conf

Now follow the instructions in [`InstallDockerCentOS7`_] to download and
install the **docker-engine**. The instructions conclude with a "test pull"
of a sample "Hello World" docker container. This should now work with the
above pre-requisite actions.

.. _dockerdocs: https://docs.docker.com/
.. _dockerhub: https://hub.docker.com/r/opnfv/functest/
.. _Proxy: https://docs.docker.com/engine/admin/systemd/#http-proxy
.. _FunctestDockerTags: https://hub.docker.com/r/opnfv/functest/tags/
.. _InstallDockerCentOS7: https://docs.docker.com/engine/installation/linux/centos/
.. _OPNFV_FuncTestUserGuide: http://artifacts.opnfv.org/functest/docs/userguide/index.html
