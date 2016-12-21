import time

import testcase_base as base
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_logger as ft_logger


class FeatureBase(base.TestcaseBase):
    def __init__(self, project='functest', case='', repo='', cmd=''):
        super(FeatureBase, self).__init__()
        self.project_name = project
        self.case_name = case
        self.cmd = cmd
        self.repo = self.get_conf('general.dir.{}'.format(repo))
        self.result_file = self.get_result_file()
        self.logger = ft_logger.Logger(project).getLogger()

    def run(self, **kwargs):
        self.prepare()
        self.start_time = time.time()
        ret = ft_utils.execute_command(self.cmd, output_file=self.result_file)
        self.stop_time = time.time()
        self.post()
        self.parse_results(ret)
        self.log_results()
        return base.TestcaseBase.EX_OK

    def prepare(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    def parse_results(self, ret):
        exit_code = base.TestcaseBase.EX_OK
        if ret == 0:
            self.logger.info("{} OK".format(self.project_name))
            self.criteria = 'PASS'
        else:
            self.logger.info("{} FAILED".format(self.project_name))
            exit_code = base.TestcaseBase.EX_RUN_ERROR
            self.criteria = "FAIL"

        return exit_code

    def get_result_file(self):
        dir = self.get_conf('general.dir.results')
        return "{}/{}.log".format(dir, self.project_name)

    def log_results(self):
        ft_utils.logger_test_results(self.project_name,
                                     self.case_name,
                                     self.criteria,
                                     self.details)

    @staticmethod
    def get_conf(parameter):
        return ft_utils.get_functest_config(parameter)
