.. SPDX-License-Identifier: CC-BY-4.0

Release Gating
==============

Thanks to the analysis of the offical OPNFV results and local tests (see
`Orange ONAP Openlab`_), Functest is trustable for verifying all OPNFV Fraser
installers and more generally classical OpenStack Pike and Kubernetes
deployments.

It should be noted that:

  * any test case in failure highlights side effects for end users
  * OpenStack scenarios wich don't pass tempest_smoke_serial break the
    upstream rules (and then decrease the overall quality) as all patches are
    tested vs tempest in OpenStack gating

.. _`Orange ONAP Openlab`: https://wiki.opnfv.org/pages/viewpage.action?pageId=13211751

.. toctree::

    apex.rst
    compass.rst
    daisy.rst
    fuel_amd64.rst
    fuel_arm64.rst
    joid.rst
