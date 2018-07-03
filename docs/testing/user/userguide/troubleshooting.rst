.. SPDX-License-Identifier: CC-BY-4.0

Troubleshooting
===============

This section gives some guidelines about how to troubleshoot the test cases
owned by Functest.

**IMPORTANT**: As in the previous section, the steps defined below must be
executed inside the Functest Docker container and after sourcing the OpenStack
credentials::

    . $creds

or::

    source /home/opnfv/functest/conf/env_file

VIM
---

This section covers the test cases related to the VIM (healthcheck, vping_ssh,
vping_userdata, tempest_smoke, tempest_full, rally_sanity, rally_full).

vPing common
^^^^^^^^^^^^
For both vPing test cases (**vPing_ssh**, and **vPing_userdata**), the first
steps are similar:

    * Create Glance image
    * Create Network
    * Create Security Group
    * Create Instances

After these actions, the test cases differ and will be explained in their
respective section.

These test cases can be run inside the container, using new Functest CLI as
follows::

    $ run_tests -t vping_ssh
    $ run_tests -t vping_userdata

The Functest CLI is designed to route a call to the corresponding internal
python scripts, located in paths::

    /usr/lib/python2.7/site-packages/functest/opnfv_tests/openstack/vping/vping_ssh.py
    /usr/lib/python2.7/site-packages/functest/opnfv_tests/openstack/vping/vping_userdata.py

Notes:

  #. There is one difference, between the Functest CLI based test case
     execution compared to the earlier used Bash shell script, which is
     relevant to point out in troubleshooting scenarios:

         The Functest CLI does **not yet** support the option to suppress
         clean-up of the generated OpenStack resources, following the execution
         of a test case.

     Explanation: After finishing the test execution, the corresponding
     script will remove, by default, all created resources in OpenStack
     (image, instances, network and security group). When troubleshooting,
     it is advisable sometimes to keep those resources in case the test
     fails and a manual testing is needed.

     It is actually still possible to invoke test execution, with suppression
     of OpenStack resource cleanup, however this requires invocation of a
     **specific Python script:** 'run_tests'.
     The `OPNFV Functest Developer Guide`_ provides guidance on the use of that
     Python script in such troubleshooting cases.

Some of the common errors that can appear in this test case are::

    vPing_ssh- ERROR - There has been a problem when creating the neutron network....

This means that there has been some problems with Neutron, even before creating
the instances. Try to create manually a Neutron network and a Subnet to see if
that works. The debug messages will also help to see when it failed (subnet and
router creation). Example of Neutron commands (using 10.6.0.0/24 range for
example)::

    neutron net-create net-test
    neutron subnet-create --name subnet-test --allocation-pool start=10.6.0.2,end=10.6.0.100 \
    --gateway 10.6.0.254 net-test 10.6.0.0/24
    neutron router-create test_router
    neutron router-interface-add <ROUTER_ID> test_subnet
    neutron router-gateway-set <ROUTER_ID> <EXT_NET_NAME>

Another related error can occur while creating the Security Groups for the
instances::

    vPing_ssh- ERROR - Failed to create the security group...

In this case, proceed to create it manually. These are some hints::

    neutron security-group-create sg-test
    neutron security-group-rule-create sg-test --direction ingress --protocol icmp \
    --remote-ip-prefix 0.0.0.0/0
    neutron security-group-rule-create sg-test --direction ingress --ethertype IPv4 \
    --protocol tcp --port-range-min 80 --port-range-max 80 --remote-ip-prefix 0.0.0.0/0
    neutron security-group-rule-create sg-test --direction egress --ethertype IPv4 \
    --protocol tcp --port-range-min 80 --port-range-max 80 --remote-ip-prefix 0.0.0.0/0

The next step is to create the instances. The image used is located in
*/home/opnfv/functest/data/cirros-0.4.0-x86_64-disk.img* and a Glance image is
created with the name **functest-vping**. If booting the instances fails (i.e.
the status is not **ACTIVE**), you can check why it failed by doing::

    nova list
    nova show <INSTANCE_ID>

It might show some messages about the booting failure. To try that manually::

    nova boot --flavor m1.small --image functest-vping --nic net-id=<NET_ID> nova-test

This will spawn a VM using the network created previously manually.
In all the OPNFV tested scenarios from CI, it never has been a problem with the
previous actions. Further possible problems are explained in the following
sections.


vPing_SSH
^^^^^^^^^
This test case creates a floating IP on the external network and assigns it to
the second instance **opnfv-vping-2**. The purpose of this is to establish
a SSH connection to that instance and SCP a script that will ping the first
instance. This script is located in the repository under
/usr/lib/python2.7/site-packages/functest/opnfv_tests/openstack/vping/ping.sh
and takes an IP as a parameter. When the SCP is completed, the test will do a
SSH call to that script inside the second instance. Some problems can happen
here::

    vPing_ssh- ERROR - Cannot establish connection to IP xxx.xxx.xxx.xxx. Aborting

If this is displayed, stop the test or wait for it to finish, if you have used
the special method of test invocation with specific supression of OpenStack
resource clean-up, as explained earler. It means that the Container can not
reach the Public/External IP assigned to the instance **opnfv-vping-2**. There
are many possible reasons, and they really depend on the chosen scenario. For
most of the ODL-L3 and ONOS scenarios this has been noticed and it is a known
limitation.

First, make sure that the instance **opnfv-vping-2** succeeded to get an IP
from the DHCP agent. It can be checked by doing::

    nova console-log opnfv-vping-2

If the message *Sending discover* and *No lease, failing* is shown, it probably
means that the Neutron dhcp-agent failed to assign an IP or even that it was
not responding. At this point it does not make sense to try to ping the
floating IP.

If the instance got an IP properly, try to ping manually the VM from the
container::

    nova list
    <grab the public IP>
    ping <public IP>

If the ping does not return anything, try to ping from the Host where the
Docker container is running. If that solves the problem, check the iptable
rules because there might be some rules rejecting ICMP or TCP traffic
coming/going from/to the container.

At this point, if the ping does not work either, try to reproduce the test
manually with the steps described above in the vPing common section with the
addition::

    neutron floatingip-create <EXT_NET_NAME>
    nova floating-ip-associate nova-test <FLOATING_IP>


Further troubleshooting is out of scope of this document, as it might be due to
problems with the SDN controller. Contact the installer team members or send an
email to the corresponding OPNFV mailing list for more information.



vPing_userdata
^^^^^^^^^^^^^^
This test case does not create any floating IP neither establishes an SSH
connection. Instead, it uses nova-metadata service when creating an instance
to pass the same script as before (ping.sh) but as 1-line text. This script
will be executed automatically when the second instance **opnfv-vping-2** is
booted.

The only known problem here for this test to fail is mainly the lack of support
of cloud-init (nova-metadata service). Check the console of the instance::

    nova console-log opnfv-vping-2

If this text or similar is shown::

    checking http://169.254.169.254/2009-04-04/instance-id
    failed 1/20: up 1.13. request failed
    failed 2/20: up 13.18. request failed
    failed 3/20: up 25.20. request failed
    failed 4/20: up 37.23. request failed
    failed 5/20: up 49.25. request failed
    failed 6/20: up 61.27. request failed
    failed 7/20: up 73.29. request failed
    failed 8/20: up 85.32. request failed
    failed 9/20: up 97.34. request failed
    failed 10/20: up 109.36. request failed
    failed 11/20: up 121.38. request failed
    failed 12/20: up 133.40. request failed
    failed 13/20: up 145.43. request failed
    failed 14/20: up 157.45. request failed
    failed 15/20: up 169.48. request failed
    failed 16/20: up 181.50. request failed
    failed 17/20: up 193.52. request failed
    failed 18/20: up 205.54. request failed
    failed 19/20: up 217.56. request failed
    failed 20/20: up 229.58. request failed
    failed to read iid from metadata. tried 20

it means that the instance failed to read from the metadata service. Contact
the Functest or installer teams for more information.


Tempest
^^^^^^^

In the upstream OpenStack CI all the Tempest test cases are supposed to pass.
If some test cases fail in an OPNFV deployment, the reason is very probably one
of the following

+----------------------------+------------------------------------------------+
| Error                      | Details                                        |
+============================+================================================+
| Resources required for     | Such resources could be e.g. an external       |
| testcase execution are     | network and access to the management subnet    |
| missing                    | (adminURL) from the Functest docker container. |
+----------------------------+------------------------------------------------+
| OpenStack components or    | Check running services in the controller and   |
| services are missing or    | compute nodes (e.g. with "systemctl" or        |
| not configured properly    | "service" commands).                           |
|                            | Configuration parameters can be verified from  |
|                            | the related .conf files located under          |
|                            | '/etc/<component>' directories.                |
+----------------------------+------------------------------------------------+
| Some resources required    | The tempest.conf file, automatically generated |
| for execution test cases   | by Rally in Functest, does not contain all the |
| are missing                | needed parameters or some parameters are not   |
|                            | set properly.                                  |
|                            | The tempest.conf file is located in directory  |
|                            | 'root/.rally/verification/verifier-<UUID>      |
|                            | /for-deployment-<UUID>'                        |
|                            | in the Functest Docker container. Use the      |
|                            | "rally deployment list" command in order to    |
|                            | check the UUID of the current deployment.      |
+----------------------------+------------------------------------------------+


When some Tempest test case fails, captured traceback and possibly also the
related REST API requests/responses are output to the console. More detailed
debug information can be found from tempest.log file stored into related Rally
deployment folder.

Functest offers a possibility to test a customized list of Tempest test cases.
To enable that, add a new entry in docker/components/testcases.yaml on the
"components" container with the following content::

    -
        case_name: tempest_custom
        project_name: functest
        criteria: 100
        blocking: false
        description: >-
            The test case allows running a customized list of tempest
            test cases
        dependencies:
            installer: ''
            scenario: ''
        run:
            module: 'functest.opnfv_tests.openstack.tempest.tempest'
            class: 'TempestCustom'

Also, a list of the Tempest test cases must be provided to the container or
modify the existing one in
/usr/lib/python2.7/site-packages/functest/opnfv_tests/openstack/tempest/custom_tests/test_list.txt

Example of custom list of tests 'my-custom-tempest-tests.txt'::

    tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basic_ops[compute,id-7fff3fb3-91d8-4fd0-bd7d-0204f1f180ba,network,smoke]
    tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops[compute,id-f323b3ba-82f8-4db7-8ea6-6a895869ec49,network,smoke]

This is an example of running a customized list of Tempest tests in Functest::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
      -v $(pwd)/images:/home/opnfv/functest/images \
      -v $(pwd)/my-custom-testcases.yaml:/usr/lib/python2.7/site-packages/functest/ci/testcases.yaml \
      -v $(pwd)/my-custom-tempest-tests.txt:/usr/lib/python2.7/site-packages/functest/opnfv_tests/openstack/tempest/custom_tests/test_list.txt \
      opnfv/functest-components run_tests -t tempest_custom


Rally
^^^^^

The same error causes which were mentioned above for Tempest test cases, may
also lead to errors in Rally as well.

Possible scenarios are:
 * authenticate
 * glance
 * cinder
 * heat
 * keystone
 * neutron
 * nova
 * quotas
 * vm

To know more about what those scenarios are doing, they are defined in
directory:
/usr/lib/python2.7/site-packages/functest/opnfv_tests/openstack/rally/scenario
For more info about Rally scenario definition please refer to the Rally
official documentation. `[3]`_

To check any possible problems with Rally, the logs are stored under
*/home/opnfv/functest/results/rally/* in the Functest Docker container.

.. _`[3]`: https://rally.readthedocs.org/en/latest/index.html

Controllers
-----------

Opendaylight
^^^^^^^^^^^^

If the Basic Restconf test suite fails, check that the ODL controller is
reachable and its Restconf module has been installed.

If the Neutron Reachability test fails, verify that the modules
implementing Neutron requirements have been properly installed.

If any of the other test cases fails, check that Neutron and ODL have
been correctly configured to work together. Check Neutron configuration
files, accounts, IP addresses etc.).


Features
--------

Please refer to the dedicated feature user guides for details.


VNF
---

cloudify_ims
^^^^^^^^^^^^
vIMS deployment may fail for several reasons, the most frequent ones are
described in the following table:

+-----------------------------------+------------------------------------+
| Error                             |  Comments                          |
+===================================+====================================+
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
| Test Docker container and the VM  | fail...                            |
+-----------------------------------+------------------------------------+
| No Internet access from the VM    | the VMs of the VNF must have an    |
|                                   | external access to Internet        |
+-----------------------------------+------------------------------------+
| No access to OpenStack API from   | Orchestrator can be installed but  |
| the VM                            | the vIMS VNF installation fails    |
+-----------------------------------+------------------------------------+

Please note that this test case requires resources (8 VM (2Go) + 1 VM (4Go)),
it is there fore not recommended to run it on a light configuration.

.. _`OPNFV Functest Developer Guide`:  http://artifacts.opnfv.org/functest/docs/testing_developer_devguide/index.html#
