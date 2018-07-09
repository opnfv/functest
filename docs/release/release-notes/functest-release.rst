.. SPDX-License-Identifier: CC-BY-4.0

======================================
OPNFV master release note for Functest
======================================

Abstract
========

This document contains the release notes of the Functest project.

OPNFV master Release
====================

Functest deals with functional testing of the OPNFV solution.
It includes test cases developed within the project, test cases developed in
other OPNFV projects and it also integrates test cases from other upstream
communities.

OpenStack
---------

The internal test cases are:

 * connection_check
 * api_check
 * snaps_health_check
 * vping_ssh
 * vping_userdata
 * tempest_smoke_serial
 * rally_sanity
 * refstack_defcore
 * patrole
 * odl
 * snaps_smoke
 * neutron_trunk
 * tempest_full
 * rally_full
 * cloudify_ims
 * vyos_vrouter
 * juju_epc

The OPNFV projects integrated into Functest framework for automation are:

 * doctor
 * bgpvpn
 * odl-sfc
 * barometer
 * fds

Kubernetes
----------

The internal test cases are:

 * k8s_smoke
 * k8s_conformance

The OPNFV projects integrated into Functest framework for automation are:

 * stor4nfv
 * clover

Release Data
============

+--------------------------------------+--------------------------------------+
| **Project**                          | functest                             |
+--------------------------------------+--------------------------------------+
| **Repository branch**                | master                               |
+--------------------------------------+--------------------------------------+

Deliverables
============

Software
--------

 Functest Docker images (OpenStack):

 * https://hub.docker.com/r/opnfv/functest-healthcheck
 * https://hub.docker.com/r/opnfv/functest-smoke
 * https://hub.docker.com/r/opnfv/functest-features
 * https://hub.docker.com/r/opnfv/functest-components
 * https://hub.docker.com/r/opnfv/functest-vnf

 Functest Docker images (Kubernetes):

 * https://hub.docker.com/r/opnfv/functest-kubernetes-healthcheck
 * https://hub.docker.com/r/opnfv/functest-kubernetes-smoke
 * https://hub.docker.com/r/opnfv/functest-kubernetes-features

Docker tag for master: latest

Documents
---------

 * Config Guide: http://docs.opnfv.org/en/latest/submodules/functest/docs/testing/user/configguide/index.html
 * User Guide: http://docs.opnfv.org/en/latest/submodules/functest/docs/testing/user/userguide/index.html
 * Developer Guide: http://docs.opnfv.org/en/latest/submodules/functest/docs/testing/developer/devguide/index.html
 * API Docs: http://functest.readthedocs.io/en/latest/

Version change
==============

New test cases
--------------

 * neutron_trunk
 * patrole
 * juju_epc
 * k8s_smoke
 * k8s_conformance
 * stor4nfv
 * clover

Key changes
-----------

 * update test cases and containers to `OpenStack Pike`_
 * move the framework into a separate project: Xtesting_
 * ease running all containers thanks to default values
 * clean interfaces with OPNFV Installers and Features
 * rewrite all vnfs to allow multiple tests in parallel
 * fully support non-default region names and Keystone v3 domains
 * refactor all tempest-based test cases (e.g. refstack_defcore)
 * remove obsolete OpenStack and Functest utils
 * verify all changes via doc8 and yamllint too
 * generate reports for all tempest-based test cases

.. _`OpenStack Pike`: https://raw.githubusercontent.com/openstack/requirements/stable/pike/upper-constraints.txt
.. _Xtesting: http://xtesting.readthedocs.io/en/latest/

Key benefits
------------

 * the enduser can run all tests by setting only one input (EXTERNAL_NETWORK)
 * the developer can only work on the test suites without diving into CI/CD
   integration
 * both OpenStack and Kubernetes deployments can be verified
 * Functest test cases are trustable as they meet the best coding rules (unit
   tests, coverage, linters, etc.)
 * Functest can be reused in other projects (e.g.
   `ONS: Re-using OPNFV framework tests for LFN projects`_)

.. _`ONS: Re-using OPNFV framework tests for LFN projects`: https://wiki.lfnetworking.org/display/LN/LFN+Developer+Forum+Schedule?preview=/328197/328329/ONS-OPNFV%20framework%20tests%20for%20LFN%20projects.pdf

Code quality
------------

 * pylint: ~9.5/10
 * code coverage: ~70%

Useful links
============

 * wiki project page: https://wiki.opnfv.org/opnfv_functional_testing
 * Functest git repository: https://git.opnfv.org/cgit/functest
 * Functest CI dashboard: https://build.opnfv.org/ci/view/functest/
 * JIRA dashboard: https://jira.opnfv.org/secure/Dashboard.jspa?selectPageId=10611
 * Functest IRC channel: #opnfv-functest
 * Reporting page: http://testresults.opnfv.org/reporting/master/functest/functest.html
