
Troubleshooting
===============
VIM
---
vPing_SSH
^^^^^^^^^

vPing should work on all the scenarios. In case of timeout, check your network
connectivity. The test case creates its own security group to allow SSH access,
check your network settings and your security rules.


vPing_userdata
^^^^^^^^^^^^^^

Cloud-init in not supported on scenario dealing with ONOS.

Tempest
^^^^^^^

In the upstream OpenStack CI all the Tempest test cases are supposed to pass.
If some test cases fail in an OPNFV deployment, the reason is very probably one
of the following::

 +-----------------------------+------------------------------------------------+
 | Error                       | Details                                        |
 +=============================+================================================+
 | Resources required for test | Such resources could be e.g. an external       |
 | case execution are missing  | network and access to the management subnet    |
 |                             | (adminURL) from the Functest docker container. |
 +-----------------------------+------------------------------------------------+
 | OpenStack components or     | Check running services in the controller and   |
 | services are missing or not | compute nodes (e.g. with "systemctl" or        |
 | configured properly         | "service" commands). Configuration parameters  |
 |                             | can be verified from related .conf files       |
 |                             | located under /etc/<component> directories.    |
 +-----------------------------+------------------------------------------------+
 | Some resources required for | The tempest.conf file, automatically generated |
 | execution test cases are    | by Rally in Functest, does not contain all the |
 | missing                     | needed parameters or some parameters are not   |
 |                             | set properly.                                  |
 |                             | The tempest.conf file is located in /home/opnfv|
 |                             | /.rally/tempest/for-deployment-<UUID> in       |
 |                             | Functest container                             |
 |                             | Use "rally deployment list" command in order to|
 |                             | check UUID of current deployment.              |
 +-----------------------------+------------------------------------------------+


When some Tempest test case fails, captured traceback and possibly also related
REST API requests/responses are output to the console.
More detailed debug information can be found from tempest.log file stored into
related Rally deployment folder.


Rally
^^^^^

Same error causes than for Tempest mentioned above may lead to error in Rally.

Controllers
-----------

ODL
^^^
2 versions are supported in Brahmaputra depending on the scenario:
 * Lithium
 * Berylium

The upstream test suites have not been adapted, so you may get 18 or 15 tests
passed on 18 depending on your configuration. The 3 testcases are partly failed
due to wrong return code.

ONOS
^^^^

TODO

OpenContrail
^^^^^^^^^^^^


Feature
-------

vIMS
^^^^
vIMS deployment may fail for several reasons, the most frequent ones are
described in the following table:

+===================================+====================================+
| Error                             |  Comments                          |
+-----------------------------------+------------------------------------+
| Keystone admin API  not reachable | Impossible to create vIMS user and |
|                                   | tenant                             |
+-----------------------------------+------------------------------------+
| Impossible to retrieve admin role | Impossible to create vIMS user and |
| id                                | tenant                             |
+-----------------------------------+------------------------------------+
| Error when uploading image from   | impossible to deploy VNF           |
| OpenStack to glance               |                                    |
+-----------------------------------+------------------------------------+
| Cinder quota cannot be updated    | Default quotas not sufficient, they|
|                                   | are adapted in the script          |
+-----------------------------------+------------------------------------+
| Impossible to create a volume     | VNF cannot be deployed             |
+-----------------------------------+------------------------------------+
| SSH connection issue between the  | if vPing test fails, vIMS test will|
| Test container and the VM         | fail...                            |
+-----------------------------------+------------------------------------+
| No Internet access from a VM      | the VMs of the VNF must have an    |
|                                   | external access to Internet        |
+-----------------------------------+------------------------------------+


Promise
^^^^^^^

TODO
