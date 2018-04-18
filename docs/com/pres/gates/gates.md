# Functest Gates

[Cédric Ollivier](mailto:cedric.ollivier@orange.com)

2018/04/19



### Why gating?

- maintain an overall high quality whatever the skills involved in our
open community
- detect the errors as soon as possible (before merge operations)
- verify automatically most of Functest milestones


### Today's Verify -1

- one error is detected by yamllint, pylint or doc8
- one unit test is failing (py27 and py35)
- our Framework is not fully covered
- specific modules are not rated 10/10 by pylint
- unix permissions are wrong
- one doc cannot be generated without warning

Please see [tox.ini](https://git.opnfv.org/functest/tree/tox.ini) for details


### Gambia's Verify -1

- enforce an overall 10/10 by pylint
- check the full coverage of all third-party interfaces
- integrate other linters like ShellScript (if they fit tox basics)

Please see
[Gambia Challenges](http://testresults.opnfv.org/functest/gambiachallenges/)
for details


### Great! But

- the current gate checks all coding rules, our Framework and all interfaces
to third-parties but **not the testcases**
- it doesn't break **the circular dependencies** between Installers and
Functest (Installers asks for a trustable Healthcheck but we need installer
runs to get its results)

Our testcases have still **to be verified by hand** what differs from
OpenStack Workflow



### functional gating

- we need to run all Functest patches before merge against reference
plateforms (OpenStack and Kubernetes)
- a voting job must forbid the merge if one test is failed (as the workflow
process implemented by OpenStack)


### reference platform

- it could be baremetal or virtual if all testcases (including all VNFs) can
be tested successfully
- any installer could be selected as long as the right target VIM version is
proposed at the beginning of the release:
  - devstack (OpenStack gates)
  - kolla-ansible (Orange ONAP OpenLab)
  - XCI
  - APEX


### Verify +2

- only the functional check will end after hours (and only after the patchset
is accepted by core reviewers). each patchset will be verified in ~10 minutes.
- **most Functest milestones will be met by design** which generates more
benefits that the duration before merge
- we are currently waiting for days/weeks for relevant results



## Thank you!
