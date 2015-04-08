===========================
OPNFV functional test guide
===========================

The goal of this document consists in describing how to run functional tests on OPNFV solution and how to automate these tests.

For release 1, several test cases have been selected:
 * Rally Bench test suite
 * Tempest tes suite
 * OpenDaylight test suite
 * vPing
 * vIMS
  

.. _prereqs:

-------------
Prerequisites
-------------
We assume that an OPNFV solution has been installed (System Under Test). 
For release 1, the tools needed for functional testing are not part of the installer and are not automatically installed.

.. _pharos: https://wiki.opnfv.org/pharos
 
It is recommended to install the tools on the jump host server as defined in the Pharos project.

.. _installation:

------------
Installation
------------

Rally bench test suite
======================

Create or enter a folder where you want to check out the tool repos. Follow `Rally installation procedure`_.

.. _`Rally installation procedure`: https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html


Tempest
=======

It is possible to use Rally to perform Tempest tests. See `tempest installation guide using Rally`_.

.. _`tempest installation guide using Rally`: https://www.mirantis.com/blog/rally-openstack-tempest-testing-made-simpler/ 

OpenDaylight 
============

vPing
=====

vIMS
====


.. _manualtest:

--------------
Manual testing
--------------

Rally
=====
Check your deployment::

    # rally deployment check
    keystone endpoints are valid and following service are available:
    +-------------+-----------+------------+
    | Services  | Type        | Status     |
    +-----------+-------------+------------+
    | cinder    | volume      | Available  |
    | cinderv2  | volumev2    | Available  |
    | glance    | image       | Available  |
    | keystone  | identity    | Available  | 
    | neutron   | network     | Available  |
    | nova      | compute     | Available  |
    | nova_ec2  | compute_ec2 | Available  |
    | novav3    | computev3   | Available  |
    +-----------+-------------+------------+

Create a new opnfv scenario directory and run test suite::

    # cd ~/rally/samples/tasks/scenario/
    # mkdir opnfv 
    # wget http://git.opnfv.org/.. <TODO>
    # rally task start --abort-on-sla-failure ./opnfv.json

Tempest
=======

If we consider running Tempest suite with Rally::

    # rally verify start
    # rally verify list




OpenDaylight 
============

vPing
=====

vIMS
====


.. _automatictest:

------------------
Testing Automation
------------------

Connection of your platform
===========================
If you want to add your platform to the community automation, you need to declare your machine as a Jenkins slave.
 * Send a mail to OPNFV LF Helpdesk (opnfv-helpdesk@rt.linuxfoundation.org)
 * Create a local user jenkins on your machine
 * wget http://mirrors.jenkins-ci.org/war/1.599/jenkins.war
 * Extract contents, find the file named slave.jar and copy it to somewhere which jenkins user created in first step can access.
 * Create a directory /home/jenkins/opnfv_slave_root
 * check the java version (>1.7.0_75)
 * Contact Linux Foundation to manage authentication of your server 
 * A key/token will be produced. Establish connection towards OPNFV Jenkins by using below command: java -jar slave.jar -jnlpUrl https://build.opnfv.org/ci/computer/<slave_name>/slave-agent.jnlp -secret <token>

Continuous integration scripts
==============================

.. _references:

----------
References
----------

OPNFV main site: opnfvmain_.

OPNFV functional test page: opnfvfunctest_.

IRC support chan: #opnfv-testperf

.. _opnfvmain: http://www.opnfv.org
.. _opnfvfunctest: https://wiki.opnfv.org/opnfv_functional_testing
