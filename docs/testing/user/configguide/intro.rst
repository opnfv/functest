.. SPDX-License-Identifier: CC-BY-4.0

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

Note connectivity to management network is not needed for most of the
testcases. But it may be needed for some specific snaps tests.

All the libraries and dependencies needed by all of the Functest tools are
pre-installed into the Docker images. This allows running Functest on any
platform.

The automated mechanisms inside the Functest Docker containers will:

  * Prepare the environment according to the System Under Test (SUT)
  * Perform the appropriate functional tests
  * Push the test results into the OPNFV test result database (optional)

The OpenStack credentials file must be provided to the container.

These Docker images can be integrated into CI or deployed independently.

Please note that the Functest Docker images have been designed for OPNFV,
however, it would be possible to adapt them to any OpenStack based VIM +
controller environment, since most of the test cases are integrated from
upstream communities.

The functional test cases are described in the :ref:`functest-userguide`
