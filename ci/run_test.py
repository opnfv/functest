import os
import sys
import time
import argparse
import yaml
import functest.utils.openstack_utils as os_utils
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.ci.tier_builder as tb

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", dest="test", action='store',
                    help="Test case or tier (group of tests) to be executed. "
                    "It will run all the test if not specified.")
parser.add_argument("-n", "--noclean", help="Do not clean OpenStack resources"
                    " after running each test (default=false).",
                    action="store_true")
parser.add_argument("-r", "--report", help="Push results to database "
                    "(default=false).", action="store_true")
args = parser.parse_args()


with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)

REPOS_DIR = os.getenv('repos_dir')
FUNCTEST_REPO = ("%s/functest/" % REPOS_DIR)


def source_rc_file(logger):
    rc_file = os.getenv('creds')
    if not os.path.isfile(rc_file):
        logger.error("RC file %s does not exist..." % rc_file)
        sys.exit(1)
    logger.debug("Sourcing the OpenStack RC file...")
    os_utils.source_credentials(rc_file)


def check_return_value(ret, start_time, stop_time):
    status = 'FAIL'
    if ret == 0:
        status = 'PASS'

    details = {
        'timestart': start_time,
        'duration': round(stop_time - start_time, 1),
        'status': status,
    }

    return status, details


def get_repo(project):
    return functest_yaml\
        .get('general')\
        .get('directories')\
        .get('dir_repo_%s' % project)


def get_cmd(test):
    return "%s/%s" % (get_repo(test.get_name()), test.cmd)


def run(test, clean=False, report=False):
    test_name = test.get_name()
    case_name = test.get_case()
    logger = ft_logger.Logger(test_name).getLogger()
    cmd = get_cmd(test)
    if case_name == '':
        project = 'functest'
        case_name = test_name
    else:
        project = test_name
        case_name = case_name

    start_time = time.time()
    ret = ft_utils.execute_command(cmd,
                                   logger,
                                   info=True,
                                   exit_on_error=False)
    stop_time = time.time()

    status, details = eval("%s(%s, %s, %s)" %
                           (test.get_criteria(), ret, start_time, stop_time))

    ft_utils.logger_test_results(logger,
                                 project,
                                 case_name,
                                 status,
                                 details)

    if report:
        logger.debug("Report Parser Results to DB......")
        ft_utils.push_results_to_db(project,
                                    case_name,
                                    logger,
                                    start_time,
                                    stop_time,
                                    status,
                                    details)
    exit(ret)


def main():
    installer = os.getenv('INSTALLER_TYPE')
    scenario = os.getenv('DEPLOY_SCENARIO')
    logger = ft_logger.Logger('run_test').getLogger()

    file = get_repo('functest') + "/ci/testcases.yaml"
    _tiers = tb.TierBuilder(installer, scenario, file)

    clean = True
    if args.noclean:
        clean = False

    report = False
    if args.report:
        report = True

    if args.test:
        test_name = args.test
        test = _tiers.get_test(test_name)
        if test:
            source_rc_file(logger)
            run(test, clean, report)
        else:
            logger.error("Unknown test case '%s', or not supported by "
                         "the given scenario '%s' installer '%s'."
                         % (test_name, scenario, installer))
            logger.debug("Available tiers are:\n\n%s" % _tiers)

if __name__ == '__main__':
    main()
