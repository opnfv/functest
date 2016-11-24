import time

import TestCasesBase
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_logger as ft_logger


class Umbrella(TestCasesBase.TestCasesBase):
    def __init__(self, project='functest', case='', repo='', cmd=''):
        super(Umbrella, self).__init__()
        self.project_name = project
        self.case_name = case
        self.repo = self.get_conf('general.directories.{}'.format(repo))
        self.cmd = cmd
        self.result_file = self.get_result_file()
        self.logger = ft_logger.Logger(project).getLogger()

    def run(self, **kwargs):
        self.start_time = time.time()
        ret = ft_utils.execute_command(self.cmd, output_file=self.result_file)
        self.stop_time = time.time()
        self.parse_results(ret)
        self.log_results()

        if ret == 0:
            return TestCasesBase.TestCasesBase.EX_OK
        else:
            return TestCasesBase.TestCasesBase.EX_RUN_ERROR

    def parse_results(self, ret):
        def get_criteria_value():
            criteria = ft_utils.get_criteria_by_test(self.project_name)
            return criteria.split('==')[1].strip()

        self.criteria = 'FAIL'
        if str(ret) == get_criteria_value():
            self.criteria = 'PASS'

        self.details = {
            'timestart': self.start_time,
            'duration': round(self.stop_time - self.start_time, 1),
            'status': self.criteria,
        }

    def get_result_file(self):
        dir = self.get_conf('general.directories.dir_results')
        return "{}/{}.log".format(dir, self.project_name)

    def log_results(self):
        ft_utils.logger_test_results(self.project_name,
                                     self.case_name,
                                     self.criteria,
                                     self.details)

    @staticmethod
    def get_conf(parameter):
        return ft_utils.get_functest_config(parameter)
