# Rally tests for OpenStack

Original Rally testsuites can be found here: https://github.com/stackforge/rally 

---
## Intro
In order to perform functional and performance testing, we use a dedicated VM.

    TODO: add test-tool VM in architecture and puppetise test-tool VM

On this VM, we installed:
* Rally: https://wiki.openstack.org/wiki/Rally

    TODO RobotFramework: http://robotframework.org, SIPP http://sipp.sourceforge.net/



## Installation & Configuration

### Rally

* Log on the test-tool VM
* install Rally (https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html)

openrc file (info from OpenStack) is needed, password is required during configuration procedure

* check 
```bash
# rally deployment check
keystone endpoints are valid and following service are available:
+-------------+-----------+------------+
| Services  | Type        | Status     |
+-----------+-------------+------------+
| cinder    | volume      | Available  |
| cinderv2  | volumev2    | Available  |
| glance    | image       | Available  |
| keystone  | identity    | Available  | 
| neutron   | network     | Available  |
| nova      | compute     | Available  |
| nova_ec2  | compute_ec2 | Available  |
| novav3    | computev3   | Available  |
+-----------+-------------+------------+

```

* For Rally scenario, follow https://rally.readthedocs.org/en/latest/tutorial/step_1_setting_up_env_and_running_benchmark_from_samples.html
```bash
# rally task start ./samples/tasks/scenarios/nova/my-boot-and-delete.json 
--------------------------------------------------------------------------------
 Preparing input task
--------------------------------------------------------------------------------

Input task is:
{
    "NovaServers.boot_and_delete_server": [
        {
            "args": {
                "flavor": {
                    "name": "m1.small"
                },
                "image": {
                    "name": "^ubuntu-14.10-64b"
                },
                "force_delete": false
            },
            "runner": {
                "type": "constant",
                "times": 10,
                "concurrency": 2
            },
            "context": {
                "users": {
                    "tenants": 3,
                    "users_per_tenant": 2
                }
            }
        }
    ]
}

--------------------------------------------------------------------------------
 Task  f42c8aed-00a6-4715-9951-945b4fb97c32: started
--------------------------------------------------------------------------------

Benchmarking... This can take a while...

To track task status use:

	rally task status
	or
	rally task detailed
	
--------------------------------------------------------------------------------
Task f42c8aed-00a6-4715-9951-945b4fb97c32: finished
--------------------------------------------------------------------------------

test scenario NovaServers.boot_and_delete_server
args position 0
args values:
OrderedDict([(u'runner', OrderedDict([(u'type', u'constant'), (u'concurrency', 2), (u'times', 10)])), (u'args', OrderedDict([(u'force_delete', False), (u'flavor', OrderedDict([(u'name', u'm1.small')])), (u'image', OrderedDict([(u'name', u'^ubuntu-14.10-64b')]))])), (u'context', OrderedDict([(u'users', OrderedDict([(u'project_domain', u'default'), (u'users_per_tenant', 2), (u'tenants', 3), (u'resource_management_workers', 30), (u'user_domain', u'default')]))]))])
+--------------------+-----------+-----------+-----------+---------------+---------------+---------+-------+
| action             | min (sec) | avg (sec) | max (sec) | 90 percentile | 95 percentile | success | count |
+--------------------+-----------+-----------+-----------+---------------+---------------+---------+-------+
| nova.boot_server   | 4.675     | 5.554     | 6.357     | 6.289         | 6.323         | 100.0%  | 10    |
| nova.delete_server | 2.365     | 3.301     | 4.728     | 4.553         | 4.64          | 100.0%  | 10    |
| total              | 7.303     | 8.857     | 10.789    | 10.543        | 10.666        | 100.0%  | 10    |
+--------------------+-----------+-----------+-----------+---------------+---------------+---------+-------+
Load duration: 45.7972288132
Full duration: 58.912060976

HINTS:
* To plot HTML graphics with this data, run:
	rally task report f42c8aed-00a6-4715-9951-945b4fb97c32 --out output.html

* To get raw JSON output of task results, run:
	rally task results f42c8aed-00a6-4715-9951-945b4fb97c32

Using task: f42c8aed-00a6-4715-9951-945b4fb97c32

```
* For Tempest, follow the instructions https://www.mirantis.com/blog/rally-openstack-tempest-testing-made-simpler
* In first step Rally scenario were fine but Tempest scenarios failed due to configuration
Apply patch https://review.openstack.org/#/c/163330/
```bash
pip uninstall rally && cd ./rally && python setup.py install
```

You shall be able to run Rally/Tempest towards your OpenStack
```bash
root@rally:~/rally# rally verify start
[...]
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest
    test_attach_volumes_with_nonexistent_volume_id[compute,gate,id-f5e56b0a-5d02-43c1-a2a7-c9b792c2e3f6,negative]FAIL
    test_create_volume_with_invalid_size[gate,id-1ed83a8a-682d-4dfb-a30e-ee63ffd6c049,negative]OK  0.02
    test_create_volume_with_nonexistent_snapshot_id[gate,id-0c36f6ae-4604-4017-b0a9-34fdc63096f9,negative]OK  0.04
    test_create_volume_with_nonexistent_source_volid[gate,id-47c73e08-4be8-45bb-bfdf-0c4e79b88344,negative]OK  0.05
    test_create_volume_with_nonexistent_volume_type[gate,id-10254ed8-3849-454e-862e-3ab8e6aa01d2,negative]OK  0.02
    test_create_volume_with_out_passing_size[gate,id-9387686f-334f-4d31-a439-33494b9e2683,negative]OK  0.02
    test_create_volume_with_size_negative[gate,id-8b472729-9eba-446e-a83b-916bdb34bef7,negative]OK  0.02
[...]
Ran 933 tests in 1020.200s

FAILED (failures=186)
Test set 'full' has been finished with error. Check log for details

```

It is possible to get a better view on the result
```bash
# rally verify list
+--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------------+----------+
| UUID                                 | Deployment UUID                      | Set name | Tests | Failures | Created at                 | Duration       | Status   |
+--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------------+----------+
| b1de3608-dbee-40e7-84c4-1c756ca0347c | e7d70ddf-9be0-4681-9456-aa8dce515e0e | None     | 0     | 0        | 2015-03-11 08:48:04.416793 | 0:00:00.102275 | running  |
| ff0d9285-184f-47d5-9474-7475135ae8cf | e7d70ddf-9be0-4681-9456-aa8dce515e0e | full     | 933   | 186      | 2015-03-11 09:57:01.836611 | 0:18:08.360204 | finished |
| fec2fd0a-a4ef-4064-a292-95e9da68025c | e7d70ddf-9be0-4681-9456-aa8dce515e0e | full     | 933   | 186      | 2015-03-12 09:46:40.818691 | 0:17:02.316443 | finished |
+--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------------+----------+

rally verify show fec2fd0a-a4ef-4064-a292-95e9da68025c
Total results of verification:

+--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
| UUID                                 | Deployment UUID                      | Set name | Tests | Failures | Created at                 | Status   |
+--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
| fec2fd0a-a4ef-4064-a292-95e9da68025c | e7d70ddf-9be0-4681-9456-aa8dce515e0e | full     | 933   | 186      | 2015-03-12 09:46:40.818691 | finished |
+--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+

Tests:

+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------+--------+
| name                                                                                                                                                                                                      | time      | status |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------+--------+
| tearDownClass (tempest.api.image.v1.test_images.CreateRegisterImagesTest)                                                                                                                                 | 0.0       | FAIL   |
| tearDownClass (tempest.api.image.v1.test_images.UpdateImageMetaTest)                                                                                                                                      | 0.0       | FAIL   |
[...]
| tempest.cli.simple_read_only.volume.test_cinder.SimpleReadOnlyCinderClientTest.test_cinder_quota_show[id-18166673-ffa8-4df3-b60c-6375532288bc]                                                            | 1.309555  | OK     |
| tempest.cli.simple_read_only.volume.test_cinder.SimpleReadOnlyCinderClientTest.test_cinder_rate_limits[id-b2c66ed9-ca96-4dc4-94cc-8083e664e516]                                                           | 1.277704  | OK     |
| tempest.cli.simple_read_only.volume.test_cinder.SimpleReadOnlyCinderClientTest.test_cinder_region_list[id-95a2850c-35b4-4159-bb93-51647a5ad232]                                                           | 1.105877  | FAIL   |
| tempest.cli.simple_read_only.volume.test_cinder.SimpleReadOnlyCinderClientTest.test_cinder_retries_list[id-6d97fcd2-5dd1-429d-af70-030c949d86cd]                                                          | 1.306407  | OK     |
| tempest.cli.simple_read_only.volume.test_cinder.SimpleReadOnlyCinderClientTest.test_cinder_service_list[id-301b5ae1-9591-4e9f-999c-d525a9bdf822]                                                          | 1.24909   | OK     |
| tempest.cli.simple_read_only.volume.test_cinder.SimpleReadOnlyCinderClientTest.test_cinder_snapshot_list[id-7a19955b-807c-481a-a2ee-9d76733eac28]                                                         | 1.270242  | OK     |
[...]
| tempest.thirdparty.boto.test_s3_ec2_images.S3ImagesTest                                                                                                                                                   | 0.0       | SKIP   |
| tempest.thirdparty.boto.test_s3_objects.S3BucketsTest.test_create_get_delete_object[id-4eea567a-b46a-405b-a475-6097e1faebde]                                                                              | 0.239222  | FAIL   |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------+--------+

```
Rally includes a reporting tool
https://rally.readthedocs.org/en/latest/tutorial/step_1_setting_up_env_and_running_benchmark_from_samples.html





## Test description

### Rally

By default, the different Rally Scenarios are:
```bash

ls samples/tasks/scenarios/
authenticate  cinder     dummy   heat      mistral  nova    README.rst  sahara                                 vm
ceilometer    designate  glance  keystone  neutron  quotas  requests    tempest-do-not-run-against-production  zaqar

```

tempest tests can be retrieved at https://github.com/openstack/tempest


## Automation
