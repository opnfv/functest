.. SPDX-License-Identifier: CC-BY-4.0

======================================
OPNFV hunter release note for Functest
======================================

Abstract
========

This document contains the release notes of the Functest project.

OPNFV hunter Release
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
| **Repository branch**                | stable/hunter                        |
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

Docker tag for hunter: hunter

Documents
---------

 * Config Guide: https://functest.readthedocs.io/projects/configguide/en/stable-hunter/
 * User Guide: https://functest.readthedocs.io/projects/userguide/en/stable-hunter/
 * Developer Guide: https://functest.readthedocs.io/projects/devguide/en/stable-hunter/
 * API Docs: https://functest.readthedocs.io/en/stable-hunter/

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

 * update test cases and containers to `OpenStack Rocky`_ and to
   `Kubernetes v1.11.2`_
 * define new scenarios to ease writing testcases vs OpenStack
 * isolate all resources created in different tenants
 * fully remove all OPNFV logics
 * publish new Jenkins jobs
 * support VIO (VMware Integrated OpenStack) and arm64 for Kubernetes
 * reduce Functest Kubernetes image sizes
 * add tempest_full and tempest_scenario in all daily jobs
 * include benchmarking tools such as Vmtp ans Shaker
 * increase functional scope by adding bgpvpn and sfc tempest plugins

.. _`OpenStack Rocky`: https://github.com/openstack/requirements/blob/stable/rocky/upper-constraints.txt
.. _`Kubernetes v1.11.2`: https://github.com/kubernetes/kubernetes/tree/v1.11.2

Key benefits
------------

 * the enduser can easily build its own toolchains by loading our Jenkins jobs
 * all developpers can easily verify their changes before merge
 * our testcases may be run vs VIM in production
 * all testcases can run in parallel to decrease the overall duration
 * Functest includes most of the OpenStack gate jobs

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
