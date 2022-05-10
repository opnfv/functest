# Docker slicing

[Cédric Ollivier](mailto:cedric.ollivier@orange.com)

2017/10/19



## Danube issues


### OPNFV projects' setup.py

- no requirements were installed when calling *python setup.py install* as none of the next keys was set:
    - install_requires
    - tests_require
    - dependency_links
- shell scripts were not installed neither in $PATH nor in dist-packages
- all requirements were not synchronized over the OPNFV projects


### Functest's Dockerfile

- it copied all the files hosted by the third-party projects (e.g. docs, .git...)
- several requirements were downgraded/upgraded when building the container as they were managed one after the other
- it could download packages from [PyPI](https://pypi.python.org/pypi) (e.g. [networking-bgpvpn](https://pypi.python.org/pypi/networking-bgpvpn)...) instead of cloning git repository
- build dependencies couldn't be removed to save space as it created multiple layers (>70)



## Management of the requirements


### Rely on [pbr](https://docs.openstack.org/developer/pbr/)

- pbr injects requirements into the install_requires, tests_require and/or dependency_links arguments to setup
- it supports conditional dependencies which can be added to the requirements (e.g. dnspython>=1.14.0;python_version=='2.7')


### Split requirements into 3 files

- **requirements.txt** which should list all abstract (i.e. [not associated with any particular index](https://packaging.python.org/requirements/)) dependencies of the OPNFV packages
- **test-requirements.txt** which could list all abstract dependencies required for testing the OPNFV packages
- **upper-constraints.txt** which should list all concrete dependencies required by Functest Docker container or the testing virtual environments


### Follow [OpenStack requirements management](https://specs.openstack.org/openstack/openstack-specs/specs/requirements-management.html)

- OPNFV (test-)requirements.txt have been updated according to stable/ocata global-requirements.txt.
- Functest simply use (and complete) stable/ocata upper-constraints.txt in Docker files and tox configuration (testing virtual environments).


### On the road

- we have fixed lots of hardcoded paths hidden by the previous design
- some files were outside the python packages
- lots of (console) scripts added in OPNFV packages to ease the maintenance of Functest testcases.yaml



## Docker slicing


### 8 Functest containers

```shell
$ sudo docker search opnfv |grep functest-
opnfv/functest-core         OPNFV Functest core image
opnfv/functest-restapi      OPNFV Functest restapi image
opnfv/functest-features     OPNFV Functest vnf image
opnfv/functest-healthcheck  OPNFV Functest healthcheck image
opnfv/functest-smoke        OPNFV Functest smoke image
opnfv/functest-vnf          OPNFV Functest vnf image
opnfv/functest-components   OPNFV Functest components image
opnfv/functest-parser       OPNFV Functest parser image
```


### 8 Functest containers

- Alpine 3.6 is now used as base image
- one container per test suite has been published (5). All of them are built on top of functest-core.
- Parser is hosted in its own containers (it requires librairies released for OpenStack Pike)
- a full container is dedicated to our REST API.

Please see [Run Alpine Functest containers](https://wiki.opnfv.org/display/functest/Run+Alpine+Functest+containers)



## Next steps


### Functest and XCI

- the purpose is simply to allow any OPNFV project integrated by Functest to build their own containers on top of opnfv/functest-core
- it will allow testing one specific change of these OPNFV projects before merging it in tree
- it induces that all requirements are synchronized between the different OPNFV projects


### F-release

- to allow building opnfv/functest-core from a gerrit change (see https://gerrit.opnfv.org/gerrit/#/c/40909/)
- to split Functest core/ci and the Functest testcases in two separated Python packages
- to unlink prepare_env.py and tempest/rally


### F-release

- to add python3 support for Functest ci scripts (Functest core already supports both versions)
- to unlink functest-core from others OPNFV projects (mainly releng and snaps)
- to write a generic Dockerfile using a set of python packages as input


### 2 OPNFV project proposals

- requirements, the counterpart of [OpenStack requirements](https://wiki.openstack.org/wiki/Requirements),
focused on additional OPNFV project needs
- xtesting which would be derived from Functest (core and ci parts) as proposed in
[Functional testing gating](https://wiki.opnfv.org/display/functest/Functional+testing+gating)



## Thank you!

