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
 * odl
 * tempest_smoke
 * tempest_horizon
 * tempest_neutron
 * tempest_cinder
 * tempest_keystone
 * tempest_heat
 * rally_sanity
 * refstack_defcore
 * patrole
 * networking-bgpvpn
 * networking-sfc
 * tempest_barbican
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
 * odl-sfc
 * barometer
 * stor4nfv_os

Kubernetes
----------

The internal test cases are:

 * k8s_quick
 * k8s_smoke
 * k8s_conformance
 * xrally_kubernetes
 * kube_hunter
 * kube_bench_master
 * kube_bench_node
 * xrally_kubernetes_full
 * k8s_vims
 * helm_vims
 * cnf_conformance

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
 * https://hub.docker.com/r/opnfv/functest-vnf
 * https://hub.docker.com/r/opnfv/functest-smoke-cntt
 * https://hub.docker.com/r/opnfv/functest-benchmarking-cntt

 Functest Docker images (Kubernetes):

 * https://hub.docker.com/r/opnfv/functest-kubernetes-healthcheck
 * https://hub.docker.com/r/opnfv/functest-kubernetes-smoke
 * https://hub.docker.com/r/opnfv/functest-kubernetes-security
 * https://hub.docker.com/r/opnfv/functest-kubernetes-benchmarking
 * https://hub.docker.com/r/opnfv/functest-kubernetes-cnf

Docker tag for hunter: hunter

Documents
---------

 * Functest Guides: https://functest.readthedocs.io/en/stable-hunter/
 * API Docs: https://functest-api.readthedocs.io/en/stable-hunter/

Version change
==============

Key changes
-----------

 * update testcases and containers to `OpenStack Rocky`_ and to
   `Kubernetes v1.13.5`_
 * add rally_full in Installer daily jobs (including the virtual deployments)
 * harden the VNF testcases and decrease their requirements (e.g. image size)
 * verify all patches before merge via functional gates
 * reorder the testcases to run them in parallel
 * publish new `Ansible playbooks`_ to easily deploy the OPNFV CI/CD toolchain
 * port Functest on `Raspberry PI`_

.. _`OpenStack Rocky`: https://github.com/openstack/requirements/blob/stable/rocky/upper-constraints.txt
.. _`Kubernetes v1.13.5`: https://github.com/kubernetes/kubernetes/tree/v1.13.5
.. _`Ansible playbooks`: https://wiki.opnfv.org/pages/viewpage.action?pageId=32015004
.. _`Raspberry PI`: https://wiki.opnfv.org/display/functest/Run+Functest+containers+on+Raspberry+PI

Key benefits
------------

 * the enduser can easily deploy its own `Functest toolchains`_ in few commands
 * everyone can pick stable Functest rolling releases (latest included)
 * Functest can verify VIM in production even on `Raspberry PI`_
 * all testcases can run in parallel (tested with 5 executors in our gates)

.. _`Functest toolchains`: https://wiki.opnfv.org/pages/viewpage.action?pageId=32015004

Code quality
------------

 * pylint: 10.00/10
 * code coverage: 71%

Useful links
============

 * wiki project page: https://wiki.opnfv.org/display/functest/Opnfv+Functional+Testing
 * Functest git repository: https://github.com/opnfv/functest
 * Functest CI dashboard: https://build.opnfv.org/ci/view/functest/
 * JIRA dashboard: https://jira.opnfv.org/secure/Dashboard.jspa?selectPageId=10611
 * Functest IRC channel: #opnfv-functest
 * Reporting page: http://testresults.opnfv.org/reporting/master/functest/functest.html
