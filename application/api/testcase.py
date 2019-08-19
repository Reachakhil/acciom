import ast
from flask import current_app as app
from flask import json
from flask import request
from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from application.common.constants import (APIMessages, ExecutionStatus,
                                          SupportedTestClass, SupportedDBType)
from application.common.response import (STATUS_CREATED, STATUS_SERVER_ERROR,
                                         STATUS_BAD_REQUEST)
from application.common.response import api_response
from application.common.runbysuiteid import create_job
from application.common.token import (token_required)
from application.common.utils import (get_table_name,
                                      db_details_without_password)
from application.helper.corefunctions.datavalidation import manage_none_value
from application.helper.runnerclass import (run_by_case_id,
                                            save_case_log_information)
from application.helper.runnerclass import (save_case_log_information)
from application.helper.runnerclasshelpers import (
    save_case_log)
from application.model.models import (TestCaseLog, TestCase, DbConnection,
                                      PersonalToken, TestSuite)
from index import app
from index import db


class TestCaseJob(Resource):
    """
    TestCaseJob Executes either particular suite or a case, based on the either
    test_case_id or suite_id and
    """

    @token_required
    def post(self, session):
        """
        Executes either particular suite or a case either by suite_id
        or case_id, returns Success reponse on Execution or error log
        in case of a error

        Args:
            session(Object): session gives user ID of the owner
            who is execution the job

        Returns: Return api response ,either successful job run or error.
        """
        # try:
        user_id = session.user_id
        parser = reqparse.RequestParser()
        parser.add_argument('suite_id', type=int, required=False,
                            help=APIMessages.PARSER_MESSAGE)
        parser.add_argument('case_id_list',
                            type=list, location="json",
                            help=APIMessages.PARSER_MESSAGE)
        execution_data = parser.parse_args()
        is_external = False
        if execution_data['suite_id']:
            test_suite_obj = TestSuite.query.filter_by(
                test_suite_id=int(execution_data['suite_id'])).first()
            if not test_suite_obj:
                return api_response(False, APIMessages.SUITE_NOT_EXIST,
                                    STATUS_SERVER_ERROR)
            # Create a Job
            create_job(user_id, test_suite_obj, is_external)
            return api_response(True, APIMessages.RETURN_SUCCESS,
                                STATUS_CREATED)

        elif execution_data['case_id_list']:
            test_case_obj = TestCase.query.filter_by(
                test_case_id=execution_data['case_id_list'][0]).first()
            if not test_case_obj:
                return api_response(False,
                                    APIMessages.TEST_CASE_NOT_IN_DB,
                                    STATUS_SERVER_ERROR)
            test_suite_id = test_case_obj.test_suite_id
            test_suite_obj = TestSuite.query.filter_by(
                test_suite_id=test_suite_id).first()
            # Create a Job
            create_job(user_id, test_suite_obj, is_external,
                       execution_data['case_id_list'])
            return api_response(True, APIMessages.RETURN_SUCCESS,
                                STATUS_CREATED
                                )
        else:
            return api_response(False, APIMessages.INTERNAL_ERROR,
                                STATUS_SERVER_ERROR)

        # except Exception as e:
        #     app.logger.error(e)
        #     return api_response(False, APIMessages.INTERNAL_ERROR,
        #                         STATUS_SERVER_ERROR)


with app.app_context():
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
            'code': 'akhil'
        })
        response.content_type = "application/json"
        return response


class TestCaseSparkJob(Resource):
    """
    TestCaseSparkJob class Store log generated from sparkJob , it will reflect
    test_case ,testcaselog table
    """

    def post(self, test_case_log_id):
        """
        Accepts result from spark execution and stores result in table

        Args:
            test_case_log_id (Int): test_case_log_id of the job being executed

        Returns: Stores result in the db given by the spark job.
        """
        case_log = TestCaseLog.query.filter_by(
            test_case_log_id=test_case_log_id).first()
        case = TestCase.query.filter_by(
            test_case_id=case_log.test_case_id).first()

        spark_log_dict = request.data.decode('utf-8', 'ignore')
        parsed_log = ast.literal_eval(spark_log_dict)

        if parsed_log['result'] == 'error':
            case_log.error_log = parsed_log['exception']
            case_log.execution_status = ExecutionStatus(). \
                get_execution_status_id_by_name('error')
            case_log.save_to_db()
            case_test_status = case_log.execution_status = ExecutionStatus(). \
                get_execution_status_id_by_name('error')
            save_case_log(case_log, case_test_status)

        else:
            result_src = parsed_log['result']['src_to_dest']
            for x in range(0, len(result_src)):
                result_src[x] = ast.literal_eval(result_src[x])
            src_processed_data = manage_none_value(result_src, parsed_log
            ['result']['src_columns_name'])

            result_des = parsed_log['result']['dest_to_src']
            for x in range(0, len(result_des)):
                result_des[x] = ast.literal_eval(result_des[x])
            dest_processed_data = manage_none_value(result_des, parsed_log
            ['result']['dest_columns_name'])

            src_count = parsed_log['src_result_count']
            target_count = parsed_log["target_result_count"]
            result_count = parsed_log['result_count']

            if result_count == 0:
                case_log_execution_status = ExecutionStatus(). \
                    get_execution_status_id_by_name('pass')
                save_case_log_information(case_log, case_log_execution_status,
                                          parsed_log['src_count'][0],
                                          (src_count), None,
                                          parsed_log['dest_count'][0],
                                          (target_count), None,
                                          case_log.test_case_id)
                save_case_log(case_log, case_log_execution_status)
                # save_job_status(case_log, case_log_execution_status)

            elif result_count != 0:
                case_log_execution_status = ExecutionStatus(). \
                    get_execution_status_id_by_name('fail')
                save_case_log_information(case_log, case_log_execution_status,
                                          parsed_log['src_count'][0],
                                          src_count, src_processed_data,
                                          parsed_log['dest_count'][0],
                                          target_count,
                                          dest_processed_data,
                                          case_log.test_case_id)

                save_case_log(case_log, case_log_execution_status)
                # save_job_status(case_log, case_log_execution_status)


class EditTestCase(Resource):
    """ To handle GET,PUT APIs for getting and updating tese case details """

    @token_required
    def get(self, session):
        """
        To get test case details from the data base for the user provided
        test case id.

        Args:
            session (object):By using this object we can get the user_id.

        Returns:
            Standard API Response with message(returns message saying
            that data loaded successfully) and data,http status code.
        """
        get_testcase_parser = reqparse.RequestParser()
        get_testcase_parser.add_argument('test_case_id', required=True,
                                         type=int,
                                         location='args')
        testcase_id = get_testcase_parser.parse_args()
        try:
            if testcase_id:
                test_case_id = testcase_id.get("test_case_id")
                db_obj = TestCase.query.filter_by(
                    test_case_id=test_case_id).one()
                if db_obj:
                    test_case_detail = db_obj.test_case_detail
                    source_db_id = test_case_detail["src_db_id"]
                    target_db_id = test_case_detail["target_db_id"]
                    table_names_dic = get_table_name(test_case_detail["table"])
                    DbConnection_object_src = DbConnection.query.filter_by(
                        db_connection_id=source_db_id).first()
                    DbConnection_object_target = DbConnection.query.filter_by(
                        db_connection_id=target_db_id).first()
                    DbConnection_detail_src = db_details_without_password(
                        DbConnection_object_src.db_connection_id)
                    DbConnection_detail_target = db_details_without_password(
                        DbConnection_object_target.db_connection_id)
                    if test_case_detail["column"] == {}:
                        column = ''
                    else:
                        column = test_case_detail["column"]
                    test_case_class = SupportedTestClass(). \
                        get_test_class_name_by_id(
                        db_obj.test_case_class)
                    queries = test_case_detail["query"]

                    if test_case_detail["query"] == {}:
                        src_qry = ''
                        target_qry = ''
                    else:
                        query_list = []
                        if test_case_class == "countcheck" or \
                                test_case_class == "datavalidation":
                            src_query = queries["sourceqry"]
                            target_query = queries["targetqry"]
                            query_list.append(src_query)
                            query_list.append(target_query)
                            src_qry = query_list[0]
                            target_qry = query_list[1]
                        else:
                            src_qry = 'None'
                            target_qry = queries["targetqry"]
                    payload = {"test_case_id": db_obj.test_case_id,
                               "test_case_class": test_case_class,
                               "test_status": ExecutionStatus().
                                   get_execution_status_by_id(
                                   db_obj.latest_execution_status),
                               "src_table": table_names_dic["src_table"],
                               "target_table": table_names_dic["target_table"],
                               "src_db_id": source_db_id,
                               "target_db_id": target_db_id,
                               "src_db_name": DbConnection_detail_src[
                                   "db_name"],
                               "des_db_name": DbConnection_detail_target[
                                   "db_name"],
                               "src_db_type": SupportedDBType().
                                   get_db_name_by_id(
                                   DbConnection_detail_src["db_type"]),
                               "des_db_type": SupportedDBType().
                                   get_db_name_by_id(
                                   DbConnection_detail_target["db_type"]),
                               "src_connection_name": DbConnection_detail_src[
                                   "db_connection_name"],
                               "target_connection_name":
                                   DbConnection_detail_target[
                                       "db_connection_name"],

                               "column": column,
                               "test_queries": test_case_detail["query"],
                               "src_qry": src_qry,
                               "des_qry": target_qry
                               }
                    return api_response(True, APIMessages.DATA_LOADED,
                                        STATUS_CREATED,
                                        payload)
                else:
                    return api_response(False,
                                        APIMessages.TEST_CASE_NOT_IN_DB.format(
                                            test_case_id),
                                        STATUS_BAD_REQUEST)
            else:
                return api_response(False,
                                    APIMessages.PASS_TESTCASEID,
                                    STATUS_BAD_REQUEST)
        except SQLAlchemyError as e:
            db.session.rollback()
            return api_response(False, APIMessages.INTERNAL_ERROR,
                                STATUS_SERVER_ERROR,
                                {'error_log': str(e)})
        except Exception as e:
            return api_response(False, APIMessages.INTERNAL_ERROR,
                                STATUS_SERVER_ERROR,
                                {'error_log': str(e)})

    @token_required
    def put(self, session):
        """
        To update the test case details in the database for the user provided
        test case id.

        Args:
            session (object):By using this object we can get the user_id.

        Returns:
             Standard API Response with message(returns message saying
            that test case details updated successfully) and http status code.
        """
        # TODO: Need to use save to db only at the last(after all the fileds)
        put_testcase_parser = reqparse.RequestParser(bundle_errors=True)
        put_testcase_parser.add_argument('test_case_id', required=True,
                                         type=int)
        put_testcase_parser.add_argument('src_table', type=str)
        put_testcase_parser.add_argument('target_table', type=str)
        put_testcase_parser.add_argument('src_qry', type=str)
        put_testcase_parser.add_argument('target_qry', type=str)
        put_testcase_parser.add_argument('column', type=str)
        put_testcase_parser.add_argument('src_db_id', type=int)
        put_testcase_parser.add_argument('target_db_id', type=int)
        user_test_case_detail = put_testcase_parser.parse_args()
        test_case_id = user_test_case_detail["test_case_id"]
        try:
            if test_case_id:
                db_obj = TestCase.query.filter_by(
                    test_case_id=test_case_id).first()
                del user_test_case_detail["test_case_id"]
                if db_obj:
                    testcasedetail = db_obj.test_case_detail
                    for key, value in user_test_case_detail.items():
                        if value and str(value).strip():
                            if key == 'src_db_id':
                                testcasedetail["src_db_id"] = \
                                    user_test_case_detail["src_db_id"]
                                db_obj.save_to_db()
                            if key == 'target_db_id':
                                testcasedetail["target_db_id"] = \
                                    user_test_case_detail["target_db_id"]
                                db_obj.save_to_db()
                            if key == 'src_table':
                                table = testcasedetail["table"]
                                for key in table:
                                    target_table = table[key]
                                table[user_test_case_detail['src_table']] = key
                                del table[key]
                                table[
                                    user_test_case_detail[
                                        'src_table']] = target_table
                                db_obj.save_to_db()
                            if key == "target_table":
                                table = testcasedetail["table"]
                                for key in table:
                                    table[key] = user_test_case_detail[
                                        "target_table"]
                                db_obj.save_to_db()
                            if key == "src_qry":
                                queries = testcasedetail["query"]
                                queries["sourceqry"] = user_test_case_detail[
                                    "src_qry"]
                                db_obj.save_to_db()
                            if key == "target_qry":
                                queries = testcasedetail["query"]
                                queries["targetqry"] = user_test_case_detail[
                                    "target_qry"]
                                db_obj.save_to_db()
                            if key == "column":
                                column = testcasedetail["column"]
                                if ";" and ":" in user_test_case_detail[
                                    "column"]:
                                    column = {}

                                    user_columns = user_test_case_detail[
                                        "column"].split(
                                        ";")
                                    for columnpair in user_columns:
                                        if ":" in columnpair:
                                            singlecolumn = columnpair.split(
                                                ":")
                                            column[singlecolumn[0]] = \
                                                singlecolumn[1]
                                        else:
                                            column[columnpair] = columnpair
                                    testcasedetail["column"] = column
                                elif ";" in user_test_case_detail["column"]:
                                    column = {}
                                    columns = user_test_case_detail[
                                        "column"].split(";")
                                    for singlecolumn in columns:
                                        column[singlecolumn] = singlecolumn
                                    testcasedetail["column"] = column
                                else:
                                    column = {}
                                    column[user_test_case_detail["column"]] = \
                                        user_test_case_detail["column"]
                                    testcasedetail["column"] = column
                                db_obj.save_to_db()

                    db_obj.test_case_detail = testcasedetail
                    db_obj.save_to_db()
                    return api_response(
                        True, APIMessages.TEST_CASE_DETAILS_UPDATED.format(
                            test_case_id), STATUS_CREATED)
                else:
                    return api_response(False,
                                        APIMessages.TEST_CASE_NOT_IN_DB.format(
                                            test_case_id),
                                        STATUS_BAD_REQUEST)
            else:
                return api_response(False, APIMessages.PASS_TESTCASEID,
                                    STATUS_BAD_REQUEST)

        except SQLAlchemyError as e:
            db.session.rollback()
            return api_response(False, APIMessages.INTERNAL_ERROR,
                                STATUS_SERVER_ERROR,
                                {'error_log': str(e)})
        except Exception as e:
            return api_response(False, APIMessages.INTERNAL_ERROR,
                                STATUS_SERVER_ERROR,
                                {'error_log': str(e)})


class TestCaseJobExternal(Resource):
    """
    class to  Execute the job from external source
    """

    @token_required
    def post(self, session):
        """
        Method to execute the job from external source by the use of token
        generated from the user
        Args:
            session (Obj): session obj will give the user_id

        Returns:  execute the job from external source by the use of token
        generated from the user

        """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('suite_id', type=int, required=False,
                                help=APIMessages.PARSER_MESSAGE,
                                location="json")
            parser.add_argument('case_id_list',
                                required=False,
                                help=APIMessages.PARSER_MESSAGE,
                                type=list, default=list(), location="json")
            parser.add_argument('token', type=str, required=True,
                                location="json",
                                help=APIMessages.PARSER_MESSAGE)
            execution_data = parser.parse_args()
            user_id = session.user_id
            is_external = True
            token = execution_data['token']
            personal_token_obj = PersonalToken.query.filter_by(
                encrypted_personal_token=token).first()
            if execution_data['case_id_list'] and not execution_data[
                'suite_id']:
                if personal_token_obj.user_id == user_id:
                    test_case_obj = TestCase.query.filter_by(
                        test_case_id=execution_data['case_id_list'][0]).first()
                    test_suite_id = test_case_obj.test_suite_id
                    run_result = create_job(user_id, test_suite_id,
                                            execution_data['case_id_list'],
                                            is_external)
                    return api_response(True, APIMessages.RETURN_SUCCESS,
                                        STATUS_CREATED)
                else:
                    return api_response(False, APIMessages.TOKEN_MISMATCH,
                                        STATUS_SERVER_ERROR)

            elif execution_data['suite_id'] and not execution_data[
                'case_id_list']:
                if personal_token_obj.user_id == user_id:
                    create_job(user_id, execution_data['suite_id'],
                               is_external)
                    return api_response(True, APIMessages.RETURN_SUCCESS,
                                        STATUS_CREATED)
                else:
                    return api_response(False, APIMessages.TOKEN_MISMATCH,
                                        STATUS_SERVER_ERROR)
        except Exception as e:
            return api_response(False, APIMessages.INTERNAL_ERROR,
                                STATUS_SERVER_ERROR,
                                {'error_log': str(e)})
