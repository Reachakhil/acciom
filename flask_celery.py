from application.common.constants import (ExecutionStatus, SupportedTestClass)
from application.helper.runnerclass import run_by_case_id
from application.model.models import (TestCase, TestCaseLog)
from application.helper.send_mail import send_email,check_complete
from index import celery
from celery.result import AsyncResult
import time

@celery.task(name='run_by_case_id_dv', queue="Dv_Q")
def run_by_case_id_dv(case_log_id, test_case_id, user_id):
    run_by_case_id(case_log_id, test_case_id, user_id)


@celery.task(name='run_by_case_id_other', queue="other_Q")
def run_by_case_id_other(case_log_id, test_case_id, user_id):
    run_by_case_id(case_log_id, test_case_id, user_id)
    return "others"

@celery.task(name='check_job_status', queue="job_status_Q")
def check_job_status(job_id,user_id,celery_task_list):
    # for task in celery_task_list:
    #     res = AsyncResult(id=task)
    #     if res.state == 'SUCCESS':
    #         celery_task_list.remove(task)
    # if celery_task_list:
    #     check_job_status.apply_async((job_id,user_id,celery_task_list),
    #     countdown=5)
    # else:
    #     completed = check_complete(job_id)
    #     completed= True
    #     if completed:
    #         send_email(job_id, user_id)
    #     else:
    #         check_job_status.delay((job_id,user_id,celery_task_list), 
    #         countdown=5) 
    # return True

    #########################################
    while celery_task_list:
        for task in celery_task_list:
            res = AsyncResult(id = task)
            if res.state == 'SUCCESS':
                celery_task_list.remove(task)
        time.sleep(2)
    check_complete(job_id)
    while not check_complete(job_id):
        time.sleep(5)
    send_email(job_id, user_id)
    return True
        



@celery.task(name='job_submit', queue="master_Q")
def job_submit(job_id, user_id, send_email):
    """
    Method will submit each case associated with the job id in the celery queue
    parralely.
    Args:
        job_id (Int): Job id of the job passed
        user_id (int): User id associated with the executor

    Returns: Status of the jobs

    """
    celery_task_list= list()
    execution_status_new = ExecutionStatus().get_execution_status_id_by_name(
        'new')
    test_case_log_obj = TestCaseLog.query.filter_by(job_id=job_id).all()
    for each_case in test_case_log_obj:
        case_obj = each_case.test_case_id
        case = TestCase.query.filter_by(test_case_id=case_obj).first()
        if (each_case.execution_status == execution_status_new) and (
                case.test_case_class == SupportedTestClass().get_test_class_id_by_name(
            'datavalidation')):
            celery_task = run_by_case_id_dv.delay(each_case.test_case_log_id,
                                    each_case.test_case_id,
                                    user_id)
        else:
            celery_task = run_by_case_id_other.delay(each_case.test_case_log_id,
                                    each_case.test_case_id,
                                    user_id)
        celery_task_list.append(celery_task.task_id)
    if send_email == True:
        check_job_status.apply_async((job_id,user_id,celery_task_list), countdown=2)
