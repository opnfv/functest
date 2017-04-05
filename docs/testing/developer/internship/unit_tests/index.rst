=======
License
=======

Functest Docs are licensed under a Creative Commons Attribution 4.0
International License.
You should have received a copy of the license along with this.
If not, see <http://creativecommons.org/licenses/by/4.0/>.

===================
Functest Unit tests
===================

Author: Ashish Kumar
Mentors: H.Yao, J.Lausuch, M.Richomme

Abstract
========


Version history
===============

+------------+----------+------------------+------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**            |
|            |          |                  |                        |
+------------+----------+------------------+------------------------+
| 2016-11-14 | 0.0.1    | Morgan Richomme  | Beginning of the       |
|            |          | (Orange)         | Internship             |
+------------+----------+------------------+------------------------+
| 2017-03-31 | 0.0.2    | Ashish Kumar     | During the             |
|            |          | (IIIT Hyderabad) | Internship             |
+------------+----------+------------------+------------------------+


Overview:
=========
Functest project is developping and integrating functional test cases for OPNFV
and it is part of OPNFV since the beginning. Functest develops its own testcase
and framework. This framework includes several utility libraries. Project is
growing rapidly with more features, tests added as per requirement. It becomes
the responsibility of every developer to maintain the integrity of code i.e. new
patch shouldn't break the previous functionality of the project. To automate this
process of software development, we should write unit tests and add it to CI so
that when new patch is ready to merge, we shouldn't allow those which are breaking
previous unit tests or decreasing the coverage.



Problem Statement:
------------------
The goal of the intership consists in creating unit test suites on Functest code
with good code coverage (>80%) and integrate it in continuous integration in order
to consolidate existing code.


Curation Phase
--------------
The curation phase was the first 3 to 4 weeks of the internship. This phase was to get
familiar with the functest code and functionality and explore the solutions for unit
testing in other projects and come up with the strategy for writing unit tests in functest.

In this phase we decided,
- Coverage should be 80%. There are some functions like __init__, getter, setter and other
  private methods for which writing unit test is a tedious job, so we are leaving these methods
  for now.
- Do method wise testing for every module.
- Use mock for external or third party services, system calls and other external library calls
  which could impact the behaviour of system during the run of unit test.
- Add it in jenkins as passing criteria for patches.
- Write tests in modular way so that it can help to serve as a form of documentation.



Schedule:
=========
+--------------------------+------------------------------------------+
| **Date**                 | **Comment**                              |
|                          |                                          |
+--------------------------+------------------------------------------+
| Nov 14th - Nov 28th      | 1. Learn Functest Project Business       |
|                          | 2. Set up the development environment    |
|                          | 3. Run Functest code                     |
+--------------------------+------------------------------------------+
| Nov 28th  -  Dec.9th     | 1. Explore Unit Testing Strategy,        |
|                          | 2. Learn about Mock in python            |
+--------------------------+------------------------------------------+
| Dec 12th - Dec 23rd      | Implement Unit Tests for CLI             |
|                          |                                          |
+--------------------------+------------------------------------------+
| Dec 26th   - Jan 6th     | Implement Unit Tests for Utils           |
|                          |                                          |
+--------------------------+------------------------------------------+
| Jan 9th -  Jan 20th      | Implement Unit Tests for CI              |
|                          |                                          |
+--------------------------+------------------------------------------+
| Jan 23rd - Feb 3rd       | Implement Unit Tests for Core            |
|                          |                                          |
+--------------------------+------------------------------------------+
| Feb 6th  - Feb 17th      | Implement Unit Tests for                 |
|                          | OPNFV_TESTS/Openstack/tempest            |
+--------------------------+------------------------------------------+
| Feb 20th  - Mar 3rd      | Implement Unit Tests for                 |
|                          | OPNFV_TESTS/Openstack/rally              |
+--------------------------+------------------------------------------+
| Mar 6th  - Mar 17th      | Implement Unit Tests for                 |
|                          | OPNFV_TESTS/VNF/IMS                      |
+--------------------------+------------------------------------------+
| Mar 20th  - Mar 31st     | Recheck and Increase Coverage for all    |
|                          | modules > 80%                            |
+--------------------------+------------------------------------------+
| Apr 3rd  -  Apr 14th     | Add CI Gating for unit tests             |
|                          |                                          |
+--------------------------+------------------------------------------+
| Apr 17th  -  Apr 28th    | Use Tox Utility, Documentation           |
|                          |                                          |
+--------------------------+------------------------------------------+
| Apr 28th  -  End         | Bug Fixing                               |
|                          |                                          |
+--------------------------+------------------------------------------+


References:
===========

.. _`[1]` : https://wiki.opnfv.org/display/DEV/Intern+Project%3A+Functest+unit+tests

