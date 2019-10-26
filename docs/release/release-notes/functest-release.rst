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
 * tempest_smoke
 * tempest_horizon
 * odl
 * neutron-tempest-plugin-api
 * tempest_cinder
 * rally_sanity
 * refstack_compute
 * refstack_object
 * refstack_platform
 * tempest_full
 * tempest_scenario
 * tempest_slow
 * patrole
 * barbican
 * neutron_trunk
 * networking-bgpvpn
 * networking-sfc
 * octavia
 * rally_full
 * rally_jobs
 * vmtp
 * shaker
 * cloudify
 * cloudify_ims
 * heat_ims
 * vyos_vrouter
 * juju_epc

Kubernetes
----------

The internal test cases are:

 * k8s_smoke
 * xrally_kubernetes
 * k8s_conformance

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
 * https://hub.docker.com/r/opnfv/functest-vnf

 Functest Docker images (Kubernetes):

 * https://hub.docker.com/r/opnfv/functest-kubernetes-healthcheck
 * https://hub.docker.com/r/opnfv/functest-kubernetes-smoke

Docker tag for master: latest

Documents
---------

 * Functest Guides: https://functest.readthedocs.io/en/latest/
 * API Docs: https://functest-api.readthedocs.io/en/latest/

Version change
==============

Key changes
-----------

 * update testcases and containers to `OpenStack master`_ and to
   `Kubernetes master`_

.. _`OpenStack master`: https://github.com/openstack/requirements/blob/master/upper-constraints.txt
.. _`Kubernetes master`: https://github.com/kubernetes/kubernetes

Key benefits
------------

 * the enduser can easily deploy its own `Functest toolchains`_ in few commands
 * everyone can pick stable Functest rolling releases (latest included)
 * Functest can verify VIM in production even on `Raspberry PI`_
 * all testcases can run in parallel (tested with 4 executors in our gates)
 * no remaining resources detected in our gates after multiple runs

.. _`Functest toolchains`: https://wiki.opnfv.org/pages/viewpage.action?pageId=32015004
.. _`Raspberry PI`: https://wiki.opnfv.org/display/functest/Run+Functest+containers+on+Raspberry+PI

Code quality
------------

 * pylint: 10.00/10
 * code coverage: 70%

Useful links
============

 * wiki project page: https://wiki.opnfv.org/display/functest/Opnfv+Functional+Testing
 * Functest git repository: https://github.com/opnfv/functest
 * Functest CI dashboard: https://build.opnfv.org/ci/view/functest/
 * JIRA dashboard: https://jira.opnfv.org/secure/Dashboard.jspa?selectPageId=10611
 * Functest IRC channel: #opnfv-functest
 * Reporting page: http://testresults.opnfv.org/reporting/master/functest/functest.html
