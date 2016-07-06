******************************
OPNFV FUNCTEST developer guide
******************************

.. toctree::
   :numbered:
   :maxdepth: 2


============
Introduction
============

This document describes how feature projects aiming to run functional tests can
be integrated into Functest framework.


================================
Functest High level architecture
================================

Functest is project delivering a test container dedicated to OPNFV.
It includes the tools, the scripts and the test scenarios.

Functest can be described as follow::

 +----------------------+
 |                      |
 |   +--------------+   |                  +-------------------+
 |   |              |   |    Public        |                   |
 |   | Tools        |   +------------------+      OPNFV        |
 |   | Scripts      |   |                  | System Under Test |
 |   | Scenarios    |   +------------------+                   |
 |   |              |   |    Management    |                   |
 |   +--------------+   |                  +-------------------+
 |                      |
 |    Functest Docker   |
 |                      |
 +----------------------+

Functest deals with internal and external test cases.
The Internal test cases in Colorado are:

 * vping_ssh
 * vping_userdata
 * odl
 * tempest_smoke_serial
 * rally_sanity
 * tempest_full_parallel
 * rally_full
 * vims

The external tescases are:

 * promise
 * doctor
 * onos
 * bgpvpn
 * security_scan
 * copper
 * moon

Since Colorado, test categories also known as tiers have been created to
group similar tests, provide consistant sub-lists and at the end optimize
test duration for CI.

see `[2]`_ for details.


Functest can also be considered as a framework that may include external OPNFV
projects.
This framework will ease the integration of the feature test suite to the CI.
A feature category has been created to simplify the integration of feature
project test suites into Functest.

====================
Test Dashboard & API
====================

The OPNFV testing group created a test collection database to collect the test
results from CI.
Any test project running on any lab integrated in CI can push the results to
this database.
This database can be used afterwards to see the evolution of the tests and
compare the results versus the installers, the scenario or the labs.

You can find more information about the dashboard from Testing Dashboard wiki
page `[3]`_.

Overall Architecture
====================
The Test result management can be summarized as follows::

  +-------------+    +-------------+    +-------------+
  |             |    |             |    |             |
  |   Test      |    |   Test      |    |   Test      |
  | Project #1  |    | Project #2  |    | Project #N  |
  |             |    |             |    |             |
  +-------------+    +-------------+    +-------------+
           |               |               |
           V               V               V
       +-----------------------------------------+
       |                                         |
       |         Test Rest API front end         |
       |  http://testresults.opnfv.org/test      |
       |                                         |
       +-----------------------------------------+
           A                |
           |                V
           |     +-------------------------+
           |     |                         |
           |     |    Test Results DB      |
           |     |         Mongo DB        |
           |     |                         |
           |     +-------------------------+
           |
           |
     +----------------------+
     |                      |
     |    test Dashboard    |
     |                      |
     +----------------------+

Test API description
====================
The Test API is used to declare pods, projects, test cases and test results. An
additional method dashboard has been added to post-process the raw results in release Brahmaputra.
The data model is very basic, 4 objects are created:

  * Pods
  * Projects
  * Testcases
  * Results

Pods::

  {
    "id": <ID>,
    "details": <URL description of the POD>,
    "creation_date": "YYYY-MM-DD HH:MM:SS",
    "name": <The POD Name>,
    "mode": <metal or virtual>,
    "role": <ci-pod or community-pod or single-node>
  },

Projects::

  {
    "id": <ID>,
    "name": <Name of the Project>,
    "creation_date": "YYYY-MM-DD HH:MM:SS",
    "description": <Short description>
  },

Testcases::

  {
    "id": <ID>,
    "name":<Name of the test case>,
    "project_name":<Name of belonged project>,
    "creation_date": "YYYY-MM-DD HH:MM:SS",
    "description": <short description>,
    "url":<URL for longer description>
  },

Results::

  {
    "_id": <ID>,
    "case_name": <Reference to the test case>,
    "project_name": <Reference to project>,
    "pod_name": <Reference to POD where the test was executed>,
    "installer": <Installer Apex or Compass or Fuel or Joid>,
    "version": <master or Colorado or Brahmaputra>,
    "start_date": "YYYY-MM-DD HH:MM:SS",
    "stop_date": "YYYY-MM-DD HH:MM:SS",
    "build_tag": <such as "jenkins-functest-fuel-baremetal-daily-master-108">,
    "scenario": <Scenario on which the test was executed>,
    "criteria": <PASS or FAILED>,
    "trust_indicator": <0~1>
  }

The API can described as follows. For detailed information, please go to
http://testresults.opnfv.org/test/swagger/spec.html

Authentication: opnfv/api@opnfv

Please notes that POST/DELETE/PUT operations for test or study purpose via
swagger website is not allowed, because it will change the real data in
the database.

Version:

 +--------+--------------------------+-----------------------------------------+
 | Method | Path                     | Description                             |
 +========+==========================+=========================================+
 | GET    | /versions                 | Get all supported API versions         |
 +--------+--------------------------+-----------------------------------------+


Pods:

 +--------+----------------------------+-----------------------------------------+
 | Method | Path                       | Description                             |
 +========+============================+=========================================+
 | GET    | /api/v1/pods               | Get the list of declared Labs (PODs)    |
 +--------+----------------------------+-----------------------------------------+
 | POST   | /api/v1/pods               | Declare a new POD                       |
 |        |                            | Content-Type: application/json          |
 |        |                            | {                                       |
 |        |                            | "name": "pod_foo",                      |
 |        |                            | "mode": "metal",                        |
 |        |                            | "role": "ci-pod",                       |
 |        |                            | "details": "it is a ci pod"             |
 |        |                            | }                                       |
 +--------+----------------------------+-----------------------------------------+
 | GET    | /api/v1/pods/{pod_name}    | Get a declared POD                      |
 +--------+----------------------------+-----------------------------------------+

Projects:

 +--------+----------------------------+-----------------------------------------+
 | Method | Path                       | Description                             |
 +========+============================+=========================================+
 | GET    | /api/v1/projects           | Get the list of declared projects       |
 +--------+----------------------------+-----------------------------------------+
 | POST   | /api/v1/projects           | Declare a new test project              |
 |        |                            | Content-Type: application/json          |
 |        |                            | {                                       |
 |        |                            | "name": "project_foo",                  |
 |        |                            | "description": "whatever you want"      |
 |        |                            | }                                       |
 +--------+----------------------------+-----------------------------------------+
 | DELETE | /api/v1/projects/{project} | Delete a test project                   |
 +--------+----------------------------+-----------------------------------------+
 | GET    | /api/v1/projects/{project} | Get details on a {project}              |
 |        |                            |                                         |
 +--------+----------------------------+-----------------------------------------+
 | PUT    | /api/v1/projects/{project} | Update a test project                   |
 |        |                            |                                         |
 |        |                            | Content-Type: application/json          |
 |        |                            | {                                       |
 |        |                            | <the field(s) you want to modify>       |
 |        |                            | }                                       |
 +--------+----------------------------+-----------------------------------------+


Testcases:

 +--------+----------------------------+-----------------------------------------+
 | Method | Path                       | Description                             |
 +========+============================+=========================================+
 | GET    | /api/v1/projects/{project}/| Get the list of testcases of {project}  |
 |        | cases                      |                                         |
 +--------+----------------------------+-----------------------------------------+
 | POST   | /api/v1/projects/{project}/| Add a new test case to {project}        |
 |        | cases                      | Content-Type: application/json          |
 |        |                            | {                                       |
 |        |                            | "name": "case_foo",                     |
 |        |                            | "description": "whatever you want"      |
 |        |                            | "url": "whatever you want"              |
 |        |                            | }                                       |
 +--------+----------------------------+-----------------------------------------+
 | DELETE | /api/v1/projects/{project}/| Delete a test case                      |
 |        | cases/{case}               |                                         |
 +--------+----------------------------+-----------------------------------------+
 | GET    | /api/v1/projects/{project}/| Get a declared test case                |
 |        | cases/{case}               |                                         |
 +--------+----------------------------+-----------------------------------------+
 | PUT    | /api/v1/projects/{project}?| Modify a test case of {project}         |
 |        | cases/{case}               |                                         |
 |        |                            | Content-Type: application/json          |
 |        |                            | {                                       |
 |        |                            | <the field(s) you want to modify>       |
 |        |                            | }                                       |
 +--------+----------------------------+-----------------------------------------+

Results:

 +--------+----------------------------+------------------------------------------+
 | Method | Path                       | Description                              |
 +========+============================+==========================================+
 | GET    | /api/v1/results             | Get all the test results                |
 +--------+----------------------------+------------------------------------------+
 | POST   | /api/v1/results            | Add a new test results                   |
 |        |                            | Content-Type: application/json           |
 |        |                            | {                                        |
 |        |                            | "project_name": "project_foo",           |
 |        |                            | "scenario": "odl-l2",                    |
 |        |                            | "stop_date": "2016-05-28T14:42:58.384Z", |
 |        |                            | "trust_indicator": 0.5,                  |
 |        |                            | "case_name": "vPing",                    |
 |        |                            | "build_tag": "",                         |
 |        |                            | "version": "Colorado",                   |
 |        |                            | "pod_name": "pod_foo",                   |
 |        |                            | "criteria": "PASS",                      |
 |        |                            | "installer": "fuel",                     |
 |        |                            | "start_date": "2016-05-28T14:41:58.384Z",|
 |        |                            | "details": <your results>                |
 |        |                            | }                                        |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | Get the test results of {case}           |
 |        | case={case}                |                                          |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | Get the test results of build_tag        |
 |        | build_tag={tag}            | {tag}.                                   |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | Get last {N} records of test results     |
 |        | last={N}                   |                                          |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | Get the test results of scenario         |
 |        | scenario={scenario}        | {scenario}.                              |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | Get the test results of trust_indicator  |
 |        | trust_indicator={ind}      | {ind}.                                   |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | Get the test results of last days        |
 |        | period={period}            | {period}.                                |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | Get the test results of {project}        |
 |        | project={project}          |                                          |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | Get the test results of version          |
 |        | version={version}          | {version}.                               |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | Get the test results of criteria         |
 |        | criteria={criteria}        | {criteria}.                              |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | get the results on pod {pod}             |
 |        | pod={pod}                  |                                          |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | Get the test results of installer {inst} |
 |        | installer={inst}           |                                          |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results?           | Get the results according to combined    |
 |        | <query conditions>         | query conditions supported above         |
 +--------+----------------------------+------------------------------------------+
 | GET    | /api/v1/results/{result_id}| Get the test result by result_id         |
 +--------+----------------------------+------------------------------------------+


Dashboard:

 +--------+----------------------------+-----------------------------------------+
 | Method | Path                       | Description                             |
 +========+============================+=========================================+
 | GET    |/dashboard/v1/results?      | Get all the dashboard ready results of  |
 |        |&project={project}          | {case} of the project {project}         |
 |        |&case={case}                |                                         |
 +--------+----------------------------+-----------------------------------------+
 | GET    |/dashboard/v1/results?      | Get all the dashboard ready results of  |
 |        |&project={project}          | {case} of the project {project}         |
 |        |&case={case}                | version {version}                       |
 |        |&version={version}          |                                         |
 +--------+----------------------------+-----------------------------------------+
 | GET    |/dashboard/v1/results?      | Get all the dashboard ready results of  |
 |        |&project={project}          | {case} of the project {project}         |
 |        |&case={case}                | since {days} days                       |
 |        |&period={days}              |                                         |
 +--------+----------------------------+-----------------------------------------+
 | GET    |/dashboard/v1/results?      | Get all the dashboard ready results of  |
 |        |&project={project}          | {case} of the project {project}         |
 |        |&case={case}                | installed by {installer}                |
 |        |&installer={installer}      |                                         |
 +--------+----------------------------+-----------------------------------------+
 | GET    |/dashboard/v1/results?      | Get all the dashboard ready results of  |
 |        |&project={project}          | {case} of the project {project}         |
 |        |&case={case}                | on POD {pod}                            |
 |        |&pod={pod}                  |                                         |
 +--------+----------------------------+-----------------------------------------+
 | GET    |/dashboard/v1/results?      | Get all the dashboard ready results of  |
 |        |&project={project}          | {case} of the project {project}         |
 |        |&case={case}                | and combined by other query conditions  |
 |        |&<query conditions>         | supported above.                        |
 +--------+----------------------------+-----------------------------------------+
 | GET    |/dashboard/v1/projects?     | Get all the dashboard ready projects    |
 +--------+----------------------------+-----------------------------------------+

Dashboard description
=====================

The results with dashboard method are post-processed from raw results.
Please note that dashboard results are not stored. Only raw results are stored.

Release Brahmaputra
-------------------

Dashboard url: http://testresults.opnfv.org/dashboard/

Release Colorado
----------------

Dashboard url: http://testresults.opnfv.org/kibana_dashboards/

Credentials for a guest account: opnfvuser/kibana

==================
How Tos Functest ?
==================


How Functest works?
===================

The installation, the launch of the Functest docker image is described in
`[1]`_.

The procedure to start tests is described  in `[2]`_


How test constraints are defined?
=================================

Test constraints are based on:

 * scenario (DEPLOY_SCENARIO env variable)
 * installer (INSTALLER_TYPE env variable)

A scenario is a formal description of the system under test.
The rules to define a scenario are described in `[4]`_

These 2 constraints are considered to determinate if the test is runnable
or not (no need to run onos suite on odl scenario).

On the test declaration for CI, the test owner shall indicate these 2
constraints. The file testcases.yaml `[5]`_ must be patched in git to
include new test cases.

For each dependency, it is possible to define a regex


 name: promise
 criteria: 'success_rate == 100%'
 description: >-
     Test suite from Promise project.
 dependencies:
     installer: '(fuel)|(joid)'
     scenario: ''

In the example above, it means that promise test will be runnable only
with joid or fuel installers on any scenario.

             
 name: vims
 criteria: 'status == "PASS"'
 description: >-
     This test case deploys an OpenSource vIMS solution from Clearwater
     using the Cloudify orchestrator. It also runs some signaling traffic.
 dependencies:
     installer: ''
     scenario: '(ocl)|(nosdn)|^(os-odl)((?!bgpvpn).)*$'

The vims criteria means any installer and exclude onos and odl with
bgpvpn scenarios

How to know which test I can run?
=================================


How to manually start Functest test?
====================================

How to declare my tests in Functest?
====================================

The files of the Functest repository you must modify to integrate Functest are:

 * functest/docker/Dockerfile: get your code
 * functest/ci/testcases.yaml: reference your tests
 * functest/ci/exec_test.sh: run your test from CI and CLI


Dockerfile
----------

This file lists the repositories to be cloned in the Functest container.
The repositories can be internal or external::

 RUN git clone https://gerrit.opnfv.org/gerrit/<your porject> ${repos_dir}/<your project>

testcases.yaml
--------------

exec_test.sh
------------


How to select my list of tests for CI?
======================================



How to push your results into the Test Database
===============================================

The test database is used to collect test results. By default it is enabled only
in Continuous Integration.
The architecture and associated API is described in `[2]`_.
If you want to push your results from CI, you just have to use the API at the
end of your script.

You can also reuse a python function defined in functest_utils.py::

  def push_results_to_db(db_url, case_name, logger, pod_name,version, payload):
    """
    POST results to the Result target DB
    """
    url = db_url + "/results"
    installer = get_installer_type(logger)
    params = {"project_name": "functest", "case_name": case_name,
              "pod_name": pod_name, "installer": installer,
              "version": version, "details": payload}

    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(url, data=json.dumps(params), headers=headers)
        if logger:
            logger.debug(r)
        return True
    except Exception, e:
        print "Error [push_results_to_db('%s', '%s', '%s', '%s', '%s')]:" \
            % (db_url, case_name, pod_name, version, payload), e
        return False


==========
References
==========

.. _`[1]`: http://artifacts.opnfv.org/functest/docs/configguide/index.html Functest configuration guide URL
.. _`[2]`: http://artifacts.opnfv.org/functest/docs/userguide/index.html functest user guide URL
.. _`[3]`: https://wiki.opnfv.org/opnfv_test_dashboard
.. _`[4]`: https://wiki.opnfv.org/display/INF/CI+Scenario+Naming
.. _`[5]`: https://git.opnfv.org/cgit/functest/tree/ci/testcases.yaml



OPNFV main site: opnfvmain_.

OPNFV functional test page: opnfvfunctest_.

IRC support chan: #opnfv-testperf

.. _opnfvmain: http://www.opnfv.org
.. _opnfvfunctest: https://wiki.opnfv.org/opnfv_functional_testing
.. _`OpenRC`: http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html
.. _`Rally installation procedure`: https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html
.. _`config_test.py` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.py
.. _`config_functest.yaml` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.yaml

