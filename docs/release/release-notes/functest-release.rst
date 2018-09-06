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
 * tenantnetwork1
 * tenantnetwork2
 * vmready1
 * vmready2
 * singlevm1
 * singlevm2
 * vping_ssh
 * vping_userdata
 * cinder_test
 * api_check
 * snaps_health_check
 * odl
 * tempest_smoke
 * neutron-tempest-plugin-api
 * rally_sanity
 * refstack_defcore
 * patrole
 * snaps_smoke
 * neutron_trunk
 * networking-bgpvpn
 * networking-sfc
 * barbican
 * tempest_full
 * tempest_scenario
 * rally_full
 * cloudify
 * cloudify_ims
 * heat_ims
 * vyos_vrouter
 * juju_epc
 * vgpu

The OPNFV projects integrated into Functest framework for automation are:

 * doctor
 * bgpvpn
 * odl-sfc
 * barometer
 * fds
 * stor4nfv_os

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
 * https://hub.docker.com/r/opnfv/functest-benchmarking
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

 * tenantnetwork1
 * tenantnetwork2
 * vmready1
 * vmready2
 * singlevm1
 * singlevm2
 * cinder_test
 * neutron-tempest-plugin-api
 * networking-bgpvpn
 * networking-sfc
 * barbican
 * vmtp
 * shaker
 * tempest_scenario
 * cloudify
 * heat_ims
 * vgpu

Key changes
-----------

 * update test cases and containers to `OpenStack Queens`_ and to
   `Kubernetes v1.11`_
 * define new scenarios to ease writing testcases vs OpenStack
 * allow parallel testing
 * publish new Jenkins jobs to help any user to build his own CI/CD chain
 * remove all OPNFV logics
 * support VIO (VMware Integrated OpenStack)

.. _`OpenStack Queens`: https://raw.githubusercontent.com/openstack/requirements/stable/pike/upper-constraints.txt
.. _`Kubernetes v1.11`: https://github.com/kubernetes/kubernetes/tree/v1.11.2

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
