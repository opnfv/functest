# From Verification to CNTT Compliance

[Cédric Ollivier](mailto:cedric.ollivier@orange.com)

2019/12/04



## Infrastructure Verification


### Functest in a nutshell

- verify any kind of OpenStack and Kubernetes deployments (OPNFV model)
  including production environments
- conform with upstream rules (OpenStack gate jobs and Kubernetes conformance
  tests)
- ensure that the platforms meet Network Functions Virtualization requirements


### Functest suites

- all functional tests (3000+) as defined by the upstream communities
  (e.g. Tempest, neutron-tempest-api, Barbican, Patrole...)
- 3 hours upstream API and dataplane benchmarking tests (Rally, VMTP and
  Shaker)
- Virtual Network Function deployments and testing (vIMS, vRouter and vEPC)



## CNTT Compliance


### Verification vs Compliance

- verification allows skipping test if optional services (Gnocchi, Barbican,
  etc.) or capabilities (remote console access, Neutron BGPVPN or SFC, etc.)
  are missing
- compliance forces here the full API descriptions as currently proposed by
  CNTT (please see
  [Interfaces and APIs](https://github.com/cntt-n/CNTT/blob/master/doc/ref_arch/openstack/chapters/chapter05.md))
- then the testcase descriptions should forbid skipping any test and cover only
  the mandatory services (and their mandatory capabilities)


### Changelog

- all the logics were already in Functest and the underlying frameworks (Rally,
  Tempest, etc.)
- 2 new CNTT-related containers including the new testcase descriptions were
  published to easily verify the compliance
- all 3 Functest SUTs (Rocky, Stein/Train and Master) are now compliant with
  CNTT API to ensure the continuous integration
- the benchmarking testcases doesn't validate any KPI as nothing is written in
  CNTT documentation


### RI verification and Compliance

- CNTT Reference Implementation 1 is already continuously verified
  ([continuous integration model](https://build.opnfv.org/ci/view/cntt/job/cntt-latest-daily/))
- the conformance is currently failing due to a few bugs in deployments and
  missing features

**Be free to [deploy your own CNTT Compliance CI/CD toolchain](https://wiki.opnfv.org/pages/viewpage.action?pageId=32015004)
  in a few commands**



## Conclusion


### Next steps

- fix reference implementation 1 deployments and then achieve the compliance
- port existing OPNFV testcases to Xtesting and then add them in the continuous
  integration loop
- update the testcase descritions according to the CNTT progress (KPI, API
  changes)


### Takeaways

- Functest allows verifying any production Infrastructure and now checking the
  CNTT API Compliance
- all containers can be already consumed
- any third-party certification should reuse the Functest CNTT-related
  containers as they are
- [CNTT RI continuous integration](https://build.opnfv.org/ci/view/cntt/job/cntt-latest-daily/)
  is in place and any testcase can be smoothly added if they leverage on
  Xtesting

**Try it, and you will love it!**



## Thank you
