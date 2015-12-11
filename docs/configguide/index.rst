===============================================
OPNFV FUNCTEST configuration/installation guide
===============================================

.. contents::

------------
Introduction
------------

** DOCUMENT IS IN PROGRESS FOR BRAHMAPUTRA **

.. _prereqs:

-------------
Prerequisites
-------------

The installation of the OPNFV solution is out of scope of this document but can be found XXX.
In the rest of the document the OPNFV solution would be considered as the System Under Test (SUT).

The installation and configuration of the tools needed to perform the tests will be described in the following sections.

Since Arno SR1, the tools are automatically installed. Manual sourcing of OpenStack credentials is no more required if you are fully integrated in the continuous integration.
A script has been added to automatically retrieve the credentials.
However, if you still install manually functest, you will need to source the rc file on the machine you are running the tests.
More details will be provided in the configuration section.

.. _pharos: https://wiki.opnfv.org/pharos

It is recommended to install the different tools on the jump host server as defined in the pharos_ project.

For functest, the following libraries are needed. You can install them either with yum install or apt-get install, depending on your operating system:
 * python-pip
 * python-dev
 * libffi-dev
 * libxml2-dev
 * libxslt1-dev

You will also need some Python modules:
 * sudo pip install GitPython
 * sudo pip install python-novaclient
 * sudo pip install python-neutronclient
 * sudo pip install python-glanceclient
 * sudo pip install python-keystoneclient


The high level architecture can be described as follow::

 CIMC/Lights+out management                  Admin     Private   Public   Storage
                                              PXE
                                                                   +
 +                                             +     IP_PRIV/24    |        |
 |                                             |         +         +        |
 |                                             |         |    IP_PUB/24     |
 |     +-----------------+                     |         |         +        |
 |     |                 |                     |         |         |        |
 +-----+  Jumpserver     |                     |         |         |        |
 |     |                 +---------------------+         |         |        |
 |     |                 |                     |         |         |        |
 |     |  +----------+   |                     |         |         |        |
 |     |  |  Rally   |   +---- --------------------------+         |        |
 |     |  |          |   |                     |         |         |        |
 |     |  |  Robot   |   |                     |         |         |        |
 |     |  |          |   |                     |         |         |        |
 |     |  |  vPing   |   |                     |         |         |        |
 |     |  |          |   |                     |         |         |        |
 |     |  | Tempest  |   |                     |         |         |        |
 |     |  +----------+   |                     |         |         |        |
 |     |   FuncTest      +-----------------------------------------+        |
 |     |                 |                     |         |         |        |
 |     |                 +--------------------------------------------------+
 |     |                 |                     |         |         |        |
 |     +-----------------+                     |         |         |        |
 |                                             |         |         |        |
 |    +----------------+                       |         |         |        |
 |    |             1  |                       |         |         |        |
 +----+ +--------------+-+                     |         |         |        |
 |    | |             2  |                     |         |         |        |
 |    | | +--------------+-+                   |         |         |        |
 |    | | |             3  |                   |         |         |        |
 |    | | | +--------------+-+                 |         |         |        |
 |    | | | |             4  |                 |         |         |        |
 |    +-+ | | +--------------+-+               |         |         |        |
 |      | | | |             5  +---------------+         |         |        |
 |      +-+ | |  nodes for     |               |         |         |        |
 |        | | |  deploying     +-------------------------+         |        |
 |        +-+ |  opnfv         |               |         |         |        |
 |          | |     SUT        +-----------------------------------+        |
 |          +-+                |               |         |         |        |
 |            |                +--------------------------------------------+
 |            +----------------+               |         |         |        |
 |                                             |         |         |        |
 |                                             +         +         +        +


.. _tooling_installation:

------------
Installation
------------

-------------
Configuration
-------------

-----------------
Integration in CI
-----------------



----------
References
----------

OPNFV main site: opnfvmain_.

OPNFV functional test page: opnfvfunctest_.

IRC support chan: #opnfv-testperf

.. _opnfvmain: http://www.opnfv.org
.. _opnfvfunctest: https://wiki.opnfv.org/opnfv_functional_testing
.. _`OpenRC`: http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html
.. _`Rally installation procedure`: https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html
.. _`config_test.py` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.py
.. _`config_functest.yaml` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.yaml
