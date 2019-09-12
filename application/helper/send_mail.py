import datetime
import json
from flask_mail import Message, Mail
from flask import current_app as app
from index import mail
from flask import render_template
from application.model.models import (TestCaseLog,User,TestCase)
from application.common.constants import (SupportedTestClass,
ExecutionStatus)
from application.model.models import TestSuite

def send_email(job_id, user_id):
    Test_Name = []
    Test_Description = []
    Test_src_table = []
    Test_target_table = []
    Test_status = []
    test_case_log_obj = TestCaseLog.query.filter_by(job_id=job_id).all()
    print(test_case_log_obj)
    test_case_log_obj_list = list() 
    for eachlog in test_case_log_obj:
        case_obj = TestCase.query.filter_by(test_case_id = eachlog.test_case_id,
        is_deleted=False).first()
        Test_Name.append(SupportedTestClass().get_test_class_name_by_id
        (case_obj.test_case_class))
        Test_Description.append(case_obj.test_case_detail.get('test_desc'))
        Test_status.append(ExecutionStatus().get_execution_status_by_id
        (case_obj.latest_execution_status))
        (src_table, dest_table), = (case_obj.test_case_detail).get('table').items()
        Test_src_table.append(src_table)
        Test_target_table.append(dest_table)
    suite_obj = TestSuite.query.filter_by(test_suite_id = case_obj.test_suite_id).first()

    render_list = {}
    render_list['Test_status'] = Test_status
    render_list['Test_Name'] = Test_Name
    render_list['Test_Description'] = Test_Description
    render_list['src_tables'] = Test_src_table
    render_list['dest_tables'] = Test_target_table

    current_time = datetime.datetime.now()
    current_time.strftime("%c")


    User_obj = User.query.filter_by(user_id = user_id).first()
    email = User_obj.email
    msg = Message('Quality Suite Result',
                sender=("Acciom", app.config.get('MAIL_USERNAME')),
                recipients=[email])
    msg.html = render_template('email.html',
    content=render_list,executed_at=str(current_time.strftime("%c")),
    zip_content=zip(Test_Name, Test_Description, Test_src_table,
                        Test_target_table, Test_status),
                        suite_name = suite_obj.test_suite_name,
                        suite_id = suite_obj.test_suite_id
    )
    mail.send(msg)


def check_complete(job_id):
    test_case_log_obj = TestCaseLog.query.filter_by(job_id=job_id).all()
    for each_case in test_case_log_obj:
            if each_case.execution_status == 0:
                return False
    return True



