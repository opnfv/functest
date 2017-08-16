.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

******************************
OPNFV FUNCTEST developer guide
******************************

.. toctree::
   :numbered:
   :maxdepth: 2

Version history
===============
+------------+----------+------------------+----------------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**                      |
|            |          |                  |                                  |
+------------+----------+------------------+----------------------------------+
| 2017-01-23 | 1.0.0    | Morgan Richomme  | Creation for Danube              |
+------------+----------+------------------+----------------------------------+
| 2017-08-16 | 1.0.1    | Morgan Richomme  | Adaptations for Euphrates        |
|            |          |                  | - move generic part to Testing   |
|            |          |                  | developer guide                  |
|            |          |                  | - move reporting part to functest|
|            |          |                  | user guide                       |
|            |          |                  | - update test case list          |
|            |          |                  | - include auto generated core    |
|            |          |                  | documentation                    |
+------------+----------+------------------+----------------------------------+

============
Introduction
============

Functest is a project dealing with functional testing.
Functest produces its own internal test cases but can also be considered
as a framework to support feature and VNF onboarding project testing.

Therefore there are many ways to contribute to Functest. You can:

 * Develop new internal test cases
 * Integrate the tests from your feature project
 * Develop the framework to ease the integration of external test cases

Additional tasks involving Functest but addressing all the test projects
may also be mentioned:

  * Develop the API / Test collection framework
  * Develop dashboards or automatic reporting portals

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
Until Danube, Functest produced 2 docker files based on Ubuntu 14.04:

  * x86 Functest: https://hub.docker.com/r/opnfv/functest/
  * aarch64 Functest: https://hub.docker.com/r/opnfv/functest_aarch64/

In Euphrates Alpine containers have been introduce in order to lighten the
container and manage testing slicing, the new containers are created according
to the different tiers:

  * functest-core: https://hub.docker.com/r/opnfv/functest-core/
  * functest-healthcheck: https://hub.docker.com/r/opnfv/functest-healthcheck/
  * functest-smoke: https://hub.docker.com/r/opnfv/functest-smoke/
  * functest-features: TODO
  * functest-components: TODO
  * functest-vnf: TODO

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

Functest internal test cases
============================
The internal test cases in Euphrates are:


 * api_check
 * cloudify_ims
 * connection_check
 * vping_ssh
 * vping_userdata
 * odl
 * odl-netvirt
 * odl-fds
 * rally_full
 * rally_sanity
 * snaps_health_check
 * tempest_full_parallel
 * tempest_smoke_serial
 * cloudify_ims

By internal, we mean that this particular test cases have been developped and/or
integrated by functest contributors and the associated code is hosted in the
Functest repository.
An internal case can be fully developed or a simple integration of
upstream suites (e.g. Tempest/Rally developped in OpenStack, or odl suites are
just integrated in Functest).

The structure of this repository is detailed in `[1]`_.
The main internal test cases are in the opnfv_tests subfolder of the
repository, the internal test cases are:

 * sdn: odl, odl_netvirt, odl_fds, onos
 * openstack: api_check, connection_check, snaps_health_check, vping_ssh, vping_userdata, tempest_*, rally_*, snaps_smoke
 * vnf: cloudify_ims

If you want to create a new test case you will have to create a new folder under
the testcases directory (See next section for details).

Functest external test cases
============================
The external test cases are inherited from other OPNFV projects, especially the
feature projects.

The external test cases are:

 * barometer
 * bgpvpn
 * doctor
 * domino
 * onos
 * fds
 * orchestra_clearwaterims
 * orchestra_openims
 * parser
 * promise
 * refstack_defcore
 * snaps_smoke
 * sfc-odl
 * vyos_vrouter

External test cases integrated in previous versions but not released in
Euphrates:

 * copper
 * multisites
 * netready
 * security_scan


The code to run these test cases is hosted in the repository of the project.


Functest framework
==================

Functest is as a framework.

Historically Functest is released as a docker file, including tools, scripts and
a CLI to prepare the environment and run tests.
It simplifies the integration of external test suites in CI pipeline and provide
commodity tools to collect and display results.

Since Colorado, test categories also known as tiers have been created to
group similar tests, provide consistent sub-lists and at the end optimize
test duration for CI (see How To section).

The definition of the tiers has been agreed by the testing working group.

The tiers are:
  * healthcheck
  * smoke
  * features
  * components
  * performance
  * vnf
  * stress

Functest abstraction classes
============================

In order to harmonize test integration, abstraction classes have been
introduced:

 * testcase: base for any test case
 * unit: run unti tests as test case
 * feature: abstraction for feature project
 * vnf: abstraction for vnf onboarding

The goal is to unify the way to run tests in Functest.

Feature, unit and vnf_base inherit from testcase::

              +-----------------------------------------+
              |                                         |
              |         TestCase                        |
              |                                         |
              |         - init()                        |
              |         - run()                         |
              |         - publish_report()              |
              |         - check_criteria()              |
              |                                         |
              +-----------------------------------------+
                 |               |
                 V               V
  +--------------------+   +--------------+   +--------------------------+
  |                    |   |              |   |                          |
  |    feature         |   |    unit      |   |      vnf                 |
  |                    |   |              |   |                          |
  |                    |   |              |   |  - prepare()             |
  |  - execute()       |   |              |   |  - deploy_orchestrator() |
  | BashFeature class  |   |              |   |  - deploy_vnf()          |
  |                    |   |              |   |  - test_vnf()            |
  |                    |   |              |   |  - clean()               |
  +--------------------+   +--------------+   +--------------------------+


Testcase
========
.. raw:: html
   :url: http://artifacts.opnfv.org/functest/docs/apidoc/functest.core.testcase.html

Feature
=======
.. raw:: html
   :url: http://artifacts.opnfv.org/functest/docs/apidoc/functest.core.feature.html

Unit
====
.. raw:: html
   :url: http://artifacts.opnfv.org/functest/docs/apidoc/functest.core.unit.html

VNF
===
.. raw:: html
   :url: http://artifacts.opnfv.org/functest/docs/apidoc/functest.core.vnf.html


see `Functest framework overview`_ to get code samples


Functest util classes
=====================

In order to simplify the creation of test cases, Functest develops also some
functions that can be used by any feature or internal test cases.
Several features are supported such as logger, configuration management and
Openstack capabilities (snapshot, clean, tacker,..).
These functions can be found under <repo>/functest/utils and can be described as
follows::

 functest/utils/
 |-- config.py
 |-- constants.py
 |-- env.py
 |-- functest_utils.py
 |-- openstack_clean.py
 |-- openstack_snapshot.py
 |-- openstack_tacker.py
 `-- openstack_utils.py

Please note that it is possible to use snaps utils. SNAPS `[4]`_ is an OPNFV
project providing OpenStack utils.


Test API
========
Functest is using the Test collection framework and the test API developped by
the OPNFV community. See `OPNFV Test collection framework`_ for details.


Reporting
=========
A web page is automatically generated every day to display the status based on
jinja2 templates `[3]`_.


Dashboard
=========

Additional dashboarding is managed at the testing group level, see
`OPNFV Testing dashboard`_


=======
How TOs
=======

See `How to section`_ on Functest wiki


==========
References
==========

_`[1]`: http://artifacts.opnfv.org/functest/docs/configguide/index.html Functest configuration guide

_`[2]`: http://artifacts.opnfv.org/functest/docs/userguide/index.html functest user guide

_`[3]`: https://git.opnfv.org/cgit/releng/tree/utils/test/reporting

_`[4]`: https://git.opnfv.org/snaps/

_`Functest framework overview` : http://testresults.opnfv.org/functest/framework/index.html

_`OPNFV Test collection framework`: TODO

_`OPNFV Testing dashboard`: https://opnfv.biterg.io/goto/283dba93ca18e95964f852c63af1d1ba

_`How to section`: https://wiki.opnfv.org/pages/viewpage.action?pageId=7768932

IRC support chan: #opnfv-functest
