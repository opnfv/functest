# Functest 2020

[Cédric Ollivier](mailto:cedric.ollivier@orange.com)

2020/01/16



### What's new in Jerma?


### Better test case verification

- switch to Ceph in our Functest SUTs
- add Neutron features in our SUTs to improve the case verification
- test all capabilities possible (e.g. vnc_console)
- verify automatically the CNTT-related containers into additional to the
  classical ones
- harden xrally_kubernetes

**Functest SUTs are compliant to CNTT RC**


### New test cases

- tempest_horizon
- tempest_keystone
- tempest_cinder
- refstack_platform
- refstack_object
- octavia
- xrally_kubernetes


### New usage

- **support CNTT RC (API testing, API and dataplane benchmarking, VNF onboarding and testing)**
- verify ONAP WindRiver OpenLab via Functest CI in a VM ("Inception model")
- allow minimal l2-only testing via Rally

**still pushing the limit!**


### Kali (K-release)

- finish updating to Alpine 3.11 and Python 3.8
- finish KloudBuster integration (it has to be updated to Python3 first)
- add tempest-stress
- update and possibly add heat-tempest-plugin
- add cyborg-tempest-plugin? ironic-tempest-plugin ? xxx-tempest-plugin?
- add CNF into Kubernetes testing

**continuously hardening the gates and improving code quality**



## Thank you
