.. SPDX-License-Identifier: CC-BY-4.0

=======================
Open Source VNF Catalog
=======================

Author: Kumar Rishabh
Mentors: B.Souville, M.Richomme, J.Lausuch

Abstract
========



Version hissory
===============

+------------+----------+------------------+------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**            |
|            |          |                  |                        |
+------------+----------+------------------+------------------------+
| 2016-12-12 | 0.0.1    | Morgan Richomme  | Beginning of the       |
|            |          | (Orange)         | Internship             |
+------------+----------+------------------+------------------------+


Overview:
=========


This project aims to create an Open Source catalog for reference and
classification of Virtual Network Functions (VNFs)s available on
Internet. The classification method proposed will be in sync with the
requirements of Telcos active in NFV landscape. The project aims to have
running web platform similar to [1] by the mid of internship (2nd week
of March). By the penultimate month of internship I aim to have fully
functional implementation of an Open Source VNF in functest.


Problem Statement:
------------------

OPNFV aims to be the reference platform for development,
standardization and integration of Open Source NFV components across
various Open Source Platforms. It mainly deals with the infrastructure
through the Network Function Virtualization Infrastructure (NFVI) and
Virtual Infrastructure manager (VIM). The MANO (Management and
orchestration) stacks have been introduced recently. VNFs are not
directly in OPNFV scope, however VNFs are needed to test and qualify the
infrastructure. In this regard having a common curated Open Source
Reference VNF catalog would be of immense importance to community.

Since major focus of OPNFV is Telcos, a curated platform targeted from
industry point of view would be very useful. We plan to divide the
entire project into three major phases(with some iterative improvements
and overlaps)


Curation Phase
--------------
This phase pertains to studying various Open Source VNFs available and
classification of them based on certain parameters. The parameters that
I currently have in mind are:

 * Developer Metrics: These pertain to repo characteristics of VNF under
   study
 * Usage Statistics - Activity, Number of Commits, stars
 * Maturity Statistics - For instance if an NFV community decides code
   coverage is important for them, it shows the NFV community is serious
   about taking the project forward
 * Technical Tagging: These are the tags that pertain to technical
   characteristics of a VNF
 * Broad Use Cases - Whether the VNF fits strictly in IaaS, PaaS or
   SaaS layer or is an hybrid of two/all.
 * Generic Use Cases - This in my opinion is the broadest
   classification category. For instance a VNF could be built with a
   broad idea of powering IOT devices at home or from usage perspective
   of Telco Operators (vFW, vEPC, vIMS, vCDN, vAAA, vCPE,...).`[2]`_
 * Fields of Application
 * Library Status - Whether APIs are standardized, support RESTful
   services.
 * Dependency Forwarding Graph - This is pretty complex tagging
   mechanism. It essentially tries to establish a graph relationship
   between the VNFs (elementary VNFs are used in Service Function
   Chaining chains such as Firewall, DPI, content enrichment,..). In my
   opinion this is useful immensely. This will allow users to go to
   platform and ask a question like - “I have this X tech stack to
   support, Y and Z are my use cases, which NFVs should I use to support
   this.
 * Visitor Score - Based on `[1]`_ I plan to evolve a visitor score for
   the platform. This will allow users to score an NFV on certain
   parameters, may be post comments.

**I plan to use the above three scores and evolve cumulative score which
will be displayed next to each of the NFV on the platform.**

 * Platform building phase - This will involve erecting a Web Platform
   which will be similar to this  `[1]`_. I am decently familiar with
   Django and hence I will write the platform in Django. There are two
   action plans that I have in mind right now. Either I can start writing
   the platform simultaneously which will help keep track of my progress
   or I can write the platform after 1.5 - 2 months into the internship.
   Either way I aim to have the Web Platform ready by March 12.
 * Functest VNF implementation phase - This is the last phase that will
   involve writing a fully functional implementation of an Open Source VNF
   into Functest. I will undertake this after I am 3 months into the
   internship. I have a decent familiarity with python and hence I think
   it shouldn’t be too difficult. I need to decide how complex the VNFI
   should undertake this exercise for (e.g. AAA such as free radius sounds
   relatively easy, vCDN is much more challenging).
   This will be decided in consent with my mentors.

Schedule:
=========
I plan to take this project in 6 months time frame as I want to use it
as a chance to read more about NFVs in particular and SDN in general


+--------------------------+------------------------------------------+
| **Date**                 | **Comment**                              |
|                          |                                          |
+--------------------------+------------------------------------------+
| December 12 - January 12 | Study the above mentioned metrics        |
|                          | Decide which of them are important for   |
|                          | community (and which are not).           |
+--------------------------+------------------------------------------+
| January 12 - January 27  | Make a database for the above studied    |
|                          | metrics and evolve it further based on   |
|                          | Mentors’ input. + associated API         |
+--------------------------+------------------------------------------+
| January 27 - February 5  | Compile the data collected above and make|
|                          | it public. Although I can keep everything|
|                          | public from the beginning too. My        |
|                          | rationale of not making the entire data  |
|                          | public in initial stage as the errors    |
|                          | caused by me could be misleading for     |
|                          | developers.                              |
+--------------------------+------------------------------------------+
| February 5 - March 5     | Erect the Web Platform and release it    |
|                          | for restricted group for alpha testing.  |
+--------------------------+------------------------------------------+
| March 5 - March 12       | Make it public. Release it to public for |
|                          | beta testing. Fix Bugs.                  |
+--------------------------+------------------------------------------+
| March 12 - April 12      | Start working on implementation of an    |
|                          | Open Source VNF in Functest.             |
+--------------------------+------------------------------------------+
| April 12 - May 12        | I will decided what to do here based on  |
|                          | discussion with mentors.                 |
+--------------------------+------------------------------------------+


References:
===========

.. _`[1]` : Openhub: https://www.openhub.net/explore/projects

.. _`[2]` : ETSI NFV White Paper: https://portal.etsi.org/Portals/0/TBpages/NFV/Docs/NFV_White_Paper3.pdf

.. _`[3]` : https://wiki.opnfv.org/display/DEV/Intern+Project%3A+Open+Source+VNF+catalog
