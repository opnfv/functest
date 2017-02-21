******************************
OPNFV FUNCTEST developer guide
******************************

.. toctree::
   :numbered:
   :maxdepth: 2


============
Introduction
============

Functest is a project dealing with functional testing.
Functest produces its own internal test cases but can also be considered
as a framework to support feature and VNF onboarding project testing.
Functest developed a test API and defined a test collection framework
that can be used by any OPNFV project.

Therefore there are many ways to contribute to Functest. You can:

 * Develop new internal test cases
 * Integrate the tests from your feature project
 * Develop the framework to ease the integration of external test cases
 * Develop the API / Test collection framework
 * Develop dashboards or automatic reporting portals

This document describes how, as a developer, you may interact with the
Functest project. The first section details the main working areas of
the project. The Second part is a list of "How to" to help you to join
the Functest family whatever your field of interest is.


========================
Functest developer areas
========================


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

Functest internal test cases
============================
The internal test cases in Danube are:

 * healthcheck
 * connection_check
 * api_check
 * vping_ssh
 * vping_userdata
 * odl
 * snaps_smoke
 * tempest_smoke_serial
 * rally_sanity
 * tempest_full_parallel
 * rally_full
 * cloudify_ims

By internal, we mean that this particular test cases have been
developped and/or integrated by functest contributors and the associated
code is hosted in the Functest repository.
An internal case can be fully developped or a simple integration of
upstream suites (e.g. Tempest/Rally developped in OpenStack are just
integrated in Functest).
The structure of this repository is detailed in `[1]`_.
The main internal test cases are in the opnfv_tests subfolder of the
repository, the internal test cases are:

 * sdn: odl, onos
 * openstack: healthcheck, vping_ssh, vping_userdata, tempest_*, rally_*, connection_check, api_check, snaps_smoke
 * vnf: cloudify_ims

If you want to create a new test case you will have to create a new
folder under the testcases directory.

Functest external test cases
============================
The external test cases are inherited from other OPNFV projects,
especially the feature projects.

The external test cases are:

 * promise
 * doctor
 * onos
 * bgpvpn
 * copper
 * security_scan
 * sfc-odl
 * sfc-onos
 * parser
 * domino
 * multisite
 * opera_ims
 * orchestra_ims


The code to run these test cases may be directly in the repository of
the project. We have also a **features** sub directory under opnfv_tests
directory that may be used (it can be usefull if you want to reuse
Functest library).

Functest framework
==================

Functest can be considered as a framework.
Functest is release as a docker file, including tools, scripts and a CLI
to prepare the environement and run tests.
It simplifies the integration of external test suites in CI pipeline
and provide commodity tools to collect and display results.

Since Colorado, test categories also known as tiers have been created to
group similar tests, provide consistant sub-lists and at the end optimize
test duration for CI (see How To section).

The definition of the tiers has been agreed by the testing working group.

The tiers are:
  * healthcheck
  * smoke
  * features
  * components
  * performance
  * vnf
  * stress

Functest abstraction classes
============================

In order to harmonize test integration, 3 abstraction classes have been
introduced in Danube:

 * testcase_base: base for any test case
 * feature_base: abstraction for feature project
 * vnf_base: abstraction for vnf onboarding

The goal is to unify the way to run test from Functest.

feature_base and vnf_base inherit from testcase_base.

              +-----------------------------------------+
              |                                         |
              |         Testcase_base                   |
              |                                         |
              |         - init()                        |
              |         - run()                         |
              |         - publish_report()              |
              |         - check_criteria()              |
              |                                         |
              +-----------------------------------------+
                     |                       |
                     V                       V
         +--------------------+   +--------------------------+
         |                    |   |                          |
         |    feature_base    |   |      vnf_base            |
         |                    |   |                          |
         |  - prepare()       |   |  - prepare()             |
         |  - post()          |   |  - deploy_orchestrator() |
         |  - parse_results() |   |  - deploy_vnf()          |
         |                    |   |  - test_vnf()            |
         |                    |   |  - clean()               |
         |                    |   |  - execute()             |
         |                    |   |                          |
         +--------------------+   +--------------------------+


Functest util classes
=====================

In order to simplify the creation of test cases, Functest develops some
functions that can be used by any feature or internal test cases.
Several features are supported such as logger, configuration management and
Openstack capabilities (snapshot, clean, tacker,..).
These functions can be found under <repo>/functest/utils and can be described as
follows:

functest/utils/
|-- config.py
|-- constants.py
|-- env.py
|-- functest_constants.py
|-- functest_logger.py
|-- functest_utils.py
|-- openstack_clean.py
|-- openstack_snapshot.py
|-- openstack_tacker.py
`-- openstack_utils.py

Note that for Openstack, keystone v3 is now deployed by default by compass,
fuel and joid in Danube. All installers still support keysone v2 (deprecated in
next version).

Test collection framework
=========================

The OPNFV testing group created a test collection database to collect
the test results from CI:


 http://testresults.opnfv.org/test/swagger/spec.html

 Authentication: opnfv/api@opnfv

Any test project running on any lab integrated in CI can push the
results to this database.
This database can be used to see the evolution of the tests and compare
the results versus the installers, the scenarios or the labs.


Overall Architecture
--------------------
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
--------------------
The Test API is used to declare pods, projects, test cases and test
results. Pods are the pods used to run the tests.
The results pushed in the database are related to pods, projects and
cases. If you try to push results of test done on non referenced pod,
the API will return an error message.

An additional method dashboard has been added to post-process
the raw results in release Brahmaputra (deprecated in Colorado).

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
    "trust_indicator": {
                        "current": 0,
                        "histories": []
                       }
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
 | GET    | /versions                | Get all supported API versions          |
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
 | GET    | /api/v1/results            | Get all the test results                 |
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

Scenarios:

  +--------+----------------------------+-----------------------------------------+
  | Method | Path                       | Description                             |
  +========+============================+=========================================+
  | GET    | /api/v1/scenarios          | Get the list of declared scenarios      |
  +--------+----------------------------+-----------------------------------------+
  | POST   | /api/v1/scenario           | Declare a new scenario                  |
  +--------+----------------------------+-----------------------------------------+
  | GET    | /api/v1/scenario?          | Get a declared scenario                 |
  |        | <query conditions>         |                                         |
  +--------+----------------------------+-----------------------------------------+


The code of the API is hosted in the releng repository `[6]`_.
The test API has been dockerized and may be installed locally in your
lab. See `[15]`_ for details.

The deployment of the test API has been automated.
A jenkins job manages:
  * the unit tests of the test api
  * the cration of a new docker file
  * the deployment of the new test api
  * the archive of the old test api
  * the backup of the Mongo DB

  Automatic reporting
  ===================

  An automatic reporting page has been created in order to provide a
  consistant view of the scenarios.
  In this page, each scenario is evaluated according to test criteria.
  The code for the automatic reporting is available at `[8]`_.

  The results are collected from the centralized database every day and,
  per scenario. A score is calculated based on the results from the last
  10 days. This score is the addition of single test scores. Each test
  case has a success criteria reflected in the criteria field from the
  results.

  Considering an instance of a scenario os-odl_l2-nofeature-ha, the
  scoring is the addition of the scores of all the runnable tests from the
  categories (tiers healthcheck, smoke and features)
  corresponding to this scenario.


   +---------------------+---------+---------+---------+---------+
   | Test                | Apex    | Compass | Fuel    |  Joid   |
   +=====================+=========+=========+=========+=========+
   | vPing_ssh           |    X    |    X    |    X    |    X    |
   +---------------------+---------+---------+---------+---------+
   | vPing_userdata      |    X    |    X    |    X    |    X    |
   +---------------------+---------+---------+---------+---------+
   | tempest_smoke_serial|    X    |    X    |    X    |    X    |
   +---------------------+---------+---------+---------+---------+
   | rally_sanity        |    X    |    X    |    X    |    X    |
   +---------------------+---------+---------+---------+---------+
   | odl                 |    X    |    X    |    X    |    X    |
   +---------------------+---------+---------+---------+---------+
   | promise             |         |         |    X    |    X    |
   +---------------------+---------+---------+---------+---------+
   | doctor              |    X    |         |    X    |         |
   +---------------------+---------+---------+---------+---------+
   | security_scan       |    X    |         |         |         |
   +---------------------+---------+---------+---------+---------+
   | parser              |         |         |    X    |         |
   +---------------------+---------+---------+---------+---------+
   | copper              |    X    |         |         |    X    |
   +---------------------+---------+---------+---------+---------+

  All the testcases listed in the table are runnable on
  os-odl_l2-nofeature scenarios.
  If no result is available or if all the results are failed, the test
  case get 0 point.
  If it was succesfull at least once but not anymore during the 4 runs,
  the case get 1 point (it worked once).
  If at least 3 of the last 4 runs were successful, the case get 2 points.
  If the last 4 runs of the test are successful, the test get 3 points.

  In the example above, the target score for fuel/os-odl_l2-nofeature-ha
  is 3x6 = 18 points.

  The scenario is validated per installer when we got 3 points for all
  individual test cases (e.g 18/18).
  Please note that complex or long duration tests are not considered for
  the scoring. The success criteria are not always easy to define and may
  require specific hardware configuration. These results however provide
  a good level of trust on the scenario.

  A web page is automatically generated every day to display the status.
  This page can be found at `[9]`_. For the status, click on Status menu,
  you may also get feedback for vims and tempest_smoke_serial test cases.

  Any validated scenario is stored in a local file on the web server. In
  fact as we are using a sliding windows to get results, it may happen
  that a successful scenarios is no more run (because considered as
  stable) and then the number of iterations (4 needed) would not be
  sufficient to get the green status.

  Please note that other test cases (e.g. sfc_odl, bgpvpn) need also
  ODL configuration addons and as a consequence specific scenario.
  There are not considered as runnable on the generic odl_l2 scenario.

Dashboard
=========

Dashboard is used to provide a consistant view of the results collected
in CI.
The results showed on the dashboard are post processed from the Database,
which only contains raw results.

In Brahmaputra, we created a basic dashboard.
Since Colorado, it was decided to adopt ELK framework. Mongo DB results
are extracted to feed Elasticsearch database (`[7]`_).

A script was developed to build elasticsearch data set. This
script can be found in `[16]`_.

For next versions, it was decided to integrated bitergia dashboard.
Bitergia already provides a dashboard for code and infrastructure.
A new Test tab will be added. The dataset will be built by consuming
the test API.


=======
How TOs
=======

How Functest works?
===================

The installation and configuration of the Functest docker image is
described in `[1]`_.

The procedure to start tests is described  in `[2]`_


How can I contribute to Functest?
=================================

If you are already a contributor of any OPNFV project, you can
contribute to functest. If you are totally new to OPNFV, you must first
create your Linux Foundation account, then contact us in order to
declare you in the repository database.

We distinguish 2 levels of contributors:

 * the standard contributor can push patch and vote +1/0/-1 on any Functest patch
 * The commitor can vote -2/-1/0/+1/+2 and merge

Functest commitors are promoted by the Functest contributors.


Where can I find some help to start?
====================================

This guide is made for you. You can also have a look at the project wiki
page `[10]`_.
There are references on documentation, video tutorials, tips...

You can also directly contact us by mail with [Functest] prefix in the
title at opnfv-tech-discuss@lists.opnfv.org or on the IRC chan
#opnfv-functest.


What kind of testing do you do in Functest?
===========================================

Functest is focusing on Functional testing. The results must be PASS or
FAIL. We do not deal with performance and/or qualification tests.
We consider OPNFV as a black box and execute our tests from the jumphost
according to Pharos reference technical architecture.

Upstream test suites are integrated (Rally/Tempest/ODL/ONOS,...).
If needed Functest may bootstrap temporarily testing activities if they
are identified but not covered yet by an existing testing project (e.g
security_scan before the creation of the security repository)


How test constraints are defined?
=================================

Test constraints are defined according to 2 paramaters:

 * The scenario (DEPLOY_SCENARIO env variable)
 * The installer (INSTALLER_TYPE env variable)

A scenario is a formal description of the system under test.
The rules to define a scenario are described in `[4]`_

These 2 constraints are considered to determinate if the test is runnable
or not (e.g. no need to run onos suite on odl scenario).

In the test declaration for CI, the test owner shall indicate these 2
constraints. The file testcases.yaml `[5]`_ must be patched in git to
include new test cases. A more elaborated system based on template is
planned for next releases

For each dependency, it is possible to define a regex::

    name: promise
    criteria: 'success_rate == 100%'
    description: >-
        Test suite from Promise project.
    dependencies:
        installer: '(fuel)|(joid)'
        scenario: ''

In the example above, it means that promise test will be runnable only
with joid or fuel installers on any scenario.

The vims criteria means any installer and exclude onos and odl with
bgpvpn scenarios::

    name: vims
    criteria: 'status == "PASS"'
    description: >-
        This test case deploys an OpenSource vIMS solution from Clearwater
        using the Cloudify orchestrator. It also runs some signaling traffic.
    dependencies:
        installer: ''
        scenario: '(ocl)|(nosdn)|^(os-odl)((?!bgpvpn).)*$'


How to write and check constaint regex?
=======================================

Regex are standard regex. You can have a look at  `[11]`_

You can also easily test your regex via an online regex checker such as `[12]`_.
Put your scenario in the TEST STRING window (e.g. os-odl_l3-ovs-ha), put
your regex in the REGULAR EXPRESSION window, then you can test your rule
.


How to know which test I can run?
=================================

You can use the API `[13]`_. The static declaration is in git `[5]`_

If you are in a Functest docker container (assuming that the
environement has been prepared): just use the CLI.

You can get the list per Test cases or by Tier::

    # functest testcase list
    healthcheck
    vping_ssh
    vping_userdata
    tempest_smoke_serial
    rally_sanity
    odl
    doctor
    security_scan
    tempest_full_parallel
    rally_full
    vims
    # functest tier list
    - 0. healthcheck:
    ['healthcheck']
    - 1. smoke:
    ['vping_ssh', 'vping_userdata', 'tempest_smoke_serial', 'rally_sanity']
    - 2. sdn_suites:
    ['odl']
    - 3. features:
    ['doctor', 'security_scan']
    - 4. openstack:
    ['tempest_full_parallel', 'rally_full']
    - 5. vnf:
    ['vims']


How to manually start Functest tests?
=====================================

Assuming that you are connected on the jumphost and that the system is
"Pharos compliant", i.e the technical architecture is compatible with
the one defined in the Pharos project::

    # docker pull opnfv/functest:latest
    # envs="-e INSTALLER_TYPE=fuel -e INSTALLER_IP=10.20.0.2 -e DEPLOY_SCENARIO=os-odl_l2-nofeature-ha -e CI_DEBUG=true"
    # sudo docker run --privileged=true -id ${envs} opnfv/functest:latest /bin/bash


Then you must connect to the docker container and source the
credentials::

    # docker ps (copy the id)
    # docker exec -ti <container_id> bash
    # source $creds


You must first check if the environment is ready::

    # functest env status
    Functest environment ready to run tests.


If not ready, prepare the env by launching::

    # functest env prepare
    Functest environment ready to run tests.

Once the Functest env is ready, you can use the CLI to start tests.

You can run test cases per test case or per tier:
 # functest testcase run <case name> or # functest tier run  <tier name>


e.g::

    # functest testcase run tempest_smoke_serial
    # functest tier run features


If you want to run all the tests you can type::

    # functest testcase run all


If you want to run all the tiers (same at the end that running all the
test cases) you can type::

    # functest tier run all


How to declare my tests in Functest?
====================================

If you want to add new internal test cases, you can submit patch under
the testcases directory of Functest repository.

For feature test integration, the code can be kept into your own
repository. The Functest files to be modified are:

 * functest/docker/Dockerfile: get your code in Functest container
 * functest/ci/testcases.yaml: reference your test and its associated constraints


Dockerfile
----------

This file lists the repositories (internal or external) to be cloned in
the Functest container. You can also add external packages::

 RUN git clone https://gerrit.opnfv.org/gerrit/<your project> ${REPOS_DIR}/<your project>

testcases.yaml
--------------

All the test cases that must be run from CI / CLI must be declared in
ci/testcases.yaml.

This file is used to get the constraints related to the test::

    name: <my_super_test_case>
    criteria: <not used yet in Colorado, could be > 'PASS', 'rate > 90%'
    description: >-
        <the description of your super test suite>
    dependencies:
        installer: regex related to installer e.g. 'fuel', '(apex)||(joid)'
        scenario: regex related to the scenario e.g. 'ovs*no-ha'


You must declare your test case in one of the category (tier).

If you are integrating test suites from a feature project, the default
category is **features**.


How to select my list of tests for CI?
======================================

Functest can be run automatically from CI, a jenkins job is usually
called after an OPNFV fresh installation.
By default we try to run all the possible tests (see `[14]` called from
Functest jenkins job)::

    cmd="python ${FUNCTEST_REPO_DIR}/ci/run_tests.py -t all ${flags}"


Each case can be configured as daily and/or weekly task.
Weekly tasks are used for long duration or experimental tests.
Daily tasks correspond to the minimum set of test suites to validate a scenario.

When executing run_tests.py, a check based on the jenkins build tag will
be considered to detect whether it is a daily and/or a weekly test.

in your CI you can customize the list of test you want to run by case or
by tier, just change the line::

    cmd="python ${FUNCTEST_REPO_DIR}/ci/run_tests.py -t <whatever you want> ${flags}"

e.g.::

    cmd="python ${FUNCTEST_REPO_DIR}/ci/run_tests.py -t healthcheck,smoke ${flags}"

This command will run all the test cases of the first 2 tiers, i.e.
healthcheck, connection_check, api_check, vping_ssh, vping_userdata,
snaps_somke, tempest_smoke_serial and rally_sanity.


How to push your results into the Test Database
===============================================

The test database is used to collect test results. By default it is
enabled only for CI tests from Production CI pods.

The architecture and associated API is described in previous chapter.
If you want to push your results from CI, you just have to call the API
at the end of your script.

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

_`[1]`: http://artifacts.opnfv.org/functest/docs/configguide/index.html Functest configuration guide

_`[2]`: http://artifacts.opnfv.org/functest/docs/userguide/index.html functest user guide

_`[3]`: https://wiki.opnfv.org/opnfv_test_dashboard Brahmaputra dashboard

_`[4]`: https://wiki.opnfv.org/display/INF/CI+Scenario+Naming

_`[5]`: https://git.opnfv.org/cgit/functest/tree/ci/testcases.yaml

_`[6]`: https://git.opnfv.org/cgit/releng/tree/utils/test/result_collection_api

_`[7]`: https://git.opnfv.org/cgit/releng/tree/utils/test/scripts

_`[8]`: https://git.opnfv.org/cgit/releng/tree/utils/test/reporting/functest

_`[9]`: http://testresults.opnfv.org/reporting/

_`[10]`: https://wiki.opnfv.org/opnfv_functional_testing

_`[11]`: https://docs.python.org/2/howto/regex.html

_`[12]`: https://regex101.com/

_`[13]`: http://testresults.opnfv.org/test/api/v1/projects/functest/cases

_`[14]`: https://git.opnfv.org/cgit/releng/tree/jjb/functest/functest-daily.sh

_`[15]`: https://git.opnfv.org/cgit/releng/tree/utils/test/result_collection_api/README.rst

_`[16]`: https://git.opnfv.org/cgit/releng/tree/utils/test/scripts/mongo_to_elasticsearch.py

OPNFV main site: http://www.opnfv.org

OPNFV functional test page: https://wiki.opnfv.org/opnfv_functional_testing

IRC support chan: #opnfv-functest

_`OpenRC`: http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html

_`Rally installation procedure`: https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html

_`config_functest.yaml` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.yaml
