.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

=======
License
=======

OPNFV Euphrates release note for Functest Docs
(c) by Jose Lausuch (Suse)

OPNFV Euphrates release note for Functest Docs
are licensed under a Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this.
If not, see <http://creativecommons.org/licenses/by/4.0/>.

=============================================
OPNFV Euphrates 5.0 release note for Functest
=============================================

Abstract
========

This document describes the release notes of the Functest project.


OPNFV Euphrates Release
======================

Functest deals with functional testing of the OPNFV solution.
It includes test cases developed within the project, test cases developed in
other OPNFV projects and it als intgrates test cases from other upstream
communities.

The internal test cases are:

 * connection_check
 * api_check
 * snaps_health_check
 * vping_ssh
 * vping_userdata
 * tempest_smoke_serial
 * refstack_defcore
 * snaps_smoke
 * rally_sanity
 * odl
 * tempest_full_parallel
 * rally_full
 * cloudify_ims

The OPNFV projects integrated into Functest framework for automation are:

 * barometer
 * bgpvpn
 * doctor
 * domino
 * fds
 * multisite
 * onos
 * odl-sfc
 * odl-netvirt
 * parser
 * promise
 * security scan
 * orchestra_ims
 * orchestra_clearwaterims
 * vyos_vrouter


Release Data
============

+--------------------------------------+--------------------------------------+
| **Project**                          | functest                             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo/tag**                         | opnfv-5.0.0                          |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | Euphrates service release            |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | October 20th 2017                    |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | Euphrates first release              |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Deliverables
============

Software
--------

 Functest Docker images:
 * https://hub.docker.com/r/opnfv/functest
 * https://hub.docker.com/r/opnfv/functest-healtcheck
 * https://hub.docker.com/r/opnfv/functest-smoke
 * https://hub.docker.com/r/opnfv/functest-features
 * https://hub.docker.com/r/opnfv/functest-components
 * https://hub.docker.com/r/opnfv/functest-vnf
 * https://hub.docker.com/r/opnfv/functest-parser
 * https://hub.docker.com/r/opnfv/functest-restapi

 TestAPI Docker image:
 * https://hub.docker.com/r/opnfv/testapi

Docker tag to be pulled: opnfv-5.0.0

Documents
---------

 - Installation/configuration guide: http://docs.opnfv.org/en/stable-euphrates/submodules/functest/docs/testing/user/configguide/index.html

 - User Guide: http://docs.opnfv.org/en/stable-euphrates/submodules/functest/docs/testing/user/userguide/index.html

 - Developer Guide: http://docs.opnfv.org/en/stable-euphrates/submodules/functest/docs/testing/developer/devguide/index.html

 - API Docs: http://testresults.opnfv.org/functest/apidoc/apidoc/functest.html

 - Functest Framework presentation: http://testresults.opnfv.org/functest/framework/index.html


Version change
==============

Functest delivers now light weigth Docker images based on Alpine 3.6. The test cases are grouped into several categories
or tiers and must be run from the corresponding container. For example, to run the test case healtcheck, the image
opnfv/functest-healtcheck shall be used. The tiers and the test within them are explained in detail in the User Guide.

For ARM (aarch64), the former Ubuntu image opnfv/functest shall be used since there are not any Alpine images built
for this architecture yet. It will probably be supported for Euphrates 5.1.

The Parser test case has its own dedicated Docker image since it requires libraries released for OpenStack Pike and
Euphrates is based on Ocata.

The Docker images do not contain OS images (Cirros, Ubuntu, Centos, ..) any more. A script has been created under the
ci directory (download_images.sh) which contains all the needed images for all the test. This file can be modified by
the user since not all the images might be used. It must be executed before starting Functest and attach the needed
images as a Docker volume. See Configuration Guide for more information.

The requirements have been split into 3 files:
 * requirements.txt : lists all abstract dependencies of the OPNFV packages
 * test-requirements.txt : lists all abstract dependencies required for testing the OPNFV packages
 * upper-constraints.txt : lists all concrete dependencies required by Functest Docker container

OPNFV (test-)requirements.txt have been updated according to stable/ocata global-requirements.txt.
Functest uses (and completes) stable/ocata upper-constraints.txt in Dockerfiles and tox configuration.
The project relies on pbr, which injects injects requirements into the install_requires, tests_require and/or dependency_links
arguments to setup. It also supports conditional dependencies which can be added to the requirements (e.g. dnspython>=1.14.0;python_version=='2.7')

The way to manage logging has been centralized to a configuration file (logging.ini) which might be modified by the user.
By default, the output of executing the test cases is redirected to log files and is not displayed on the console, only result
messages and summary tables are displayed.

The framework has been refactored and all the test cases inherit from a core class TestCase. For Feature projects who develop
test cases, 2 sub-classes have been created:
 - Feature: it implements all the needed functions and the developer must only overwritte the method "execute" (e.g. Barometer)
 - BashFeature: it is used if the third party test case is a shell script. This way, the execution command must be specified in
 testcases.yaml as the argument (e.g. Domino, Doctor)




Euphrates known restrictions/issues
===================================
+-----------+-----------+----------------------------------------------+
| Installer | Scenario  |  Issue                                       |
+===========+===========+==============================================+
|           |           |  The test cases belonging to the VNF tier    |
|    any    |    any    |  have been only tested on os-nosdn-nofeature |
|           |           |  scenarios.                                  |
+-----------+-----------+----------------------------------------------+
|    any    |    any    |  The migration and live migration tests in   |
|           |           |  Rally have been disabled for NOHA scenarios |
+-----------+-----------+----------------------------------------------+


Test and installer/scenario dependencies
========================================

It is not always possible to run all the test cases on all the scenarios.
The following table details the dependencies of the test cases per
scenario. The scenario dependencies (installer or scenario) are detailed
in https://git.opnfv.org/cgit/functest/tree/ci/testcases.yaml

Test results
============

Test results are available in:

 - test results logs: http://artifacts.opnfv.org

 - jenkins logs on CI: https://build.opnfv.org/ci/view/functest/

 - jenkins logs on ARM CI: https://build.opnfv.org/ci/view/armband/



Open JIRA tickets
=================

+------------------+-----------------------------------------------+
|   JIRA           |         Description                           |
+==================+===============================================+
|                  |                                               |
|                  |                                               |
+------------------+-----------------------------------------------+

All the tickets that are not blocking have been fixed or postponed
the next release.


Useful links
============

 - wiki project page: https://wiki.opnfv.org/opnfv_functional_testing

 - wiki Functest Euphrates page: https://wiki.opnfv.org/display/functest/5.+Euphrates

 - Functest repo: https://git.opnfv.org/cgit/functest

 - Functest CI dashboard: https://build.opnfv.org/ci/view/functest/

 - JIRA dashboard: https://jira.opnfv.org/secure/Dashboard.jspa?selectPageId=10611

 - Functest IRC chan: #opnfv-functest

 - Reporting page: http://testresults.opnfv.org/reporting/euphrates.html

 - Functest test configuration: https://git.opnfv.org/functest/tree/functest/ci/testcases.yaml?h=stable/euphrates
