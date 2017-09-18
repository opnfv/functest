.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

===========================
Functest Installation Guide
===========================

.. toctree::
   :numbered:
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
| 2017-01-19 | 1.0.1    | Morgan Richomme  | Adaptations for Danube           |
|            |          |                  | * update testcase list           |
|            |          |                  | * update docker command          |
+------------+----------+------------------+----------------------------------+
| 2017-08-16 | 1.0.2    | Morgan Richomme  | Adaptations for Euphrates        |
+------------+----------+------------------+----------------------------------+

Introduction
============
This document describes how to install and configure Functest in OPNFV.

High level architecture
-----------------------

The high level architecture of Functest within OPNFV can be described as
follows::

 CIMC/Lights+out management               Admin  Mgmt/API  Public  Storage Private
                                           PXE
 +                                           +       +        +       +       +
 |                                           |       |        |       |       |
 |     +----------------------------+        |       |        |       |       |
 |     |                            |        |       |        |       |       |
 +-----+       Jumphost             |        |       |        |       |       |
 |     |                            |        |       |        |       |       |
 |     |   +--------------------+   |        |       |        |       |       |
 |     |   |                    |   |        |       |        |       |       |
 |     |   | Tools              |   +----------------+        |       |       |
 |     |   | - Rally            |   |        |       |        |       |       |
 |     |   | - Robot            |   |        |       |        |       |       |
 |     |   | - RefStack         |   |        |       |        |       |       |
 |     |   |                    |   |-------------------------+       |       |
 |     |   | Testcases          |   |        |       |        |       |       |
 |     |   | - VIM              |   |        |       |        |       |       |
 |     |   |                    |   |        |       |        |       |       |
 |     |   | - SDN Controller   |   |        |       |        |       |       |
 |     |   |                    |   |        |       |        |       |       |
 |     |   | - Features         |   |        |       |        |       |       |
 |     |   |                    |   |        |       |        |       |       |
 |     |   | - VNF              |   |        |       |        |       |       |
 |     |   |                    |   |        |       |        |       |       |
 |     |   +--------------------+   |        |       |        |       |       |
 |     |     Functest Docker        +        |       |        |       |       |
 |     |                            |        |       |        |       |       |
 |     |                            |        |       |        |       |       |
 |     |                            |        |       |        |       |       |
 |     +----------------------------+        |       |        |       |       |
 |                                           |       |        |       |       |
 |    +----------------+                     |       |        |       |       |
 |    |             1  |                     |       |        |       |       |
 +----+ +--------------+-+                   |       |        |       |       |
 |    | |             2  |                   |       |        |       |       |
 |    | | +--------------+-+                 |       |        |       |       |
 |    | | |             3  |                 |       |        |       |       |
 |    | | | +--------------+-+               |       |        |       |       |
 |    | | | |             4  |               |       |        |       |       |
 |    +-+ | | +--------------+-+             |       |        |       |       |
 |      | | | |             5  +-------------+       |        |       |       |
 |      +-+ | |  nodes for     |             |       |        |       |       |
 |        | | |  deploying     +---------------------+        |       |       |
 |        +-+ |  OPNFV         |             |       |        |       |       |
 |          | |                +------------------------------+       |       |
 |          +-+     SUT        |             |       |        |       |       |
 |            |                +--------------------------------------+       |
 |            |                |             |       |        |       |       |
 |            |                +----------------------------------------------+
 |            +----------------+             |       |        |       |       |
 |                                           |       |        |       |       |
 +                                           +       +        +       +       +
              SUT = System Under Test

Note connectivity to management network is not needed for most of the testcases.
But it may be needed for some specific snaps tests.

All the libraries and dependencies needed by all of the Functest tools are
pre-installed into the Docker images. This allows running Functest on any
platform.

The automated mechanisms inside the Functest Docker container will:

  * Retrieve OpenStack credentials
  * Prepare the environment according to the System Under Test (SUT)
  * Perform the appropriate functional tests
  * Push the test results into the OPNFV test result database

This Docker image can be integrated into CI or deployed independently.

Please note that the Functest Docker container has been designed for OPNFV,
however, it would be possible to adapt it to any OpenStack based VIM +
controller environment, since most of the test cases are integrated from
upstream communities.

The functional test cases are described in the Functest User Guide `[2]`_

.. include:: ./prerequisites.rst

.. include:: ./configguide.rst

.. include:: ./ci.rst


References
==========

`[1]`_ : Keystone and public end point constraint

`[2]`_ : Functest User guide

`[3]`_ : Functest Jenkins jobs

`[4]`_ : Functest Configuration guide

`[5]`_ : OPNFV main site

`[6]`_ : Functest wiki page

IRC support channel: #opnfv-functest

.. _`[1]`: https://ask.openstack.org/en/question/68144/keystone-unable-to-use-the-public-endpoint/
.. _`[2]`: http://docs.opnfv.org/en/latest/submodules/functest/docs/testing/user/userguide/index.html
.. _`[3]`: https://git.opnfv.org/releng/tree/jjb/functest/functest-daily-jobs.yml
.. _`[4]`: http://docs.opnfv.org/en/latest/submodules/functest/docs/testing/user/configguide/index.html
.. _`[5]`: http://www.opnfv.org
.. _`[6]`: https://wiki.opnfv.org/functest
