### Functional testing for OPNFV Kubernetes (K8s) deployments with Functest

By: [Konrad Djimeli](konraddjimeli@gmail.com) (OPNFV Functest Intern)
Mentor: [Linda Wang](mailto:wangwulin@huawei.com)



### Overview

Development or integration of tests which can be used to test the functionalities of a Kubernetes deployment, in OPNFV Functest



### Kubernetes

**Kubernetes (K8s)** is an open source container manager and
orchestrator, and can be used as a VIM to orchestrate containerized VNFs.



### K8s provides an End-to-End(e2e) testing framework.

* Build/deploy/test kubernetes clusters on various providers.
* This tests provide a mechanism to test end-to-end behavior of the system.



### K8s End-to-End (e2e)testing

* The Kubernetes e2e tests are a combination of tests which fall under various categories such as [slow] (more than five minutes), [Serial] (can not run in parallel), etc


### The k8s e2e tests includes smoke and conformance tests


**Smoke test:** Tests a running Kubernetes cluster. Validates that the cluster was deployed, is accessible, and at least satisfies minimal functional requirements. Emphasis on speed and being non-destructive over thoroughness.


**Conformance tests** : Test expected to pass on any Kubernetes cluster. It is a subset of tests necessary to demonstrate conformance grows with each release. Conformance is thus considered versioned, with backwards compatibility guarantees and are designed to be run with no cloud provider configured.


**The k8s e2e test can be accessed by running the example commands below, within the K8s source code root directory**

* Build: 
```
make WHAT=test/e2e/e2e.test
```

* Run:
```
_output/bin/e2e.test --ginkgo.skip="\[Slow\]" --ginkgo.focus=\[Conformance\]"
```



### Integration of the k8s e2e testing framework with OPNFV Functest

In order to integrate k8s e2e tests into functest, various options were considered such as:


## Option #1
* Creating a docker image with opnfv/functest-core as base image and making use the Functest’s BashFeature class functionality to run the command for the test.


## OR


## Option #2
* Creating a docker image with opnfv/functest-core as base image and creating a new class which inherits from the functest.core.testcase.TestCase class, which would contain subclasses
for various testcases to be run, which are declared in a testcases.yaml file.



### Integration of the k8s testing e2e framework with OPNFV Functest

Steps taken to integrate k8s e2e testing into Functest include:

* Creating a docker image with opnfv/functest-core as base image (replaced by xtesting)
* Building/setting up the k8s e2e testing framework and it requirements in the docker image


* Adding the K8sTesting class which inherits from xtesting.core.testcase.TestCase class. This class defines the routine for executing the various k8s testcases, ensuring required env vars are set and handles logging of test output and results.
* Creation of a testcases.yaml file required to run the test in Functest.

Source code can be found on [gerrit](https://gerrit.opnfv.org/gerrit/gitweb?p=functest-kubernetes.git;a=tree)



### Testing OPNFV k8s deployment with Functest

To test an example k8s compass deployment, we can do the following


**1.** Get and place your k8s deployment config file in a directory accessible by Functest


**2.** Create an envfile with required environment variables.

```
DEPLOY_SCENARIO=k8-nosdn-nofeature-ha
KUBE_MASTER_IP="192.16.1.210:6443"
KUBERNETES_PROVIDER=local
KUBE_MASTER_URL=https://192.16.1.210:6443
```


**3.** Run the OPNFV Functest Kubernetes image

```
sudo docker run --env-file envfile \
-v path/to/kube/config:/root/.kube/config \
opnfv/functest-kubernetes
```



### Issues Faced

* Version of k8s to be used for testing (currently v1.9.4)
* Virtual deployment using various OPNFV deployers (JOID)



### What still needs to be done

* Integrating more K8s testcases
* Make logging more reliable
* Ensure tests work well on different deployments (Compass/Joid/XCI)
* Add exhaustive documentation of tests and how they work
* Complete/update unit testing
* Optimize container
* Add documentation



*We intend to ensure Functest K8s testing, properly provides functionality testing for OPNFV Kubernetes deployments and to also make it a very reliable testing framework.*
