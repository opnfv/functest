# Functest

Network virtualization has dramatically modified our architectures which asks
for more automation and powerful testing tools like Functest, a collection of
state-of-the-art virtual infrastructure test suites, including automatic VNF
testing (cf.
[[1]](https://www.linuxfoundation.org/press-release/2019/05/opnfv-hunter-delivers-test-tools-ci-cd-framework-to-enable-common-nfvi-for-verifying-vnfs/)).

In context of OPNFV, Functest verifies any kind of OpenStack and Kubernetes
deployments including production environments. It conforms to upstream rules
and integrates smoothly lots of the test cases available in the opensource
market. It includes about 3000+ functional tests and 3 hours upstream API and
dataplane benchmarks. It’s completed by Virtual Network Function deployments
and testing (vIMS, vRouter and vEPC) to ensure that the platforms meet Network
Functions Virtualization requirements. Raspberry PI is also supported to verify
datacenters as the lowest cost (50 euros hardware and software included).

| Functest releases | OpenStack releases |
|-------------------|--------------------|
| Hunter	          | Rocky              |
| Iruya             | Stein              |
| Jerma	            | Train              |
| Kali              | Ussuri             |
| Leguer            | Victoria           |
| **Master**	      | **next Wallaby**   |

## Prepare your environment

cat env
```
DEPLOY_SCENARIO=XXX  # if not os-nosdn-nofeature-noha scenario
NAMESERVER=XXX  # if not 8.8.8.8
EXTERNAL_NETWORK=XXX  # if not first network with router:external=True
DASHBOARD_URL=XXX  # else tempest_horizon will be skipped
NEW_USER_ROLE=XXX  # if not member
SDN_CONTROLLER_IP=XXX  # if odl scenario
VOLUME_DEVICE_NAME=XXX  # if not vdb
FLAVOR_EXTRA_SPECS=hw:mem_page_size:large  # if fdio scenarios
```

cat openstack.creds
```
export OS_AUTH_URL=XXX
export OS_USER_DOMAIN_NAME=XXX
export OS_PROJECT_DOMAIN_NAME=XXX
export OS_USERNAME=XXX
export OS_PROJECT_NAME=XXX
export OS_PASSWORD=XXX
export OS_IDENTITY_API_VERSION=3
export OS_REGION_NAME=XXX
```

mkdir -p images && wget -q -O- https://git.opnfv.org/functest/plain/functest/ci/download_images.sh | bash -s -- images && ls -1 images/*
```
images/cirros-0.5.1-aarch64-disk.img
images/cirros-0.5.1-x86_64-disk.img
images/cloudify-docker-manager-community-19.01.24.tar
images/Fedora-Cloud-Base-30-1.2.x86_64.qcow2
images/shaker-image-1.3.0+stretch.qcow2
images/ubuntu-14.04-server-cloudimg-amd64-disk1.img
images/ubuntu-14.04-server-cloudimg-arm64-uefi1.img
images/ubuntu-16.04-server-cloudimg-amd64-disk1.img
images/vyos-1.1.8-amd64.qcow2
```

## Run healthcheck suite

```bash
sudo docker run --env-file env \
    -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
    -v $(pwd)/images:/home/opnfv/functest/images \
    opnfv/functest-healthcheck
```

```
+--------------------------+------------------+---------------------+------------------+----------------+
|        TEST CASE         |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
+--------------------------+------------------+---------------------+------------------+----------------+
|     connection_check     |     functest     |     healthcheck     |      00:03       |      PASS      |
|      tenantnetwork1      |     functest     |     healthcheck     |      00:05       |      PASS      |
|      tenantnetwork2      |     functest     |     healthcheck     |      00:06       |      PASS      |
|         vmready1         |     functest     |     healthcheck     |      00:06       |      PASS      |
|         vmready2         |     functest     |     healthcheck     |      00:08       |      PASS      |
|        singlevm1         |     functest     |     healthcheck     |      00:32       |      PASS      |
|        singlevm2         |     functest     |     healthcheck     |      00:37       |      PASS      |
|        vping_ssh         |     functest     |     healthcheck     |      00:46       |      PASS      |
|      vping_userdata      |     functest     |     healthcheck     |      00:39       |      PASS      |
|       cinder_test        |     functest     |     healthcheck     |      01:05       |      PASS      |
|      tempest_smoke       |     functest     |     healthcheck     |      05:39       |      PASS      |
|     tempest_horizon      |     functest     |     healthcheck     |      01:05       |      PASS      |
|           odl            |     functest     |     healthcheck     |      00:00       |      SKIP      |
+--------------------------+------------------+---------------------+------------------+----------------+
```

## Run smoke suite

```bash
sudo docker run --env-file env \
    -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
    -v $(pwd)/images:/home/opnfv/functest/images \
    opnfv/functest-smoke
```

```
+---------------------------+------------------+---------------+------------------+----------------+
|         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
+---------------------------+------------------+---------------+------------------+----------------+
|      tempest_neutron      |     functest     |     smoke     |      15:30       |      PASS      |
|       tempest_cinder      |     functest     |     smoke     |      02:01       |      PASS      |
|      tempest_keystone     |     functest     |     smoke     |      01:17       |      PASS      |
|        tempest_heat       |     functest     |     smoke     |      22:14       |      PASS      |
|     tempest_telemetry     |     functest     |     smoke     |      00:00       |      SKIP      |
|        rally_sanity       |     functest     |     smoke     |      17:24       |      PASS      |
|      refstack_compute     |     functest     |     smoke     |      07:03       |      PASS      |
|      refstack_object      |     functest     |     smoke     |      02:09       |      PASS      |
|     refstack_platform     |     functest     |     smoke     |      07:31       |      PASS      |
|        tempest_full       |     functest     |     smoke     |      41:52       |      PASS      |
|      tempest_scenario     |     functest     |     smoke     |      08:42       |      PASS      |
|        tempest_slow       |     functest     |     smoke     |      43:42       |      PASS      |
|       patrole_admin       |     functest     |     smoke     |      21:06       |      PASS      |
|       patrole_member      |     functest     |     smoke     |      21:23       |      PASS      |
|       patrole_reader      |     functest     |     smoke     |      21:56       |      PASS      |
|      tempest_barbican     |     functest     |     smoke     |      02:30       |      PASS      |
|      tempest_octavia      |     functest     |     smoke     |      00:00       |      SKIP      |
|       tempest_cyborg      |     functest     |     smoke     |      00:00       |      SKIP      |
+---------------------------+------------------+---------------+------------------+----------------+
```

## Run smoke CNTT suite

```bash
sudo docker run --env-file env \
    -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
    -v $(pwd)/images:/home/opnfv/functest/images \
    opnfv/functest-smoke-cntt
```

```
+-------------------------------+------------------+---------------+------------------+----------------+
|           TEST CASE           |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
+-------------------------------+------------------+---------------+------------------+----------------+
|      tempest_neutron_cntt     |     functest     |     smoke     |      11:35       |      PASS      |
|      tempest_cinder_cntt      |     functest     |     smoke     |      01:58       |      PASS      |
|     tempest_keystone_cntt     |     functest     |     smoke     |      01:13       |      PASS      |
|       tempest_heat_cntt       |     functest     |     smoke     |      22:32       |      PASS      |
|       rally_sanity_cntt       |     functest     |     smoke     |      17:16       |      PASS      |
|       tempest_full_cntt       |     functest     |     smoke     |      41:13       |      PASS      |
|     tempest_scenario_cntt     |     functest     |     smoke     |      08:57       |      PASS      |
|       tempest_slow_cntt       |     functest     |     smoke     |      35:58       |      PASS      |
+-------------------------------+------------------+---------------+------------------+----------------+
```

## Run benchmarking suite

```bash
sudo docker run --env-file env \
    -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
    -v $(pwd)/images:/home/opnfv/functest/images \
    opnfv/functest-benchmarking
```

```
+--------------------+------------------+----------------------+------------------+----------------+
|     TEST CASE      |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
+--------------------+------------------+----------------------+------------------+----------------+
|     rally_full     |     functest     |     benchmarking     |      93:03       |      PASS      |
|     rally_jobs     |     functest     |     benchmarking     |      27:05       |      PASS      |
|        vmtp        |     functest     |     benchmarking     |      17:56       |      PASS      |
|       shaker       |     functest     |     benchmarking     |      24:02       |      PASS      |
+--------------------+------------------+----------------------+------------------+----------------+
```

## Run benchmarking CNTT suite

```bash
sudo docker run --env-file env \
    -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
    -v $(pwd)/images:/home/opnfv/functest/images \
    opnfv/functest-benchmarking-cntt
```

```
+-------------------------+------------------+----------------------+------------------+----------------+
|        TEST CASE        |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
+-------------------------+------------------+----------------------+------------------+----------------+
|     rally_full_cntt     |     functest     |     benchmarking     |      89:52       |      PASS      |
|     rally_jobs_cntt     |     functest     |     benchmarking     |      19:39       |      PASS      |
|           vmtp          |     functest     |     benchmarking     |      16:59       |      PASS      |
|          shaker         |     functest     |     benchmarking     |      23:43       |      PASS      |
+-------------------------+------------------+----------------------+------------------+----------------+
```

## Run vnf suite

```bash
sudo docker run --env-file env \
    -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/env_file \
    -v $(pwd)/images:/home/opnfv/functest/images \
    opnfv/functest-vnf
```

```
+----------------------+------------------+--------------+------------------+----------------+
|      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
+----------------------+------------------+--------------+------------------+----------------+
|       cloudify       |     functest     |     vnf      |      05:08       |      PASS      |
|     cloudify_ims     |     functest     |     vnf      |      24:46       |      PASS      |
|       heat_ims       |     functest     |     vnf      |      33:12       |      PASS      |
|     vyos_vrouter     |     functest     |     vnf      |      15:53       |      PASS      |
|       juju_epc       |     functest     |     vnf      |      27:52       |      PASS      |
+----------------------+------------------+--------------+------------------+----------------+
```
