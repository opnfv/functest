# OPNFV and CNTT in Orange RFP

[Cédric Ollivier](mailto:cedric.ollivier@orange.com)

2020/09/19



## Vision and contributions


### Our guidelines

- **automate** to bring determinism and to meet the new
  software release rate
- test all software layers **independently** (OpenStack, Kubernetes and VNFs)
- run all deployment and verification jobs in **our** continous integration
  chains
- leverage best **opensource** tools and practices

**Integrate smoothly and deploy everywhere fastly**


### How OpenSource helps?

- **Functest** offers a collection of state-of-the-art virtual infrastructure
  test suites
- **Xtesting** helps assembling sparse test cases and accelerating the adoption
  of CI/CD best practices
- **XtestingCI** eases deploying anywhere plug-and-play CI/CD toolchains in a
  few commands
- **CNTT** defines conformance suites and its playbooks leveraging this 3
  softwares

**Any contribution is more than welcome!
[[1]](https://www.linkedin.com/pulse/call-functest-cntt-rc1-contributions-c%25C3%25A9dric-ollivier/)
[[2]](https://www.linkedin.com/pulse/call-functest-cntt-rc2-contributions-c%25C3%25A9dric-ollivier/)**



## CNTT/OPNFV in Orange


### A couple of RFP requirements

- the **full** CNTT reference conformance for OpenStack results and outputs
  (Orange CNTT Field Trial is in a very good shape
  [[1]](http://testresults.opnfv.org/functest/field_trial/)
  [[2]](https://www.linkedin.com/pulse/cntt-field-trials-c%C3%A9dric-ollivier/))
- the **success** of the Functest Kubernetes test suites (now released as
  part of CNTT RC2 Baraque)
- **first** VNF test cases running in **our** continuous integration chain
  thanks to Xtesting and XtestingCI

**It's implementing Orange and CNTT targets**


### Orange CNTT RC1 Field Trial

- helped detecting a couple of issues in CNTT RC1
- integrated cinder backup and nova instance_password in Orange IaaS
- to fix 10 remaining single test failures (out 2000+ functional tests, 3 hours
  benchmarking and 3 VNFs automatically onboarded and tested)
- to enhance Functest juju_epc to pass proxies

**99,999%**


### Wish list

- to integrate **more benchmarks** in CNTT conformance (e.g. disk benchmarking)
- to switch from the current Kubernetes interoperability testing to a **true**
  CNTT conformance suite
- to build the first **VNF and CNF** conformance suites (**high priority**)

**We need your contribution helps!
[[1]](https://www.linkedin.com/pulse/call-functest-cntt-rc1-contributions-c%25C3%25A9dric-ollivier/)
[[2]](https://www.linkedin.com/pulse/call-functest-cntt-rc2-contributions-c%25C3%25A9dric-ollivier/)**



## Conclusion


### Take aways

- Orange leverages OPNFV and CNTT in RFP
- we keep contributing in both specification and implementation streams for
  the success of Network Function Virtualization
- we expect more OPNFV and CNTT contributions especially for VNF and CNF
  conformance suites, our initial CNTT target

**Try CNTT reference suites, you will love them!**



## Thank you!
