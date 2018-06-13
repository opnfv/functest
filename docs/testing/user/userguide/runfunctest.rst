.. SPDX-License-Identifier: CC-BY-4.0

Executing Functest suites
=========================

As mentioned in the configuration guide `[1]`_, Alpine docker containers have
been introduced in Euphrates.
Tier containers have been created.
Assuming that you pulled the container and your environement is ready, you can
simply run the tiers by typing (e.g. with functest-healthcheck)::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file  \
      -v $(pwd)/images:/home/opnfv/functest/images  \
      opnfv/functest-healthcheck

You should get::

  +----------------------------+------------------+---------------------+------------------+----------------+
  |         TEST CASE          |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +----------------------------+------------------+---------------------+------------------+----------------+
  |      connection_check      |     functest     |     healthcheck     |      00:02       |      PASS      |
  |         api_check          |     functest     |     healthcheck     |      03:19       |      PASS      |
  |     snaps_health_check     |     functest     |     healthcheck     |      00:46       |      PASS      |
  +----------------------------+------------------+---------------------+------------------+----------------+

You can run functest-healcheck, functest-smoke, functest-features,
functest-components and functest-vnf.

The result tables show the results by test case, it can be::

  * PASS
  * FAIL
  * SKIP: if the scenario/installer does not support the test case


Manual run
==========
If you want to run the test step by step, you may add docker option then run
the different commands within the docker.

Considering the healthcheck example, running functest manaully means::

  sudo docker run -ti --env-file env \
    -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file  \
    -v $(pwd)/images:/home/opnfv/functest/images  \
    opnfv/functest-healthcheck /bin/bash

The docker prompt shall be returned. Then within the docker run the following
commands::

  $ source /home/opnfv/functest/conf/env_file

Tier
----
Each Alpine container provided on the docker hub matches with a tier.
The following commands are available::

  # functest tier list
    - 0. healthcheck:
    ['connection_check', 'api_check', 'snaps_health_check']
  # functest tier show healthcheck
  +---------------------+---------------+--------------------------+-------------------------------------------------+------------------------------------+
  |        TIERS        |     ORDER     |         CI LOOP          |                   DESCRIPTION                   |             TESTCASES              |
  +---------------------+---------------+--------------------------+-------------------------------------------------+------------------------------------+
  |     healthcheck     |       0       |     (daily)|(weekly)     |     First tier to be executed to verify the     |     connection_check api_check     |
  |                     |               |                          |           basic operations in the VIM.          |         snaps_health_check         |
  +---------------------+---------------+--------------------------+-------------------------------------------------+------------------------------------+

To run all the cases of the tier, type::

  # functest tier run healthcheck

Testcase
--------
Testcases can be listed, shown and run though the CLI::

  # functest testcase list
   connection_check
   api_check
   snaps_health_check
  # functest testcase show api_check
  +-------------------+--------------------------------------------------+------------------+---------------------------+
  |     TEST CASE     |                   DESCRIPTION                    |     CRITERIA     |         DEPENDENCY        |
  +-------------------+--------------------------------------------------+------------------+---------------------------+
  |     api_check     |     This test case verifies the retrieval of     |       100        |       ^((?!lxd).)*$       |
  |                   |       OpenStack clients: Keystone, Glance,       |                  |                           |
  |                   |      Neutron and Nova and may perform some       |                  |                           |
  |                   |     simple queries. When the config value of     |                  |                           |
  |                   |       snaps.use_keystone is True, functest       |                  |                           |
  |                   |     must have access to the cloud's private      |                  |                           |
  |                   |                     network.                     |                  |                           |
  +-------------------+--------------------------------------------------+------------------+---------------------------+
  # functest testcase run connection_check
  ...
  # functest run all

You can also type run_tests -t all to run all the tests.

Note the list of test cases depend on the installer and the scenario.

Note that the flavors for the SNAPS test cases are able to be configured giving
new metadata values as well as new values for the basic elements of flavor
(i.e. ram, vcpu, disk, ephemeral, swap etc).
The snaps.flavor_extra_specs dict in the config_functest.yaml file could be
used for this purpose.

Reporting results to the test Database
======================================
In OPNFV CI we collect all the results from CI. A test API shall be available
as well as a test database `[17]`_.

Functest internal API
=====================

An internal API has been introduced in Euphrates. The goal is to trigger
Functest operations through an API in addition of the CLI.
This could be considered as a first step towards a pseudo micro services
approach where the different test projects could expose and consume APIs to the
other test projects.

In Euphrates the main method of the APIs are:

  * Show credentials
  * Update openrc file
  * Show environment
  * Update hosts info for domain name
  * Prepare environment
  * List all testcases
  * Show a testcase
  * Run a testcase
  * List all tiers
  * Show a tier
  * List all testcases within given tier
  * Get the result of the specified task
  * Get the log of the specified task

See `[16]`_ to get examples on how to use the API.


.. _`[1]`: http://docs.opnfv.org/en/latest/submodules/functest/docs/testing/user/configguide/index.html
.. _`[16]`: https://wiki.opnfv.org/display/functest/Running+test+cases+via+new+Functest+REST+API
.. _`[17]`: http://docs.opnfv.org/en/latest/testing/testing-dev.html
