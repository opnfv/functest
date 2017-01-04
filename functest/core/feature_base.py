import time

import testcase_base as base
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_logger as ft_logger
from functest.utils.constants import CONST


class FeatureBase(base.TestcaseBase):
    def __init__(self, project='functest', case='', repo='', cmd=''):
        super(FeatureBase, self).__init__()
        self.project_name = project
        self.case_name = case
        self.cmd = cmd
        self.repo = CONST.__getattribute__(repo)
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
        return "{}/{}.log".format(CONST.dir_results, self.project_name)

    def log_results(self):
        pod_name = CONST.POD_NAME
        scenario = CONST.DEPLOY_SCENARIO
        version = CONST.VERSION
        build_tag = CONST.BUILD_TAG

        self.logger.info(
            "\n"
            "****************************************\n"
            "\t %(p)s/%(n)s results \n\n"
            "****************************************\n"
            "DB:\t%(db)s\n"
            "pod:\t%(pod)s\n"
            "version:\t%(v)s\n"
            "scenario:\t%(s)s\n"
            "status:\t%(c)s\n"
            "build tag:\t%(b)s\n"
            "details:\t%(d)s\n"
            % {'p': self.project_name,
                'n': self.case_name,
                'db': CONST.results_test_db_url,
                'pod': pod_name,
                'v': version,
                's': scenario,
                'c': self.criteria,
                'b': build_tag,
                'd': self.details})
