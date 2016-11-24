import time

import TestCasesBase
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_logger as ft_logger


class FeatureBase(TestCasesBase.TestCasesBase):
    def __init__(self, project='functest', case='', repo='', cmd=''):
        super(FeatureBase, self).__init__()
        self.project_name = project
        self.case_name = case
        self.cmd = cmd
        self.repo = self.get_conf('general.directories.{}'.format(repo))
        self.result_file = self.get_result_file()
        self.logger = ft_logger.Logger(project).getLogger()

    def run(self, **kwargs):
        self.prepare()
        self.start_time = time.time()
        ret = ft_utils.execute_command(self.cmd, output_file=self.result_file)
        self.stop_time = time.time()
        self.post()
        exit_code = self.parse_results(ret)
        self.log_results()
        return exit_code

    def prepare(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    def parse_results(self, ret):
        exit_code = TestCasesBase.TestCasesBase.EX_OK
        duration = round(self.stop_time - self.start_time, 1)
        if ret == 0 and duration > 1:
            self.logger.info("{} OK".format(self.project_name))
            self.criteria = 'PASS'
        elif ret == 0 and duration <= 1:
            self.logger.info("{} SKIPPED".format(self.project_name))
            exit_code = TestCasesBase.TestCasesBase.EX_SKIP
        else:
            self.logger.info("{} FAILED".format(self.project_name))
            exit_code = TestCasesBase.TestCasesBase.EX_TEST_FAIL
            self.criteria = "FAIL"

        return exit_code

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
