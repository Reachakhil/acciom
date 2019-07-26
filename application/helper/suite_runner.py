import datetime
import json
import time

from flask import render_template
from flask_mail import Message, Mail

from application.common.constants import ExecutionStatus
from application.model.models import TestSuite, TestCaseLog
from index import app
from index import db

mail = Mail(app)


# app.config('EMAIL_ON_SUITE_EXECUTION', True)
# app.config('PARALLEL_SUITE_EXECUTION', True)


def check_status(case_log_id_list):
    """
    Args:
        case_log_id_list (int):

    Returns:

    """
    if not start_test(case_log_id_list):
        return False
    else:
        return True


def start_test(case_log_id_list):
    for each_log in case_log_id_list:
        # db.session.commit()
        testcase_log_id = TestCaseLog.query.filter_by(
            test_case_log_id=each_log).first()
        if testcase_log_id.execution_status == ExecutionStatus(). \
                get_execution_status_id_by_name("inprogress"):
            return False
            break
    return True


def suite_level_send_mail(case_log_id_list, email, suite_id):
    time.sleep(10)
    Test_Name = []
    Test_Description = []
    Test_src_table = []
    Test_target_table = []
    Test_status = []
    while not check_status(case_log_id_list):
        db.session.commit()
        time.sleep(10)
    suite = TestSuite.query.filter_by(test_suite_id=suite_id).first()
    for each_test in suite.test_case:
        print(each_test)
        Test_Name.append(each_test.test_case_id)
        Test_Description.append(each_test.test_id)
        Test_status.append(each_test.latest_execution_status)
        (src_table, dest_table), = json.loads(each_test.test_case_detail)[
            'table'].items()
        Test_src_table.append(src_table)
        Test_target_table.append(dest_table)
    print(Test_status, Test_Name, Test_Description, Test_src_table,
          Test_target_table)
    render_list = {}
    render_list['Test_status'] = Test_status
    render_list['Test_Name'] = Test_Name
    render_list['Test_Description'] = Test_Description
    render_list['src_tables'] = Test_src_table
    render_list['dest_tables'] = Test_target_table
    payload = {"status": True, "message": "send Mail"}
    msg = Message('Quality Suite Result',
                  sender=("Acciom", app.config.get('MAIL_USERNAME')),
                  recipients=[email])
    current_time = datetime.datetime.now()
    current_time.strftime("%c")
    with app.app_context():
        msg.html = render_template(
            'email.html', content=render_list,
            zip_content=zip(Test_Name, Test_Description, Test_src_table,
                            Test_target_table, Test_status),
            suite_name=suite.test_suite_name, suite_id=suite.test_suite_id,
            executed_at=str(current_time.strftime("%c")))
        mail.send(msg)
