# Functest on steroids

[Cédric Ollivier](mailto:cedric.ollivier@orange.com)

2019/01/08



## OPNFV

![OPNFV](https://docs.opnfv.org/en/stable-fraser/_images/OPNFV_testing_working_group1.png)
<!-- .element: style="border: 0; width: 90%" -->



## Verify OpenStack and Kubernetes


### Functest in a nutshell

- verify any kind of OpenStack and Kubernetes deployments
- conform with upstream rules (OpenStack gate jobs and Kubernetes conformance
  tests)
- ensure that the platforms meet Network Functions Virtualization requirements


### Functest suites

- as many upstream functional tests as possible (e.g. Tempest,
  neutron-tempest-api, Barbican, Patrole...)
- upstream API and dataplane benchmarking tools (Rally, Vmtp and Shaker)
- additional VNF deployments and testing (vIMS, vRouter and vEPC)

**Dovetail only runs few Functest functional tests and then we have to verify
any OPNFV-certified scenarios via Functest anyway**


### What's new in Functest?

- new testcases were quickly integrated in Functest: Patrole, Barbican, Shaker,
  ...
- all testcases can run in parallel to decrease the overall duration
- the resources cleaning has been improved
- **our testcases may be run vs VIM in production**
- **it includes most of the OpenStack gate jobs**


### Support of OS and K8s master

| Functest | OpenStack   | Kubernetes |
| :------: | :---------: | :--------: |
| master   | master      | master     |
| hunter   | rocky       | v1.11.3    |
| gambia   | queens      | v1.11.3    |


### < 50 Euros

![Raspberry PI](raspberrypi.jpg)
<!-- .element: style="border: 0; width: 70%" -->



## Reuse of OPNFV


### Xtesting in a nutshell

- allow the developer to work only on the test suites without diving into CI/CD
  integration
- simplify test integration in a complete LFN-based CI/CD toolchain (e.g.
  Jenkins, Testing Containers, Test API and dashboard)
- allow a proper design and verify multiple components in the same CI/CD
  toolchain (OpenStack, Kubernetes, ONAP, etc.)

**Easy to use and very useful for any CI/CD toochain (unlinked to Infrastrure)**


### A user story ONAP

- all tests are run by a specialized Docker container(**<100 MB**) instead of
the classical ONAP testing virtual machine (**> 1GB**).
- the container mainly inherits from opnfv/xtesting and is completed by:
  - Python dependencies
  - all ONAP Robot Framework files retrieved from the original repositories
  - testcases.yaml describing the testcases

[Orange-OpenSource/xtesting-onap-robot](https://github.com/Orange-OpenSource/xtesting-onap-robot/)  


###  What's new in Xtesting?

- new ansible roles and playbooks have been developed to allow **deploying your
  full CI/CD toolchains in few minutes** (Jenkins, Minio, TestAPI, MongoDB and
  Docker registry)

```shell
virtualenv xtesting
. xtesting/bin/activate
pip install ansible docker
ansible-galaxy install collivier.xtesting
git clone https://gerrit.opnfv.org/gerrit/functest-xtesting functest-xtesting-src
ansible-playbook functest-xtesting-src/ansible/site.yml
deactivate
```

**They are already reused in Functest and by Orange out of the
Infrastrure domain**



## Collect results


### OPNFV Test Database in a nutshell

- it's a fair comparison of Neutron implementations (Agents vs SDN
  controller)
- it stores all verification results and all performance data from different
  hardware over the world which could be easily postprocessed
- it could be very useful to select the adequate opensource solutions
  regarding metrics and capabilities


### which Neutron backend?

- most Neutron standalone and OVN scenarios pass Functest decently
- no ODL scenarios pass the advanced testcases (benchmarking tools and
  VNFs). It's still unclear if it's due to the Installers, ODL or POD
  misconfigurations.
- no Tungsten Fabric is released in Gambia

**We expected that ODL results would have improved before the first Gambia
  corrective**


### Contrail testing (out of OPNFV)

- **3.X 4.X**: mostly verified except some functional tests about
  visibility which fail due to the falsy admin role (they can be easily
  blacklisted)
- **5.X**: a limited set of bugs in Contrail mostly forbid running few
  functional tests and benchmarking tools:
  - wrong external network listing
  - Contrail doesn't allow booting a VM without network (and elects the wrong
    network)


### And performance?

- OVS DPDK is not fully integrated by an OPNFV installer (Fuel is in a good
  shape to support it)
- the only scenario including VPP is not part of Gambia

**From the time being, we can't evaluate the benefits of OVS DPDK or VPP thanks
  to OPNFV**



## Conclusion


### Gambia

- Functest and Xtesting are powerful and easy to (re)use (containers, jenkins
  jobs, ansible playbooks, Raspberry PI, etc.).
- the number of installers and scenarios decreased in Gambia (it's still
  unclear regarding the overall quality). **What about OPNFV Test Database if
  it decreases again in 2019?**


### And beyond

- test frameworks are now considered as crucial for OPNFV (see [Last OPNFV Marketing update](https://wiki.opnfv.org/download/attachments/2925933/OPNFV%20Marketing%20Update%20091818.pptx?version=1&modificationDate=1537228648000&api=v2)) and Functest and Xtesting could be
already widely reused out of OPNFV
- the new test-driven approach as proposed by the [OPNFV Strategic Plan](https://wiki.opnfv.org/download/attachments/2925933/OPNFV%20Strategy%20and%20Plan%20v0.5.pptx?version=1&modificationDate=1540961098000&api=v2) could increase **the quality of all
scenarios**. But we are also suggesting to let the installers decide their
test cases.
