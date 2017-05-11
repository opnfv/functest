# Functest Framework

created by [Cédric Ollivier](mailto:cedric.ollivier@orange.com)

2017/05/06

Note:

- Functest integrates lots of heteregeounous testcases:
    - python vs bash
    - internal vs external
- it aims to benefit from object programming
    - to define common operations
    - to avoid conditional instructions regarding the testcases
    - to avoid duplicating code
    - to ease the integration of third-party testcases (written in Bash or Python)



## Quick overview


### Functest function calls

- **CI** calls *run_tests.py* (please see [jenkins jobs](https://gerrit.opnfv.org/gerrit/gitweb?p=releng.git;a=tree;f=jjb/functest))
- *run_tests.py* parses *functest/ci/testcases.yaml* to:
    - check which testcase(s) must be run
    - execute the common operations on every testcase (run, push its results to db...)
<!-- .element: class="fragment highlight-red"-->
    - return the right status code to **CI**


### Our target

- limit run_tests.py instructions by defining:
    - the basic testcase attritutes
    - all common operations
    - the status codes expected
- avoid duplicating codes between testcases
- ease the developpement of third-party testcases (aka features)



## class TestCase

base model for single test case


### instance attributes

- project_name (default: 'functest')
- case_name
- criteria
- result
- start_time
- stop_time
- details


### methods

| Method            | Purpose                                    |
|-------------------|--------------------------------------------|
| run(**kwargs)     | run the test case                          |
| is_successful()   | interpret the results of the test case     |
| get_duration()    | return the duration of the test case       |
| push_to_db()      | push the results of the test case to the DB|


### run(**kwargs)

- the subclasses must override the default implementation which is false on purpose
- the new implementation must set the following attributes to push the results to DB:
    - result
    - start_time
    - stop_time


### class attributes

| Status code        | Returned when       |
|--------------------|---------------------|
| EX_OK              | everything is OK    |
| EX_RUN_ERROR       | run() failed        |
| EX_TESTCASE_FAILED | results are false   |
| EX_PUSH_TO_DB_ERROR| push_to_db() failed |


### run_tests.py

```python
module = importlib.import_module(run_dict['module'])
cls = getattr(module, run_dict['class'])
test_dict = ft_utils.get_dict_by_test(test_name)
test_case = cls(**test_dict)
try:
    kwargs = run_dict['args']
    result = test_case.run(**kwargs)
except KeyError:
    result = test_case.run()
if result == testcase.TestCase.EX_OK:
    if GlobalVariables.REPORT_FLAG:
        test_case.push_to_db()
    result = test_case.is_successful()
```



## Your first test case


### first.py

```python
#!/usr/bin/env python

import time

from functest.core import testcase

class Test(testcase.TestCase):

    def run(self, **kwargs):
        self.start_time = time.time()
        print "Hello World"
        self.result = 100
        self.stop_time = time.time()
        return testcase.TestCase.EX_OK
```


### functest/ci/testcases.yaml

```yaml
case_name: first
project_name: functest
criteria: 100
blocking: true
clean_flag: false
description: ''
dependencies:
    installer: ''
    scenario: ''
run:
    module: 'first'
    class: 'Test'
```



## class Feature
bases: TestCase

base model for single feature


### methods

| Method            | Purpose                   |
|-------------------|---------------------------|
| run(**kwargs)     | run the feature           |
| execute(**kwargs) | execute the Python method |


### run(**kwargs)

- allows executing any Python method by calling execute()
- sets the following attributes required to push the results to DB:
    - result
    - start_time
    - stop_time
- doesn't fulfill details when pushing the results to the DB.


### execute(**kwargs)

- the subclasses must override the default implementation which is false on purpose
- the new implementation must return 0 if success or anything else if failure.



## Your second test case


### second.py

```python
#!/usr/bin/env python

from functest.core import feature

class Test(feature.Feature):

    def execute(self, **kwargs):
        print "Hello World"
        return 0
```


### functest/ci/testcases.yaml

```yaml
case_name: second
project_name: functest
criteria: 100
blocking: true
clean_flag: false
description: ''
dependencies:
    installer: ''
    scenario: ''
run:
    module: 'second'
    class: 'Test'
```



## class BashFeature
bases: Feature

class designed to run any bash command


### execute(**kwargs)

execute the cmd passed as arg.



## Your third test case


### functest/ci/testcases.yaml

```
case_name: third
project_name: functest
criteria: 100
blocking: true
clean_flag: false
description: ''
dependencies:
    installer: ''
    scenario: ''
run:
    module: 'functest.core.feature'
    class: 'BashFeature'
    args:
        cmd: 'echo Hello World; exit 0'
```



## Euphrates


### Next actions

- __to finish VNF abstraction (coverage + pylint)__
- to publish doc API
- to manage criteria as written in testcases.yaml

Please see [Functest Euphrates page](https://wiki.opnfv.org/display/functest/Functest+Euphrates+page) for more details



## Thank You!
