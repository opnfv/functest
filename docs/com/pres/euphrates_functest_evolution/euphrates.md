# Functest
### Feedback on Euphrates evolutions

2017/10/09


### Main Framework evolutions
  * Functest Framework refactoring
  * Docker slicing with Alpine
  * Building Functest dockers
  * Requirement management...1st time...in OPNFV
  * Functest API


## Functest Framework refactoring

### The framework
  * Initiated in Danube
  * Finalized in euphrates
  * Goal: ease the integration of feature/vnf tests

### See complete presentation on the framework
http://testresults.opnfv.org/functest/framework/


## Docker slicing


#### Short story of Functest Docker


### Many rivers to cross
| Version     | Comment                                             |
|-------------|-----------------------------------------------------|
| Arno        | No docker, all tests initiated from the jumphost    |
| Brahmaputra | Introduction of Docker                              |
| Colorado    | Growth of Historical Docker                         |
| Danube      | Growth of Historical Docker                         |
| Euphrates   | Introduction of Alpine                              |


### Focus on the Historical Docker
  * Based on ubuntu 14.04

| Version      | Compressed Size |
|--------------|-----------------|
| Brahmaputra  |  354 MB         |
| Colorado.1.0 |  627 MB         |
| Danube.1.0   |  713 MB         |
| cvp.0.2.0    |  710 MB         |

* src: https://hub.docker.com/r/opnfv/functest/tags/


### Introduction to Alpine
* Alpine Linux is a GNU/Linux distribution based on musl and Busybox
* Hardened kernel, compiles all user space binaries as position-independent executables with stack-smashing protection.
* Docker Alpine leverage Alpine Linux: https://docs.docker.com/samples/library/alpine/


### Our goals
* Lighten docker / save bandwidth / save CI resources
* Slice testing
* Simplify Requirement management
* Isolate "exotic" test cases


### From 1 to many dockers
| Docker      | Size  |  Role                                           |
|-------------|-------|-------------------------------------------------|
| core        | 122MB | baseline (tools, env)                           |
| healthcheck | 122MB | OS connectivity, API, DHCP testing              |
| smoke       | 131MB | vpings, Tempest/Refstack, Rally, odl, Snaps     |
| features    | 214MB | doctor, domino, sdnvpn, sfc, promise, barometer |


### From 1 to many dockers
| Docker      | Size  |  Role                                           |
|-------------|-------|-------------------------------------------------|
| components  | 122MB | Full Tempest, Full Rally                        |
| vnf         | 155MB | vIMS, vRouter                                   |
| parser      | 127MB | parser (feature needs pike clients)             |


### Easy way to run
src: https://wiki.opnfv.org/display/functest/Run+Alpine+Functest+containers
  * env: OPNFV env variables
  * openstack.creds: OpenStack rc file

```
sudo docker run --env-file env \
    -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/openstack.creds  \
    -v $(pwd)/images:/home/opnfv/functest/images  \
    opnfv/functest-smoke:euphrates
```


#### Env
```
cat env
INSTALLER_TYPE=Compass
INSTALLER_IP=XXX
EXTERNAL_NETWORK=ext-net
DEPLOY_SCENARIO=os-nosdn-nofeature-ha
```


#### openstack.creds
```
cat openstack.creds
export OS_AUTH_URL=XXX
export OS_USER_DOMAIN_NAME=XXX
export OS_PROJECT_DOMAIN_NAME=XXX
export OS_USERNAME=XXX
export OS_PROJECT_NAME=XXX
export OS_PASSWORD=XXX
export OS_IDENTITY_API_VERSION=3
```


#### Retrieve all the images
```
mkdir -p images && wget -q -O- https://git.opnfv.org/functest/plain/functest/ci/download_images.sh | sh -s -- images && ls -1 images/*
images/CentOS-7-aarch64-GenericCloud.qcow2
images/CentOS-7-aarch64-GenericCloud.qcow2.xz
images/CentOS-7-x86_64-GenericCloud.qcow2
images/cirros-0.3.5-x86_64-disk.img
images/cirros-0.3.5-x86_64-lxc.tar.gz
images/cirros-d161201-aarch64-disk.img
images/cirros-d161201-aarch64-initramfs
images/cirros-d161201-aarch64-kernel
images/cloudify-manager-premium-4.0.1.qcow2
images/img
images/trusty-server-cloudimg-amd64-disk1.img
images/ubuntu-14.04-server-cloudimg-amd64-disk1.img
images/ubuntu-14.04-server-cloudimg-arm64-uefi1.img
images/ubuntu-16.04-server-cloudimg-amd64-disk1.img
images/vyos-1.1.7.img
```
* could be improved (retrieve only needed images Tier/config)


#### Results
```
+----------------------+--------- + ------+----------+--------+
|      TEST CASE       | PROJECT  |  TIER | DURATION | RESULT |
+----------------------+--------- + ------+----------+--------+
|      vping_ssh       | functest | smoke |  01:19   |  PASS  |
|    vping_userdata    | functest | smoke |  01:56   |  PASS  |
| tempest_smoke_serial | functest | smoke |  26:30   |  PASS  |
|     rally_sanity     | functest | smoke |  19:42   |  PASS  |
|   refstack_defcore   | functest | smoke |  22:00   |  PASS  |
|     snaps_smoke      | functest | smoke |  41:14   |  PASS  |
|         odl          | functest | smoke |  00:16   |  PASS  |
|     odl_netvirt      | functest | smoke |  00:00   |  SKIP  |
|         fds          | functest | smoke |  00:00   |  SKIP  |
+----------------------+--------- + ------+----------+--------+

```


#### Easy way to customize
  * Change list of testcase -v your_config.yaml:/usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
  * Change logger param -v your_logger.ini:/usr/lib/python2.7/site-packages/functest/ci/logging.ini


#### Docker slicing technical presentation
http://testresults.opnfv.org/functest/dockerslicing/



## Building Functest dockers


#### Until Danube
  * the unique Functest docker was "produced" from Releng


#### For Euphrates, build was done on Docker hub
  * Releng adaptations not ready in time
  * more capabilities using Docker Hub
  * Use of private ollivier then official opnfv Docker Hub
  * Euphrates 5.1: come back to releng with at least same level of features than Docker Hub/Travis CI



## Requirement management
Until now, requirements were managed as follow:


# ?


### Requirement management
  * Nothing was done
  * Danube, Colorado, .. dockers may run but no garantee on mid/long term because
    * No control of upstream or internal project dependencies
    * the dependencies of the last feature project overwrite the previous ones


###  Requirement management
  * Nothing done in any OPNFV project
    * No dependency list, no reco (e.g. support Python 3)
    * Only high level wiki declarative intentions for OpenStack (e.g. Euphrates => Ocata)
  * Nothing equivalent to OpenStack https://releases.openstack.org/ocata/


###  Functest evolutions
  * creation of requirements.txt, upper-constraints.text
  https://git.opnfv.org/functest/tree/requirements.txt
  https://git.opnfv.org/functest/tree/upper-constraints.txt
  ```
  pbr>=1.8 # Apache-2.0
  PyYAML>=3.10.0 # MIT
  GitPython>=1.0.1 # BSD License (3 clause)
  keystoneauth1>=2.18.0 # Apache-2.0
  python-cinderclient!=1.7.0,!=1.7.1,>=1.6.0 # Apache-2.0
  python-glanceclient>=2.5.0 # Apache-2.0
  python-heatclient>=1.6.1 # Apache-2.0
  ...
  ```
  * sync with ocata done manually by Cédric


###  Functest evolutions
  * Code of the feature projects under project responsibility
    * code moved to their own repo
    * no more mix between Functest and Feature project code
  * All python OPNFV projects imported properly as python modules
  * all dependencies a priori under control...



## Functest Rest API


### Introduction
* A Rest API has been introduced in Euphrates (Linda)
* Goal: allow third party to invoke Functest resources
  * pseudo micro services approach
  * avoid overlap (e.g. deployement of vIMS from other project to run perfo tests)
src: https://wiki.opnfv.org/display/functest/Functest+REST+API


### Functest rest API
| resource    | Methods  |  Description                                    |
|-------------|----------|-------------------------------------------------|
| environment | GET,POST | show, prepare environment                       |
| openstack   | GET,POST | show, check, clean, update credentials          |
| testcases   | GET,POST | list, show, run                                 |
| tiers       | GET,POST | list, show                                      |
| tasks       | GET      | Get the result of the task id                   |


### Examples
```
curl -X POST --header "Content-Type: application/json" \
  --data '{"action":"run_test_case", "args": {"opts": {}, "testcase": "vping_ssh"}}' \
  http://127.0.0.1:5000/api/v1/functest/testcases/action
{
    "task_id": "1a9f3c5d-ce0b-4354-862e-dd08b26fc484",
    "testcase":"vping_ssh"
}
```



## Conclusions
  * Framework heavily refactored for Euphrates
  * Better code quality and rules (coverage, pylint, pep8, ..)
  * Much more "trustable", light and evolutive


## Next steps
  * Still lots of work for Fraser
    * Adaptation to use it for XCI gating (xTesting)
    * Generic dockerfile Functest customized docker on demand
    * split framework and testcases in order to be able to reuse Functest for k8 or even beyond OPNFV
    * integrate k8 tests
    * better management of the images
    * ...
