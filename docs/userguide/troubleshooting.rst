.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

Troubleshooting
===============

This section gives some guidelines about how to troubleshoot the test cases
owned by Functest.

**IMPORTANT**: As in the previous section, the steps defined below must be
executed inside the Functest Docker container and after sourcing the OpenStack
credentials::

    . $creds

or::

    source /home/opnfv/functest/conf/openstack.creds

VIM
---

This section covers the test cases related to the VIM (healthcheck, vping_ssh,
vping_userdata, tempest_smoke_serial, tempest_full_parallel, rally_sanity,
rally_full).

vPing common
^^^^^^^^^^^^
For both vPing test cases (**vPing_ssh**, and **vPing_userdata**), the first steps are
similar:

    * Create Glance image
    * Create Network
    * Create Security Group
    * Create Instances

After these actions, the test cases differ and will be explained in their
respective section.

These test cases can be run inside the container, using new Functest CLI as follows::

    $ functest testcase run vping_ssh
    $ functest testcase run vping_userdata

The Functest CLI is designed to route a call to the corresponding internal
python scripts, located in paths:
*$repos_dir/functest/testcases/vPing/CI/libraries/vPing_ssh.py* and
*$repos_dir/functest/testcases/vPing/CI/libraries/vPing_userdata.py*

Notes:
  #. In this Colorado Funtest Userguide, the use of the Functest CLI is
     emphasized. The Functest CLI replaces the earlier Bash shell script
     *run_tests.sh*.

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
     **specific Python script:** '/home/opnfv/repos/functest/ci/run_test.py'.
     The `OPNFV Functest Developer Guide`_ provides guidance on the use of that
     Python script in such troubleshooting cases.

Some of the common errors that can appear in this test case are::

    vPing_ssh- ERROR - There has been a problem when creating the neutron network....

This means that there has been some problems with Neutron, even before creating the
instances. Try to create manually a Neutron network and a Subnet to see if that works.
The debug messages will also help to see when it failed (subnet and router creation).
Example of Neutron commands (using 10.6.0.0/24 range for example)::

    neutron net-create net-test
    neutron subnet-create --name subnet-test --allocation-pool start=10.6.0.2,end=10.6.0.100 \
    --gateway 10.6.0.254 net-test 10.6.0.0/24
    neutron router-create test_router
    neutron router-interface-add <ROUTER_ID> test_subnet
    neutron router-gateway-set <ROUTER_ID> <EXT_NET_NAME>

Another related error can occur while creating the Security Groups for the instances::

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
*/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img* and a Glance image is created
with the name **functest-vping**. If booting the instances fails (i.e. the status
is not **ACTIVE**), you can check why it failed by doing::

    nova list
    nova show <INSTANCE_ID>

It might show some messages about the booting failure. To try that manually::

    nova boot --flavor m1.small --image functest-vping --nic net-id=<NET_ID> nova-test

This will spawn a VM using the network created previously manually.
In all the OPNFV tested scenarios from CI, it never has been a problem with the
previous actions. Further possible problems are explained in the following sections.


vPing_SSH
^^^^^^^^^
This test case creates a floating IP on the external network and assigns it to
the second instance **opnfv-vping-2**. The purpose of this is to establish
a SSH connection to that instance and SCP a script that will ping the first
instance. This script is located in the repository under
*$repos_dir/functest/testcases/OpenStack/vPing/ping.sh* and takes an IP as
a parameter. When the SCP is completed, the test will do an SSH call to that script
inside the second instance. Some problems can happen here::

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
means that the Neutron dhcp-agent failed to assign an IP or even that it was not
responding. At this point it does not make sense to try to ping the floating IP.

If the instance got an IP properly, try to ping manually the VM from the container::

    nova list
    <grab the public IP>
    ping <public IP>

If the ping does not return anything, try to ping from the Host where the Docker
container is running. If that solves the problem, check the iptable rules because
there might be some rules rejecting ICMP or TCP traffic coming/going from/to the
container.

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
will be executed automatically when the second instance **opnfv-vping-2** is booted.

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

NOTE: Cloud-init in not supported on scenarios dealing with ONOS and the tests
have been excluded from CI in those scenarios.


Tempest
^^^^^^^

In the upstream OpenStack CI all the Tempest test cases are supposed to pass.
If some test cases fail in an OPNFV deployment, the reason is very probably one
of the following

+-----------------------------+-----------------------------------------------------+
| Error                       | Details                                             |
+=============================+=====================================================+
| Resources required for test | Such resources could be e.g. an external network    |
| case execution are missing  | and access to the management subnet (adminURL) from |
|                             | the Functest docker container.                      |
+-----------------------------+-----------------------------------------------------+
| OpenStack components or     | Check running services in the controller and compute|
| services are missing or not | nodes (e.g. with "systemctl" or "service" commands).|
| configured properly         | Configuration parameters can be verified from the   |
|                             | related .conf files located under '/etc/<component>'|
|                             | directories.                                        |
+-----------------------------+-----------------------------------------------------+
| Some resources required for | The tempest.conf file, automatically generated by   |
| execution test cases are    | Rally in Functest, does not contain all the needed  |
| missing                     | parameters or some parameters are not set properly. |
|                             | The tempest.conf file is located in directory       |
|                             | '/home/opnfv/.rally/tempest/for-deployment-<UUID>'  |
|                             | in the Functest Docker container. Use the "rally    |
|                             | deployment list" command in order to check the UUID |
|                             | the UUID of the current deployment.                 |
+-----------------------------+-----------------------------------------------------+


When some Tempest test case fails, captured traceback and possibly also the
related REST API requests/responses are output to the console. More detailed debug
information can be found from tempest.log file stored into related Rally deployment
folder.


Rally
^^^^^

The same error causes which were mentioned above for Tempest test cases, may also
lead to errors in Rally as well.

It is possible to run only one Rally scenario, instead of the whole suite.
To do that, call the alternative python script as follows::

  python $repos_dir/functest/testcases/OpenStack/rally/run_rally-cert.py -h
  usage: run_rally-cert.py [-h] [-d] [-r] [-s] [-v] [-n] test_name

  positional arguments:
    test_name      Module name to be tested. Possible values are : [
                   authenticate | glance | cinder | heat | keystone | neutron |
                   nova | quotas | requests | vm | all ] The 'all' value
                   performs all possible test scenarios

  optional arguments:
    -h, --help     show this help message and exit
    -d, --debug    Debug mode
    -r, --report   Create json result file
    -s, --smoke    Smoke test mode
    -v, --verbose  Print verbose info about the progress
    -n, --noclean  Don't clean the created resources for this test.

For example, to run the Glance scenario with debug information::

  python $repos_dir/functest/testcases/OpenStack/rally/run_rally-cert.py -d glance

Possible scenarios are:
 * authenticate
 * glance
 * cinder
 * heat
 * keystone
 * neutron
 * nova
 * quotas
 * requests
 * vm

To know more about what those scenarios are doing, they are defined in directory:
*$repos_dir/functest/testcases/OpenStack/rally/scenario*
For more info about Rally scenario definition please refer to the Rally official
documentation. `[3]`_

If the flag *all* is specified, it will run all the scenarios one by one. Please
note that this might take some time (~1,5hr), taking around 1 hour alone to
complete the Nova scenario.

To check any possible problems with Rally, the logs are stored under
*/home/opnfv/functest/results/rally/* in the Functest Docker container.


Controllers
-----------

ODL
^^^
2 versions are supported in Colorado, depending on the scenario:
 * Lithium
 * Berylium

The upstream test suites have not been adapted, so you may get 18 or 15 tests
passed on 18 depending on your configuration. The 3 testcases are partly failed
due to wrong return code.

ONOS
^^^^

Please refer to the ONOS documentation. `ONOSFW User Guide`_ .


Features
--------


Doctor
^^^^^^
Please refer to the Doctor documentation. `Doctor User Guide`_


Promise
^^^^^^^
Please refer to the Promise documentation. `Promise User Guide`_


bgpvpn
^^^^^^
Please refer to the SNVPN documentation. `SDNVPN User Guide`_


NFV
---

vIMS
^^^^
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


.. _`OPNFV Functest Developer Guide`:  http://artifacts.opnfv.org/functest/docs/devguide/#
