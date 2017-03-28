import time

import testcase as base
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_logger as ft_logger
from functest.utils.constants import CONST


class FeatureBase(base.TestCase):

    def __init__(self, project='functest', case='', repo='', cmd=''):
        super(FeatureBase, self).__init__()
        self.project_name = project
        self.case_name = case
        self.cmd = cmd
        self.real_time_output = False
        self.repo = CONST.__getattribute__(repo)
        self.result_file = self.get_result_file()
        self.logger = ft_logger.Logger(project).getLogger()

    def run(self, **kwargs):
        self.prepare()
        self.start_time = time.time()

        ret = self.execute()
        if self.real_time_output:
            for line in self.tailf_results_file():
                print line

        self.stop_time = time.time()
        self.post()
        self.parse_results(ret)
        self.log_results()
        self.logger.info("Test result is stored in '%s'" % self.result_file)
        return base.TestCase.EX_OK

    def execute(self):
        '''
        Executer method that can be overwritten
        By default it executes a shell command.
        '''
        return ft_utils.execute_command(self.cmd, output_file=self.result_file)

    def tailf_results_file(self):
        with open(self.result_file) as f:
            for line in f:
                yield line

    def prepare(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    def parse_results(self, ret):
        exit_code = base.TestCase.EX_OK
        if ret == 0:
            self.logger.info("{} OK".format(self.project_name))
            self.criteria = 'PASS'
        else:
            self.logger.info("{} FAILED".format(self.project_name))
            exit_code = base.TestCase.EX_RUN_ERROR
            self.criteria = "FAIL"

        return exit_code

    def get_result_file(self):
        return "{}/{}.log".format(CONST.dir_results, self.project_name)

    def log_results(self):
        ft_utils.logger_test_results(self.project_name,
                                     self.case_name,
                                     self.criteria,
                                     self.details)
