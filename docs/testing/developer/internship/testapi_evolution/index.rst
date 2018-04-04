.. SPDX-License-Identifier: CC-BY-4.0

=================
TestAPI evolution
=================

Author: Sakala Venkata Krishna Rohit
Mentors: S. Feng, J.Lausuch, M.Richomme

Abstract
========

The TestAPI is used by all the test opnfv projects to report results.
It is also used to declare projects, test cases and labs. A major refactoring
has been done in Colorado with the introduction of swagger. The TestAPI is defined in Functest
developer guide. The purpose of this project is to add more features to the TestAPI that automate
the tasks that are done manually now, though there are tasks other than automation.

Version history
===============

+------------+----------+------------------+------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**            |
|            |          |                  |                        |
+------------+----------+------------------+------------------------+
| 2016-11-14 | 0.0.1    | Morgan Richomme  | Beginning of the       |
|            |          | (Orange)         | Internship             |
+------------+----------+------------------+------------------------+
| 2017-02-17 | 0.0.2    | S.V.K Rohit      | End of the Internship  |
|            |          | (IIIT Hyderabad) |                        |
+------------+----------+------------------+------------------------+

Overview:
=========

The internhip time period was from Nov 14th to Feb 17th. The project prosposal page is here `[1]`_.
The intern project was assigned to Svk Rohit and was mentored by S. Feng, J.Lausuch, M.Richomme.
The link to the patches submitted is `[2]`_. The internship was successfully completed and the
documentation is as follows.

Problem Statement:
------------------

The problem statement could be divided into pending features that needed to be added into TestAPI
repo. The following were to be accomplished within the internship time frame.

* **Add verification jenkins job for the TestAPI code**
    The purpose of this job is to verify whehter the unit tests are successful or not with the
    inclusion of the patchset submitted.

* **Automatic update of opnfv/testapi docker image**
    The docker image of TestAPI is hosted in the opnfv docker hub. To ensure that the TestAPI image
    is always updated with the repository, automatic updation of the image is necessary and a job
    is triggered whenever a new patch gets merged.

* **Automation deployment of testresults.opnfv.org/test/ website**
    In the same manner as the docker image of TestAPI is updated, the TestAPI website needs to be
    in sync with the repository code. So, a job has been added to the opnfv jenkins ci for the
    updation of the testresults website.

* **Generate static documentation of TestAPI calls**
    The purpose of this is to give an static/offline view of TestAPI. If someone wants to have a
    look at the Restful APIs of TestAPI, he/she does't need to go to the website, he can download
    a html page and view it anytime.

* **Backup MongoDB of TestAPI**
    The mongoDB needs to be backed up every week. Till now it was done manually, but due to this
    internship, it is now automated using a jenkins job.

* **Add token based authorization to the TestAPI calls**
    The token based authorization was implemented to ensure that only ci_pods could access the
    database. Authentication has been added to only delete/put/post requests.

Curation Phase:
---------------

The curation phase was the first 3 to 4 weeks of the internship. This phase was to get familiar
with the TestAPI code and functionality and propose the solutions/tools for the tasks mentioned
above. Swagger codegen was choosen out of the four tools proposed `[3]`_ for generating static
documentaion.

Also, specific amount of time was spent on the script flow of the jenkins jobs. The automatic
deployment task involves accessing a remote server from inside the jenkins build. The deployment
had to be done only after the docker image update is done. For these constraints to satisfy, a
multijob jenkins job was choosen instead of a freestyle job.

Important Links:
----------------

* MongoDB Backup Link                 - `[4]`_
* Static Documentation                - `[5]`_
* TestAPI Token addition to ci_pods   - `[6]`_

Schedule:
=========

The progress and completion of the tasks is described in the below table.

+--------------------------+------------------------------------------+
| **Date**                 | **Comment**                              |
|                          |                                          |
+--------------------------+------------------------------------------+
| Nov 14th - Dec 31st      | Understand TestAPI code and the          |
|                          | requirements.                            |
+--------------------------+------------------------------------------+
| Jan 1st  - Jan 7th       | Add jenkins job to create static         |
|                          | documentation and write build scripts.   |
+--------------------------+------------------------------------------+
| Jan 8th  - Jan 21st      | Add verification jenkins job for unit    |
|                          | tests.                                   |
+--------------------------+------------------------------------------+
| Jan 22nd - Jan 28th      | Add jenkins job for mongodb backup       |
|                          |                                          |
+--------------------------+------------------------------------------+
| Jan 29th - Feb 11th      | Enable automatic deployment of           |
|                          | testresults.opnfv.org/test/              |
+--------------------------+------------------------------------------+
| Feb 12th - Feb 17th      | Add token based authentication           |
|                          |                                          |
+--------------------------+------------------------------------------+

FAQ's
=====

This section lists the problems that I have faced and the understanding that I have acquired during
the internship. This section may help other developers in solving any errors casused because of the
code written as a part of this internship.


TestAPI
-------

What is the difference between defining data_file as "/etc/.." and "etc/.." in setup.cfg ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If in the setup.cfg, it is defined as

[files]
data_files =
etc/a.conf = etc/a.conf.sample

then it ends up installed in the /usr/etc/. With this configuration, it would be installed
correctly within a venv. but when it is defined as

[files]
data_files =
/etc/a.conf = etc/a.conf.sample

then it ends up installed on the root of the filesystem instead of properly be installed within the
venv.

Which attribute does swagger-codegen uses as the title in the generation of document generation ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It uses the nickname of the api call in swagger as the title in the generation of the document
generation.

Does swagger-codegen take more than one yaml file as input ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No, swagger-codegen only takes one yaml file as input to its jar file. If there more than one yaml
file, one needs to merge them and give it as an input keeping mind the swagger specs.


Jenkins & JJB
-------------

Which scm macro is used for verification jenkins jobs ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two macros for scm one is git-scm and other git-scm-gerrit. git-scm-gerrit is used for
verification jenkins job.

Does the virtualenv created in one build script exists in other build scripts too ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No, the virtualenv created in one build script only exists in that build script/shell.

What parameters are needed for the scm macros ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Project and Branch are the two parameters needed for scm macros.

What is the directory inside the jenkins build ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The directory of the jenkins build is the directory of the repo. `ls $WORKSPACE` command will give
you all the contents of the directory.

How to include a bash script in jenkins job yaml file ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An example might be apt here as an answer.

builders:
    - shell:
        !include-raw: include-raw001-hello-world.sh


How do you make a build server run on a specific machine ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It can be done by defining a label parameter 'SLAVE_LABEL' or in OPNFV , there are macros for each
server, one can use those parameter macros.
Ex: opnfv-build-defaults. Note, if we use macro, then no need to define GIT_BASE, but if one uses
SLAVE_LABEL, one needs to define a parameter GIT_BASE. This is because macro already has GIT_BASE
defined.

What job style should be used when there is a situation like one build should trigger other builds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
or when different build scripts need to be run on different machines ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MultiJob style should be used as it has phases where each phase can be taken as a build scipt and
can have its own parameters by which one can define the SLAVE_LABEL parameter.

References:
===========

_`[1]` : https://wiki.opnfv.org/display/DEV/Intern+Project%3A+testapi+evolution

_`[2]` : https://gerrit.opnfv.org/gerrit/#/q/status:merged+owner:%22Rohit+Sakala+%253Crohitsakala%2540gmail.com%253E%22

_`[3]` : https://docs.google.com/document/d/1jWwVZ1ZpKgKcOS_zSz2KzX1nwg4BXxzBxcwkesl7krw/edit?usp=sharing

_`[4]` : http://artifacts.opnfv.org/testapibackup.html

_`[5]` : http://artifacts.opnfv.org/releng/docs/testapi.html

_`[6]` : http://artifacts.opnfv.org/functest/docs/devguide/index.html#test-api-authorization
