# Docker slicing



## Current issues


### Dockerfile

- it copies all the files hosted by the third-party projects (eg docs, .git...)
- several requirements are downgraded/upgraded when building the container as they are managed one after the other
- it could download packages from [PyPI](https://pypi.python.org/pypi) (e.g. [rally](https://pypi.python.org/pypi/rally/)...) instead of cloning git repository
- we can't remove build dependencies to save space as it creates multiple layers (>70)


### setup.py

- no requirement is installed when calling *python setup.py install* as none of the next keys are set:
    - install_requires
    - tests_require
    - dependency_links
- shell scripts are not installed neither in $PATH nor in dist-packages


### setup.py

- master is considered as an incorrect version
- empty package_data seems useless
- zip_safe flag could be set as False as \__file__ would prevent functest from working in a zipfile
- py_modules should not list cli_base as it was moved into functest package



## Proposals


### why not relying on [pbr](https://docs.openstack.org/developer/pbr/)?

- pbr injects requirements into the install_requires, tests_require and/or dependency_links arguments to setup
- it supports conditional dependencies which can be added to the requirements (e.g. subprocess32; python_version=='2.7')


### setup.py

```python
#!/usr/bin/env python

from setuptools import setup

setup(
    setup_requires=['pbr>=1.9', 'setuptools>=17.1'],
    pbr=True,
)
```


### setup.cfg

```ini
[metadata]
name = functest
version = 5
home-page = https://wiki.opnfv.org/display/functest

[files]
packages = functest
scripts =
    docker/docker_remote_api/enable_remote_api.sh
    docker/add_images.sh
    docker/config_install_env.sh

[entry_points]
console_scripts =
    functest = functest.cli.cli_base:cli
```


### Split requirements into (at least) 3 files

- **requirements.txt** which could list all abstract (i.e. [not associated with any particular index](https://packaging.python.org/requirements/)) dependencies of the functest package
- **test-requirements.txt** which could list all abstract dependencies required for testing the functest package
- **thirdparty-requirements.txt** which could list all abstract and concrete dependencies required by the full functest docker container


### tox.ini

```ini
[testenv]
usedevelop = True
deps =
  -r{toxinidir}/requirements.txt
  -r{toxinidir}/test-requirements.txt
  git+https://gerrit.opnfv.org/gerrit/releng#egg=opnfv&subdirectory=modules
  git+https://gerrit.opnfv.org/gerrit/barometer#egg=baro_tests
  git+https://gerrit.opnfv.org/gerrit/snaps#egg=snaps

```


### Dockerfile

```
RUN pip install \
  git+https://gerrit.opnfv.org/gerrit/functest@$BRANCH#egg=functest \
  git+https://gerrit.opnfv.org/gerrit/releng@$BRANCH#egg=opnfv\&subdirectory=modules \
  git+https://gerrit.opnfv.org/gerrit/barometer@$BRANCH#egg=baro_tests \
  git+https://gerrit.opnfv.org/gerrit/snaps@$BRANCH#egg=snaps
```


### Switch to Alpine

```
FROM alpine:3.5

RUN apk --no-cache add --update \
        python libffi libssl1.0 libjpeg-turbo py-pip && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev git && \
    pip install git+https://gerrit.opnfv.org/gerrit/releng#egg=opnfv\&subdirectory=modules \
        git+https://gerrit.opnfv.org/gerrit/barometer#egg=baro_tests \
        git+https://gerrit.opnfv.org/gerrit/snaps#egg=snaps \
        git+https://gerrit.opnfv.org/gerrit/functest@$BRANCH#egg=functest && \
    apk del .build-deps
```


### Status

 - the change [**"leveraging on pbr"**](https://gerrit.opnfv.org/gerrit/#/c/35813/) can be merged
 - docker containers have been published (any test is welcome):
    - [ollivier/functest-pbr](https://hub.docker.com/r/ollivier/functest-pbr/)
    - [ollivier/functest-alpine](https://hub.docker.com/r/ollivier/functest-alpine/)
 - the Dockerfile switching to Alpine can be published too



## Next steps


### docker slicing

the previous alpine example could be the base image and we could simply create other images from it (see [FROM](https://docs.docker.com/engine/reference/builder/#from)) by installing all third party python packages


### PyPI

functest could be published to the [Python Package Index](https://pypi.python.org/pypi) and then we would stop listing urls



## on the road


### We could be faced with issues

- several test cases can fail if their requirements are incomplete in setup.py (we should help them to fix it)
- all conditions for requirements may not be compatible (OpenStack requirements as a guideline?)
- we should fix lots of hardcoded paths hidden by the previous design
- some files could be outside the python package (e.g. functest ci scripts)



## Thank You!

