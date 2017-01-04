import yaml

from functest.utils.constants import CONST
import functest.utils.functest_logger as ft_logger


class TestCasesConfig(object):
    def __init__(self):
        self.logger = ft_logger.Logger("testcase.py").getLogger()
        if not hasattr(CONST, 'functest_testcases_yaml'):
            raise Exception('testcases.yaml not configed')
        self.testcases_config = CONST.functest_testcases_yaml
        try:
            with open(self.testcases_config) as f:
                self.testcases_yaml = yaml.safe_load(f)
        except:
            raise Exception('Parse {} failed'.format(self.testcases_config))

    def get_dict_by_test(self, testname):
        for dic_tier in self.testcases_yaml.get("tiers"):
            for dic_testcase in dic_tier['testcases']:
                if dic_testcase['name'] == testname:
                    return dic_testcase
    
        self.logger.error('Project %s is not defined in testcases.yaml' % testname)
        return None

    def get_criteria_by_test(self, testname):
        dict = self.get_dict_by_test(testname)
        if dict:
            return dict['criteria']
        return None

    def check_success_rate(self, case_name, success_rate):
        def get_criteria_value(op):
            return float(criteria.split(op)[1].rstrip('%'))
    
        success_rate = float(success_rate)
        criteria = self.get_criteria_by_test(case_name)
    
        status = 'FAIL'
        ops = ['==', '>=']
        for op in ops:
            if op in criteria:
                c_value = get_criteria_value(op)
                if eval("%s %s %s" % (success_rate, op, c_value)):
                    status = 'PASS'
                break
    
        return status


TCC = TestCasesConfig()
