from application.common.constants import ExecutionStatus
from application.helper.runnerclass import run_by_case_id
from application.helper.runnerclass import save_job_status, save_case_log
from application.model.models import TestSuite, TestCase, TestCaseLog


def run_by_suite_id(current_user, suite_id, is_external=False):
    """
    Method will run suite by Id

    Args:
        current_user(Object): user object
        suite_id(int): suite_id of the suite.

    Returns: Runs each job in the test suite

    """
    test_suite = TestSuite.query.filter_by(
        test_suite_id=suite_id).first()
    for each_test in test_suite.test_case:
        run_by_case_id(each_test.test_case_id, current_user, is_external)
    return True


def run_by_case_id_list(current_user, case_id_list, is_external=False):
    """
    Method to execute the test case from the list of test_cases
     provided in the list
    Args:
        current_user (int): current user id
        case_id_list (list): list of case_id objects
        is_external (boolean): determine weather job run from
        system or external

    Returns: executes the job and returns the status

    """
    for each_test in case_id_list:
        run_by_case_id(each_test, current_user, is_external)
    return True


def execute_external_job(user_id, case_id_list):
    is_external = True
    case_list = case_id_list
    case_obj = TestCase.query.filter_by(
        test_case_id=case_list[0]).first()
    test_suite_obj = TestSuite.query.filter_by(
        test_suite_id=case_obj.test_suite_id).first()
    case_id_list = [case_id.test_case_id for case_id in
                    test_suite_obj.test_case]
    print(case_id_list)

    for each_case in case_list:
        if each_case not in case_id_list:
            return False
    run_by_case_id_list(user_id,
                        case_id_list,
                        is_external)

    return True


def create_job(user_id, suite_id, case_id_list=[]):
    execution_status_new = ExecutionStatus().get_execution_status_id_by_name(
        'new')
    is_external = False
    if not case_id_list:
        case_id_list = [suite for suite in suite_id.test_case]
    job, job_id = save_job_status(suite_id, user_id, is_external)

    for each_case in case_id_list:
        case_log = save_case_log(each_case.test_case_id, execution_status_new,
                                 job_id)
        run_case(job_id)


def run_case(job_id):
    execution_status_new = ExecutionStatus().get_execution_status_id_by_name(
        'new')
    test_case_log_obj = TestCaseLog.query.filter_by(job_id=job_id).all()
    for each_case in test_case_log_obj:
        if each_case.execution_status == execution_status_new:
            run_by_case_id()
