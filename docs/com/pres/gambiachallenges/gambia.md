# Functest Gambia, new challenges

[Cédric Ollivier](mailto:cedric.ollivier@orange.com)

2018/03/22



## Gating


### Our gating is very simple

- today all test suites are run sequentially
- all resources are not necessarily cleant until the next OpenStack deployment

**It's fine for gating installers but not for verifying a production
environment (e.g. multi users running the same testcase)**


### Parallel and Live testing

- all resources should be allocated in their own OpenStack projects (already
  mostly the case)
- no testcase should create singletons on resource attributes (name, ip, etc.)
- all resources have to be cleant at the end

**According to [Orange testing results](https://wiki.opnfv.org/pages/viewpage.action?pageId=13211751),
Functest is already in a good shape to meet this goal**



## Quality Assurance

**Gambia release will match the OpenStack Quality Golden rules**


### Pylint and coverage (started from E release)
- need to refactor several vnf testcases and to remove duplicated code
- document well and cover Functest utils: they are reused by
OPNFV third-parties (SFC, SDNVPN)

** Functest will be rated 10/10**


### releasing

- Functest could be also released as a classical Python package (
[PyPI](https://pypi.python.org/pypi))
- its API docs could be published in [Read the Docs](https://readthedocs.org/)


### Current technical debt
- former python modules (e.g. cli) or containers (e.g. restapi) have to be
removed
- functest shouldn't contain any OPNFV Installer logic. **All Jenkins Jobs
must set the right env vars as all endusers**
- vnf descriptors should be hosted by Functest instead of using external github
repositories



## other challenges


### proposals

- ease integrating tempest plugins with a minimum effort (new tempest driver in Functest Framework and new opnfv/functest-tempest container)
- why not leveraging on OpenStack middlewares such as
  [oslo.config](https://docs.openstack.org/oslo.config/latest/) or
  [stevedore](https://docs.openstack.org/stevedore/latest/)?

**Any new testcase is more than welcome!**



## Thank you
