from application.common.constants import ExecutionStatus
from application.helper.runnerclass import (save_job_status, save_case_log)
from application.model.models import TestCase
from flask_celery import job_submit


def create_job(user_id, suite_obj, is_external, case_id_list=None):
    """
    Method will create a job , submit the job for the given id.
    Args:
        user_id (Int): User id of the executor
        suite_obj (Obj): suite id of the test suite passed
        is_external (bool): boolean value
        case_id_list (List): list of all the cases

    Returns: submit the job through celery ,and returns its status

    """
    execution_status_new = ExecutionStatus().get_execution_status_id_by_name(
        'new')
    if not case_id_list:
        send_mail=True
        case_id_list = [case.test_case_id for case in suite_obj.test_case]
    else:
        send_mail=False
    job, job_id = save_job_status(suite_obj.test_suite_id, user_id,
                                is_external)
    for each_case in case_id_list:
        case_obj = TestCase.query.filter_by(test_case_id=each_case).first()
        save_case_log(case_obj.test_case_id, execution_status_new, job_id)
    job_submit.delay(job_id, user_id, send_mail)  # submit the job
    return True
