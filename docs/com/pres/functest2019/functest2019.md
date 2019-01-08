# Functest 2019

[Cédric Ollivier](mailto:cedric.ollivier@orange.com)

2019/01/19



## Gates


### Today's Verify -1

- one error is detected by yamllint, pep8, pylint, ansible-lint, bashate or
  doc8
- one unit test fails (py27 and py35)
- specific modules are not rated 10/10 by pylint
- our Framework is not fully covered
- unix permissions are wrong
- one doc cannot be generated without warning

Please see [tox.ini](https://git.opnfv.org/functest/tree/tox.ini) for details


### Great! But

- the current gate checks all coding rules, our Framework and all interfaces
to third-parties but **not our testcases**
- it doesn't break **the circular dependencies** between Installers and
Functest (Installers ask for a trustable healthcheck but we need results of
"Installer runs" as prerequisites)

Our testcases have still **to be verified by hand** what differs from
OpenStack Workflow.


### Functional gating

- we need to run all Functest patches before merge against reference
plateforms (OpenStack and Kubernetes)
- a voting job must forbid the merge if one test fails (as the workflow
process implemented by OpenStack)


### Improve the current daily model

- all Functest jobs are linked to the OPNFV installers and can hardly be
  reused by endusers
- all test suites are run sequentially
- rally_full is excluded due to its duration (~3 hours)
- all possible remaining resources are cleant when installing the scenarios

**It's fine for gating installers but not for verifying that Functest supports parallel and live testing**


### New Xtesting Ansible role

- deploy anywhere the full OPNFV CI/CD toolchain in few commands
- easily add external bots voting in reviews
- produce all Xtesting-based fonctional jobs (Xtesting, Functest and Functest
  Kubernetes) in Releng
- could be instanciated for testing services out of the infrastructure domain

**It's already in a [good shape](https://lists.opnfv.org/g/opnfv-tech-discuss/message/22552). [Try it!](https://wiki.opnfv.org/pages/viewpage.action?pageId=32015004)**



## Quality Assurance

**Functest is matching the OpenStack Quality Golden rules**


### Pylint and coverage (started from E release)
- only need to refactor several vnf testcases and to remove duplicated code
- document well and cover Functest utils: they are reused by
OPNFV third-parties (SFC, SDNVPN)

** Functest will be rated 10/10 very soon**


### releasing

- Functest could be also released as a classical Python packages like Xtesting(
[PyPI](https://pypi.python.org/pypi))
- Xtesting and Functest could be released as GNU/Linux distribution packages



## other challenges


### proposals

- integrate Rally and Tempest as core modules in Functest (we do merge tempest.py and
  conf_utils.py)
- deploy cloud-native VNF (Clearwater IMS?)
- why not leveraging on OpenStack middlewares such as
  [oslo.config](https://docs.openstack.org/oslo.config/latest/)?
- promote our VNF testcases in the upstream communities

**Any new testcase is more than welcome!**



## Thank you
