.. _functest-userguide:

.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

=========================
OPNFV FUNCTEST user guide
=========================

.. toctree::
   :maxdepth: 2

Version history
===============
+------------+----------+------------------+----------------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**                      |
|            |          |                  |                                  |
+------------+----------+------------------+----------------------------------+
| 2016-08-17 | 1.0.0    | Juha Haapavirta  | Colorado release                 |
|            |          | Column Gaynor    |                                  |
+------------+----------+------------------+----------------------------------+
| 2017-01-23 | 1.0.1    | Morgan Richomme  | Adaptations for Danube           |
+------------+----------+------------------+----------------------------------+
| 2017-08-16 | 1.0.2    | Morgan Richomme  | Adaptations for Euphrates        |
+------------+----------+------------------+----------------------------------+


Introduction
============

The goal of this document is to describe the OPNFV Functest test cases and to
provide a procedure to execute them. In the OPNFV Danube system release,
a Functest CLI utility is introduced for an easier execution of test procedures.

**IMPORTANT**: It is assumed here that the Functest Docker container is already
properly deployed and that all instructions described in this guide are to be
performed from *inside* the deployed Functest Docker container.

.. include:: ./test_overview.rst

.. include:: ./test_details.rst

.. include:: ./runfunctest.rst

.. include:: ./test_results.rst

.. include:: ./reporting.rst

.. figure:: ../../../images/functest-reporting-status.png
   :align: center
   :alt: Functest reporting portal Fuel status page

.. include:: ./troubleshooting.rst


References
==========
`[1]`_: Functest configuration guide

`[2]`_: OpenStack Tempest documentation

`[3]`_: Rally documentation

`[4]`_: Functest in depth (Danube)

`[5]`_: Clearwater vIMS blueprint

`[6]`_: NIST web site

`[7]`_: OpenSCAP web site

`[8]`_: Refstack client

`[9]`_: Defcore

`[10]`_: OpenStack interoperability procedure

`[11]`_: Robot Framework web site

`[12]`_: Functest User guide

`[13]`_: SNAPS wiki

`[14]`_: vRouter

`[15]`_: Testing OpenStack Tempest part 1

`OPNFV main site`_: OPNFV official web site

`Functest page`_: Functest wiki page

IRC support chan: #opnfv-functest

.. _`[1]`: http://docs.opnfv.org/en/stable-danube/submodules/functest/docs/testing/user/configguide/index.html
.. _`[2]`: http://docs.openstack.org/developer/tempest/overview.html
.. _`[3]`: https://rally.readthedocs.org/en/latest/index.html
.. _`[4]`: http://events.linuxfoundation.org/sites/events/files/slides/Functest%20in%20Depth_0.pdf
.. _`[5]`: https://github.com/Orange-OpenSource/opnfv-cloudify-clearwater/blob/master/openstack-blueprint.yaml
.. _`[6]`: https://scap.nist.gov/
.. _`[7]`: https://github.com/OpenSCAP/openscap
.. _`[8]`: https://github.com/openstack/refstack-client
.. _`[9]`: https://github.com/openstack/defcore
.. _`[10]`: https://github.com/openstack/interop/blob/master/2016.08/procedure.rst
.. _`[11]`: http://robotframework.org/
.. _`[12]`: http://docs.opnfv.org/en/stable-danube/submodules/functest/docs/testing/user/userguide/index.html
.. _`[13]`: https://wiki.opnfv.org/display/PROJ/SNAPS-OO
.. _`[14]`: https://github.com/oolorg/opnfv-functest-vrouter
.. _`[15]`: https://aptira.com/testing-openstack-tempest-part-1/
.. _`OPNFV main site`: http://www.opnfv.org
.. _`Functest page`: https://wiki.opnfv.org/functest
.. _`OpenRC`: http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html
.. _`Rally installation procedure`: https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html
.. _`config_functest.yaml` : https://git.opnfv.org/cgit/functest/tree/functest/ci/config_functest.yaml
.. _`Functest reporting`: http://testresults.opnfv.org/reporting/functest/release/danube/index-status-fuel.html
