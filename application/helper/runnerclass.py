from application.common.constants import ExecutionStatus, SupportedTestClass, \
    TestClass
from application.common.dqi_calculation import calculate_dqi
from application.helper.runnerclasshelpers import (TestCaseExecution)
from application.model.models import (TestCaseLog, TestCase, Job)
from flask_celery import make_celery
from index import app

celery = make_celery(app)


def save_test_status(test_case_id, status):
    """
    This will save TestCase status to the table
    Args:
        test_case_id: test_case_id of the case
        status: latest_execution_status of the case

    Returns: Save status of the case to db.

    """
    test_case_id.latest_execution_status = status
    test_case_id.save_to_db()
    return True


def save_job_status(test_suite_id, user_id, is_external=False):
    job = Job(test_suite_id=test_suite_id, owner_id=user_id,
              is_external_trigger=is_external)
    job.save_to_db()
    return job, job.job_id
    # return job_id


def save_case_log(test_case_id, execution_status,
                  job_id):
    """

    Args:
        test_case_id: test_case_id associated with log
        user_id: user_id associated with log
        execution_log: execution_log
        execution_status: execution_status of the log

    Returns:

    """
    temp_log = TestCaseLog(test_case_id=test_case_id,
                           job_id=job_id,
                           execution_status=execution_status)
    temp_log.execution_log = None
    temp_log.save_to_db()
    return temp_log


@celery.task(name='runnerclass.run_by_case_id_dv', queue="Dv_Q")
def run_by_case_id_dv(case_log_id, test_case_id, user_id):
    run_by_case_id(case_log_id, test_case_id, user_id)


@celery.task(name='run_by_case_id_other', queue="other_Q")
def run_by_case_id_other(case_log_id, test_case_id, user_id):
    run_by_case_id(case_log_id, test_case_id, user_id)
    return "others"


def run_by_case_id(case_log_id, test_case_id, user_id):
    """
    This runs the case based on its test_case_id
       Args:
           test_case_id: test_case_id of the test case provided

       Returns: Executes the case, and returns result.

       """
    case_log = TestCaseLog.query.filter_by(
        test_case_log_id=case_log_id).first()
    test_case = TestCase.query.filter_by(test_case_id=test_case_id).first()
    test_suite_id = test_case.test_suite_id
    res = run_test(case_log, test_case)
    return {"status": True, "result": res}


def run_test(case_log, case_id):
    inprogress = ExecutionStatus().get_execution_status_id_by_name(
        'inprogress')
    save_test_status(case_id, inprogress)  # case_id saved
    case_log.execution_status = inprogress
    case_log.save_to_db()
    src_db_id = case_id.test_case_detail['src_db_id']
    target_db_id = case_id.test_case_detail['target_db_id']
    test_case_detail = case_id.test_case_detail

    if case_id.latest_execution_status == ExecutionStatus().get_execution_status_id_by_name(
            'inprogress'):  # can be removed
        if case_id.test_case_class == SupportedTestClass(). \
                get_test_class_id_by_name(TestClass.COUNT_CHECK):
            result = TestCaseExecution.count_check(src_db_id, target_db_id,
                                                   test_case_detail)

        if case_id.test_case_class == SupportedTestClass(). \
                get_test_class_id_by_name(TestClass.NULL_CHECK):
            result = TestCaseExecution.null_check(src_db_id, target_db_id,
                                                  test_case_detail)

        if case_id.test_case_class == SupportedTestClass(). \
                get_test_class_id_by_name(TestClass.DUPLICATE_CHECK):
            result = TestCaseExecution.duplicate_check(src_db_id, target_db_id,
                                                       test_case_detail)

        if case_id.test_case_class == SupportedTestClass(). \
                get_test_class_id_by_name(TestClass.DDL_CHECK):
            result = TestCaseExecution.ddlcheck(src_db_id, target_db_id,
                                                test_case_detail)
        if case_id.test_case_class == SupportedTestClass(). \
                get_test_class_id_by_name(TestClass.DATA_VALIDATION):
            result = {'res': ExecutionStatus().get_execution_status_id_by_name(
                'inprogress'), "Execution_log": None}

        if result['res'] == ExecutionStatus().get_execution_status_id_by_name(
                'pass'):
            pass_status = ExecutionStatus().get_execution_status_id_by_name(
                'pass')
            save_test_status(case_id, pass_status)
            case_log.execution_status = pass_status
            data = result['Execution_log']
            case_log.execution_log = data
            case_log.dqi_percentage = 100
            case_log.save_to_db()

        elif result[
            'res'] == ExecutionStatus().get_execution_status_id_by_name(
            'fail'):
            fail = ExecutionStatus().get_execution_status_id_by_name('fail')
            save_test_status(case_id, fail)
            case_log.execution_status = fail
            data = result['Execution_log']
            case_log.execution_log = data
            dqi = calculate_dqi(data, case_log.test_case_id)
            case_log.dqi_percentage = dqi
            case_log.save_to_db()

        elif result[
            'res'] == ExecutionStatus().get_execution_status_id_by_name(
            'error'):
            error = ExecutionStatus().get_execution_status_id_by_name('error')
            save_test_status(case_id, error)
            case_log.execution_status = error
            case_log.execution_log = result['Execution_log']
            case_log.dqi_percentage = 0
            case_log.save_to_db()

        elif result[
            'res'] == ExecutionStatus().get_execution_status_id_by_name(
            'inprogress'):
            save_test_status(case_id, inprogress)
            case_log.execution_status = inprogress
            case_log.save_to_db()
            if case_id.test_case_class == SupportedTestClass(). \
                    get_test_class_id_by_name(TestClass.DATA_VALIDATION):
                result = TestCaseExecution.data_validation(src_db_id,
                                                           target_db_id,
                                                           test_case_detail,
                                                           case_log)
    return {"status": True}


def save_case_log_information(case_log, case_log_execution_status,
                              source_count, src_to_dest, src_log,
                              dest_count, dest_to_src, dest_log, test_case_id):
    """
    Save log information from spark to the TestCaseLog Table
    Args:
        case_log: caselog object
        source_count: source table count
        src_to_dest: source and target table diffrence
        src_log: source log
        dest_count: target table count
        dest_to_src: target and source table diffrence
        dest_log: target table log

    Returns: Submit the log to the TestCaseLog Table

    """
    case_log.execution_status = case_log_execution_status
    if src_log == '[]':
        src_log = None
    elif dest_log == '[]':
        dest_log = None
    spark_job_data = {"source_execution_log": src_log,
                      "dest_execution_log": dest_log,
                      "src_count": source_count,
                      "src_to_dest_count": src_to_dest,
                      "dest_count": dest_count,
                      "dest_to_src_count": dest_to_src}
    case_log.execution_log = spark_job_data
    dqi = calculate_dqi(spark_job_data, test_case_id)
    case_log.dqi_percentage = dqi
    case_log.save_to_db()
