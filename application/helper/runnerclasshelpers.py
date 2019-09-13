import ast

from application.common.constants import ExecutionStatus
from application.common.dbconnect import dbconnection
from application.helper.corefunctions.countcheck import count_check
from application.helper.corefunctions.datavalidation import datavalidation
from application.helper.corefunctions.ddlcheck import ddl_check
from application.helper.corefunctions.duplicate import duplication
from application.helper.corefunctions.nullcheck import null_check
from application.helper.encrypt import decrypt
from application.model.models import DbConnection, TestCase, Job


class TestCaseExecution():
    """
    This class will execute test case based on its test case class
    """

    def create_connector(test_case_details):
        """

        Returns: this Method creates a connector for given db details

        """
        connector = dbconnection(test_case_details['db_name'],
                                 test_case_details['db_type'],
                                 test_case_details[
                                     'db_hostname'].lower(),
                                 test_case_details['db_username'],
                                 test_case_details[
                                     'db_password']).cursor()
        return connector

    def get_tables(test_case_detail):
        """

        Returns: Returns table from the test_case_details stored as json

        """
        return split_table(test_case_detail)

    def get_query(test_case_detail):
        """

        Returns:Returns query from the test_case_details stored as json

        """
        return get_query(test_case_detail)

    @classmethod
    def count_check(cls, src_db_id, target_db_id, test_case_details):
        """

        Args:
            src_db_id (int): source_db_id used to find db_details
            target_db_id (int): target_db_id used to find db_details
            test_case_details (json): json details used for finding table,
            queries

        Returns: Execute CountCheck and returns the status

        """
        try:

            src_detail = db_details(src_db_id)
            target_detail = db_details(target_db_id)
            source_db_connector = cls.create_connector(src_detail)
            target_db_connector = cls.create_connector(target_detail)
            table_name = cls.get_tables(test_case_details)
            query = get_query(test_case_details)
            result = count_check(source_db_connector,
                                 target_db_connector,
                                 table_name['src_table'],
                                 table_name['target_table'],
                                 query)
            return result
        except Exception as e:
            execution_result = ExecutionStatus(). \
                get_execution_status_id_by_name('error')
            result = {"res": execution_result,
                      "Execution_log": {"error_log": str(e)}}
            return result

    @classmethod
    def null_check(cls, src_db_id, target_db_id, test_case_details):
        """

               Args:
                   src_db_id (int): source_db_id used to find db_details
                   target_db_id (int): target_db_id used to find db_details
                   test_case_details (json): json details used for finding table,
                   queries

               Returns: Execute NullCheck and returns the status

               """
        try:

            target_detail = db_details(target_db_id)
            target_db_connector = cls.create_connector(target_detail)
            table_name = cls.get_tables(test_case_details)
            query = get_query(test_case_details)
            column = get_column(test_case_details)
            result = null_check(target_db_connector,
                                table_name['target_table'], column,
                                query, target_detail['db_type'])
            return result
        except Exception as e:
            execution_result = ExecutionStatus(). \
                get_execution_status_id_by_name('error')
            result = {"res": execution_result,
                      "Execution_log": {"error_log": str(e)}}
            return result

    @classmethod
    def duplicate_check(cls, src_db_id, target_db_id, test_case_details):
        """

               Args:
                   src_db_id (int): source_db_id used to find db_details
                   target_db_id (int): target_db_id used to find db_details
                   test_case_details (json): json details used for finding table,
                   queries

               Returns: Execute Duplicate and returns the status

               """
        try:

            target_detail = db_details(target_db_id)
            target_db_connector = cls.create_connector(target_detail)
            table_name = cls.get_tables(test_case_details)
            query = get_query(test_case_details)
            column = get_column(test_case_details)
            result = duplication(target_db_connector,
                                 table_name['target_table'], column,
                                 query, target_detail['db_type'])
            return result
        except Exception as e:
            execution_result = ExecutionStatus(). \
                get_execution_status_id_by_name('error')
            result = {"res": execution_result,
                      "Execution_log": {"error_log": str(e)}}
            return result

    @classmethod
    def ddlcheck(cls, src_db_id, target_db_id, test_case_details):
        """

               Args:
                   src_db_id (int): source_db_id used to find db_details
                   target_db_id (int): target_db_id used to find db_details
                   test_case_details (json): json details used for finding table,
                   queries

               Returns: Execute DDLcheck and returns the status

               """
        try:
            src_detail = db_details(src_db_id)
            source_db_connector = cls.create_connector(src_detail)
            target_detail = db_details(target_db_id)
            target_db_connector = cls.create_connector(target_detail)
            table_name = cls.get_tables(test_case_details)
            query = get_query(test_case_details)
            result = ddl_check(source_db_connector, target_db_connector,
                               table_name['src_table'],
                               table_name['target_table'],
                               src_detail['db_type'],
                               target_detail['db_type'])
            return result
        except Exception as e:
            execution_result = ExecutionStatus(). \
                get_execution_status_id_by_name('error')
            result = {"res": execution_result,
                      "Execution_log": {"error_log": str(e)}}
            return result

    @classmethod
    def data_validation(cls, src_db_id, target_db_id, test_case_details,
                        case_log):
        """

               Args:
                   src_db_id (int): source_db_id used to find db_details
                   target_db_id (int): target_db_id used to find db_details
                   test_case_details (json): json details used for finding table,
                   queries
                   case_log

               Returns: Execute Datavalidation and returns the status

               """
        try:
            src_detail = db_details(src_db_id)
            target_detail = db_details(target_db_id)
            table_name = cls.get_tables(test_case_details)
            query = get_query(test_case_details)
            if query == {}:
                src_qry = ""
                target_qry = ""
            else:
                src_qry = query[
                    'sourceqry'] if 'sourceqry' in query else ""
                target_qry = query[
                    'targetqry'] if 'targetqry' in query else ""
            datavalidation(src_detail['db_name'],
                           table_name['src_table'],
                           src_detail['db_type'],
                           target_detail['db_name'],
                           table_name['target_table'],
                           target_detail['db_type'],
                           src_detail['db_username'],
                           src_detail['db_password'],
                           src_detail['db_hostname'],
                           target_detail['db_username'],
                           target_detail['db_password'],
                           target_detail['db_hostname'],
                           src_qry, target_qry, case_log)
        except Exception as e:
            execution_result = ExecutionStatus(). \
                get_execution_status_id_by_name('error')
            result = {"res": execution_result,
                      "Execution_log": {"error_log": str(e)}}
            return result


def db_details(db_id):
    """
    Return db_Details as a list of the particular db_connection_id asked.
    Args:
        db_id(Int):  db_connection_id

    Returns: a list of db_Details associated with db_connection_id.

    """
    db_list = {}
    db_obj = DbConnection.query.filter_by(db_connection_id=db_id).first()
    encrypted_password = db_obj.db_encrypted_password.encode()
    decrypted = decrypt(encrypted_password)
    decrypted_password = bytes.decode(decrypted)
    db_list['db_id'] = db_obj.db_connection_id
    db_list['db_type'] = db_obj.db_type
    db_list['db_name'] = db_obj.db_name
    db_list['db_hostname'] = db_obj.db_hostname
    db_list['db_username'] = db_obj.db_username
    db_list['db_password'] = decrypted_password
    return db_list


def split_table(test_case_details):
    """
    Method to split tables from the Json stored in the test_case table.
    Args:
        test_case_details(Json): JSON from test_case table

    Returns: splited table names in dictionary

    """
    table_dict = {}
    tables = test_case_details["table"]
    for each_table in tables:
        table_dict['src_table'] = each_table
        table_dict['target_table'] = tables[each_table]
    return table_dict


def get_query(queries):
    """
    Parse the query from stored in the Json format in the case_detail of the
    test_case table
    Args:
        queries: query from Excel as Text

    Returns: Parsed queries

    """
    query = queries["query"]
    return query


def get_column(columns):
    """
    Method to retrieve columns from the Json stored in the case_details table
    of the test_case table
    Args:
        columns: columns as Text from Excel

    Returns: list of columns

    """
    column = columns["column"]
    column = list(column.values())
    return column


def save_case_log(case_log, case_log_execution_status):
    """
    Methods to store case_log execution details in testcase table
    Args:
        case_log(int): test_case_log_id of the test_case_log table
        case_log_execution_status(int): Execution status

    Returns: save case details to the db

    """
    case = TestCase.query.filter_by(
        test_case_id=case_log.test_case_id).first()
    case.latest_execution_status = case_log_execution_status
    case.save_to_db()


def save_job_status(case_log, case_log_execution_status):
    """
    Method will save job_status in Jobs table of the db ,it accepts case_log_id
    and case_log_Execution_Status
    Args:
        case_log(obj): case_log object of the case_log table
        case_log_execution_status(int): case_log_Execution status of the table
        in int

    Returns:

    """
    Job_obj = Job.query.filter_by(job_id=case_log.job_id).first()
    Job_obj.execution_status = case_log_execution_status
    Job_obj.save_to_db()


def args_as_list(list_args):
    """
    Method will return the list out of the arguments passed
    Args:
        list_args: accepts argument from parser

    Returns: a List

    """
    list_arg = ast.literal_eval(list_args)
    if type(list_arg) is not list:
        pass
    return list_arg


def datavalidation_result_format_change(log):
    """
    Change the format of result log ex:[{"id":1,"name":"hj","quantity":2}]

    Args:
        log: log of datavalidation

    Returns:
        Changed format of log ex:[["id","name","quantity"],[1,"hj",2]]
    """
    result = []
    keys = []
    for key, value in log[0].items():
        keys.append(key)
    result.append(keys)
    for dic in log:
        values = []
        for key, value in dic.items():
            values.append(value)
        result.append(values)
    return result
