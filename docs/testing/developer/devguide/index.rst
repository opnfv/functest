.. SPDX-License-Identifier: CC-BY-4.0

************************
Functest Developer Guide
************************

.. toctree::
   :maxdepth: 2

============
Introduction
============

Functest is a project dealing with functional testing.
The project produces its own internal test cases but can also be considered
as a framework to support feature and VNF onboarding project testing.

Therefore there are many ways to contribute to Functest. You can:

 * Develop new internal test cases
 * Integrate the tests from your feature project
 * Develop the framework to ease the integration of external test cases

Additional tasks involving Functest but addressing all the test projects
may also be mentioned:

  * The API / Test collection framework
  * The dashboards
  * The automatic reporting portals
  * The testcase catalog

This document describes how, as a developer, you may interact with the
Functest project. The first section details the main working areas of
the project. The Second part is a list of "How to" to help you to join
the Functest family whatever your field of interest is.


========================
Functest developer areas
========================


Functest High level architecture
================================

Functest is a project delivering test containers dedicated to OPNFV.
It includes the tools, the scripts and the test scenarios.
In Euphrates Alpine containers have been introduced in order to lighten the
container and manage testing slicing. The new containers are created according
to the different tiers:

  * functest-core: https://hub.docker.com/r/opnfv/functest-core/
  * functest-healthcheck: https://hub.docker.com/r/opnfv/functest-healthcheck/
  * functest-smoke: https://hub.docker.com/r/opnfv/functest-smoke/
  * functest-vnf: https://hub.docker.com/r/opnfv/functest-vnf/
  * functest-restapi: https://hub.docker.com/r/opnfv/functest-restapi/

Standalone functest dockers are maintained for Euphrates but Alpine containers
are recommended.

Functest can be described as follow::

  +----------------------+
  |                      |
  |   +--------------+   |                  +-------------------+
  |   |              |   |    Public        |                   |
  |   | Tools        |   +------------------+      OPNFV        |
  |   | Scripts      |   |                  | System Under Test |
  |   | Scenarios    |   |                  |                   |
  |   |              |   |                  |                   |
  |   +--------------+   |                  +-------------------+
  |                      |
  |    Functest Docker   |
  |                      |
  +----------------------+

Functest internal test cases
============================
The internal test cases in Euphrates are:


 * connection_check
 * vping_ssh
 * vping_userdata
 * odl
 * rally_full
 * rally_sanity
 * tempest_smoke
 * tempest_full
 * cloudify_ims

By internal, we mean that this particular test cases have been developed and/or
integrated by functest contributors and the associated code is hosted in the
Functest repository.
An internal case can be fully developed or a simple integration of
upstream suites (e.g. Tempest/Rally developed in OpenStack, or odl suites are
just integrated in Functest).

The structure of this repository is detailed in `[1]`_.
The main internal test cases are in the opnfv_tests subfolder of the
repository, the internal test cases can be grouped by domain:

 * sdn: odl, odl_fds
 * openstack: connection_check, vping_ssh, vping_userdata, tempest_*, rally_*
 * vnf: cloudify_ims

If you want to create a new test case you will have to create a new folder
under the testcases directory (See next section for details).

Functest framework
==================

Functest is a framework.

Historically Functest is released as a docker file, including tools, scripts
and a CLI to prepare the environment and run tests.
It simplifies the integration of external test suites in CI pipeline and
provide commodity tools to collect and display results.

Since Colorado, test categories also known as **tiers** have been created to
group similar tests, provide consistent sub-lists and at the end optimize
test duration for CI (see How To section).

The definition of the tiers has been agreed by the testing working group.

The tiers are:
  * healthcheck
  * smoke
  * benchmarking
  * features
  * vnf

Functest abstraction classes
============================

In order to harmonize test integration, abstraction classes have been
introduced:

 * testcase: base for any test case
 * unit: run unit tests as test case
 * feature: abstraction for feature project
 * vnf: abstraction for vnf onboarding

The goal is to unify the way to run tests in Functest.

Feature, unit and vnf_base inherit from testcase::

              +----------------------------------------------------------------+
              |                                                                |
              |                   TestCase                                     |
              |                                                                |
              |                   - init()                                     |
              |                   - run()                                      |
              |                   - push_to_db()                               |
              |                   - is_successful()                            |
              |                                                                |
              +----------------------------------------------------------------+
                 |             |                 |                           |
                 V             V                 V                           V
  +--------------------+   +---------+   +------------------------+   +-----------------+
  |                    |   |         |   |                        |   |                 |
  |    feature         |   |  unit   |   |    vnf                 |   | robotframework  |
  |                    |   |         |   |                        |   |                 |
  |                    |   |         |   |- prepare()             |   |                 |
  |  - execute()       |   |         |   |- deploy_orchestrator() |   |                 |
  | BashFeature class  |   |         |   |- deploy_vnf()          |   |                 |
  |                    |   |         |   |- test_vnf()            |   |                 |
  |                    |   |         |   |- clean()               |   |                 |
  +--------------------+   +---------+   +------------------------+   +-----------------+


Functest util classes
=====================

In order to simplify the creation of test cases, Functest develops also some
functions that are used by internal test cases.
Several features are supported such as logger, configuration management and
Openstack capabilities (tacker,..).
These functions can be found under <repo>/functest/utils and can be described
as follows::

 functest/utils/
 |-- config.py
 |-- constants.py
 |-- decorators.py
 |-- env.py
 |-- functest_utils.py
 |-- openstack_tacker.py
 `-- openstack_utils.py


TestAPI
=======
Functest is using the Test collection framework and the TestAPI developed by
the OPNFV community. See `[4]`_ for details.


Reporting
=========
A web page is automatically generated every day to display the status based on
jinja2 templates `[3]`_.


Dashboard
=========

Additional dashboarding is managed at the testing group level, see `[5]`_ for
details.


==========
References
==========

_`[1]`: http://artifacts.opnfv.org/functest/docs/configguide/index.html Functest configuration guide

_`[2]`: http://artifacts.opnfv.org/functest/docs/userguide/index.html functest user guide

_`[3]`: https://github.com/opnfv/releng-testresults/tree/master/reporting

_`[4]`: https://wiki.opnfv.org/display/functest/2017+Beijing?preview=%2F11699623%2F11700523%2FTestAPI+-+test+results+collection+service.pptx

_`[5]`: https://lfanalytics.io/projects/lfn%2Fopnfv/dashboard

IRC support chan: #opnfv-functest
