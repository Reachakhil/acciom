import datetime
from collections import OrderedDict
from datetime import date
from datetime import datetime as dt
from flask_restful import Resource, reqparse
from sqlalchemy import Date
from statistics import mean

from application.common.constants import (APIMessages, SupportedTestClass)
from application.common.response import (api_response, STATUS_OK,
                                         STATUS_SERVER_ERROR,
                                         STATUS_BAD_REQUEST, STATUS_NOT_FOUND)
from application.common.token import token_required
from application.model.models import (Organization, Project, TestSuite,
                                      TestCase, TestCaseLog)
from index import db


class ProjectDQI(Resource):
    """
    URL: /api/project-data-quality-index
        Returns the Projects Data Quality Index for specified time range (OR)
        for all the test suites
    Actions:
        GET:
            - Returns Data Quality Index for given project id on a test case
            type level.
    """
    dqi_name_casting = OrderedDict([('completeness', 'countcheck'),
                                    ('Null', 'nullcheck'),
                                    ('duplicates', 'duplicatecheck'),
                                    ('consistency', 'ddlcheck'),
                                    ('correcteness', 'datavalidation')])

    @token_required
    def get(self, session):
        project_dql_parser = reqparse.RequestParser()
        project_dql_parser.add_argument('project_id',
                                        help=APIMessages.PARSER_MESSAGE.format(
                                            'project_id'), required=True,
                                        type=int, location='args')
        project_dql_parser.add_argument("start_date",
                                        help=APIMessages.PARSER_MESSAGE.format(
                                            'start_date'), required=False,
                                        type=str, location='args')
        project_dql_parser.add_argument("end_date",
                                        help=APIMessages.PARSER_MESSAGE.format(
                                            'end_date'), required=False,
                                        type=str, location='args')
        project_dql_args = project_dql_parser.parse_args()
        try:
            project_obj = Project.query.filter_by(project_id=project_dql_args[
                "project_id"]).first()
            if not project_obj:
                return api_response(False, APIMessages.INVALID_PROJECT_ID,
                                    STATUS_NOT_FOUND)
            project_dql_avg, dqi_values = get_project_dqi(
                project_dql_args['project_id'], project_dql_args['start_date'],
                project_dql_args['end_date'])
            dqi_list = list()
            for key in self.dqi_name_casting.keys():
                dqi_dict = dict()
                dqi_dict["name"] = key
                dqi_dict["value"] = dqi_values[self.dqi_name_casting[key]]
                dqi_list.append(dqi_dict)
            project_dql_data = dict()
            project_dql_data['project_name'] = project_obj.project_name
            project_dql_data['project_id'] = project_obj.project_id
            project_dql_data['project_dqi_percentage'] = project_dql_avg
            project_dql_data['project_dqi_detail'] = dqi_list
            project_dql_data['start_date'] = project_dql_args['start_date']
            project_dql_data['end_date'] = project_dql_args['end_date']
            return api_response(True, APIMessages.SUCCESS, STATUS_OK,
                                project_dql_data)
        except Exception as e:
            return api_response(
                False, APIMessages.INTERNAL_ERROR, STATUS_SERVER_ERROR,
                {'error_log': str(e)})


class OrganizationDQI(Resource):
    """
    URL: /api/project-data-quality-index
        Returns the Projects Data Quality Index for specified time range (OR)
        for all the test suites
    Actions:
        GET:
            - Returns Data Quality Index for given project id on a test case
            type level.
    """

    @token_required
    def get(self, session):
        org_dql_parser = reqparse.RequestParser()
        org_dql_parser.add_argument('org_id',
                                    help=APIMessages.PARSER_MESSAGE.format(
                                        'org_id'), required=True,
                                    type=int, location='args')
        org_dql_parser.add_argument("start_date",
                                    help=APIMessages.PARSER_MESSAGE.format(
                                        'start_date'), required=False,
                                    type=str, location='args')
        org_dql_parser.add_argument("end_date",
                                    help=APIMessages.PARSER_MESSAGE.format(
                                        'end_date'), required=False,
                                    type=str, location='args')
        org_dql_args = org_dql_parser.parse_args()
        try:
            org_obj = Organization.query.filter_by(org_id=org_dql_args[
                "org_id"]).first()
            if not org_obj:
                return api_response(False, APIMessages.INVALID_ORG_ID,
                                    STATUS_NOT_FOUND)
            project_obj_list = Project.query.filter_by(
                org_id=org_obj.org_id).all()
            project_list = list()
            for project_obj in project_obj_list:
                project_dict = dict()
                project_dql_avg, dqi_values = get_project_dqi(
                    project_obj.project_id, org_dql_args['start_date'],
                    org_dql_args['end_date'])
                project_dict['project_id'] = project_obj.project_id
                project_dict['project_name'] = project_obj.project_name
                project_dict['project_dqi_percentage'] = project_dql_avg

                project_list.append(project_dict)
            org_data = dict()
            org_data['org_name'] = org_obj.org_name
            org_data['org_id'] = org_obj.org_id
            org_data['start_date'] = org_dql_args['start_date']
            org_data['end_date'] = org_dql_args['end_date']
            org_data['projects'] = project_list
            return api_response(True, APIMessages.SUCCESS, STATUS_OK, org_data)
        except Exception as e:
            return api_response(False, APIMessages.INTERNAL_ERROR,
                                STATUS_SERVER_ERROR, {'error_log': str(e)})


class ProjectDQIHistory(Resource):
    """
    URL: /api/project-dqi-history
        Returns the Projects Data Quality Index for specified time range (OR)
        for all the test suites
    Actions:
        GET:
            - Returns Data Quality Index for given project id on a test case
            type level.
    """

    @token_required
    def get(self, session):
        dqi_history_parser = reqparse.RequestParser()
        dqi_history_parser.add_argument('project_id',
                                        help=APIMessages.PARSER_MESSAGE.format(
                                            'org_id'), required=True,
                                        type=int, location='args')
        dqi_history_parser.add_argument("start_date",
                                        help=APIMessages.PARSER_MESSAGE.format(
                                            'start_date'), required=False,
                                        type=str, location='args')
        dqi_history_parser.add_argument("end_date",
                                        help=APIMessages.PARSER_MESSAGE.format(
                                            'end_date'), required=False,
                                        type=str, location='args')
        dqi_history_data = dqi_history_parser.parse_args()

        # check if project Id exists
        check_valid_project = Project.query.filter_by(
            project_id=dqi_history_data['project_id']).first()
        if not check_valid_project:
            return api_response(
                False, APIMessages.NO_RESOURCE.format('Project'),
                STATUS_BAD_REQUEST)
        # Check if both start and end date are passed instead either of them
        if (dqi_history_data['start_date']
            and not dqi_history_data['end_date']) or \
                (not dqi_history_data['start_date'] and
                 dqi_history_data['end_date']):
            return api_response(False, APIMessages.START_END_DATE,
                                STATUS_BAD_REQUEST)
        try:
            # check if user passed dates in yyyy-mm-dd format
            start_date, end_date = "", ""
            if dqi_history_data['start_date'] and dqi_history_data['end_date']:
                start_date = dt.strptime(
                    dqi_history_data['start_date'] + " 00:00:00",
                    "%Y-%m-%d %H:%M:%S")
                end_date = dt.strptime(
                    dqi_history_data['end_date'] + " 23:59:59",
                    "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return api_response(False, APIMessages.DATE_FORMAT,
                                STATUS_BAD_REQUEST)
        # calling get_project_dqi_history to get day wise data
        daily_dqi = get_project_dqi_history(
            dqi_history_data['project_id'], start_date=start_date,
            end_date=end_date)
        dqi_response = dict()
        dqi_response['project_id'] = dqi_history_data['project_id']
        dqi_response['project_name'] = check_valid_project.project_name
        dqi_response['dqi_history'] = daily_dqi
        return api_response(True, APIMessages.SUCCESS, STATUS_OK, dqi_response)


def get_project_dqi_history(project_id, start_date=None, end_date=None):
    """
    Method to return day wise dqi for each class.

    Args:
        project_id (int): Id of the project
        start_date (datetime): Date in YY-MM-DD H:M:S format
        end_date(datetime): Date in YY-MM-DD H:M:S format

    Returns: dict of dqi for each class with key as date

    """
    # If start and end date are not mentioned, take current month range
    if not start_date and not end_date:
        # If start and end date are not given, take current month range
        current_day = dt.today()
        current_month_first_day = date.today().replace(day=1)
        start_date = current_month_first_day
        end_date = current_day
    # Query that returns distinct rows with Date, dqi, test case class, test
    # suite id, and test case id order by last modified date
    dqi_for_each_day = db.session.query(
        TestCaseLog.modified_at.cast(Date), TestCaseLog.dqi_percentage,
        TestCase.test_case_class, TestSuite.test_suite_id,
        TestCase.test_case_id).distinct(
        TestCaseLog.modified_at.cast(Date), TestCase.test_case_id,
        TestSuite.test_suite_id).order_by(
        TestCaseLog.modified_at.cast(Date).desc(), TestCase.test_case_id,
        TestSuite.test_suite_id).order_by(
        TestCaseLog.modified_at.desc()).filter(
        TestCaseLog.modified_at >= start_date,
        TestCaseLog.modified_at <= end_date,
        TestCaseLog.dqi_percentage != None).join(
        TestCase, TestCaseLog.test_case_id == TestCase.test_case_id).join(
        TestSuite, TestCase.test_suite_id == TestSuite.test_suite_id).join(
        Project, TestSuite.project_id == Project.project_id).filter(
        Project.project_id == project_id).all()
    # temp dict is used to store values from tuple with each day
    temp_dict = {}
    for each_tuple in dqi_for_each_day:
        if each_tuple[3] not in temp_dict:
            temp_dict[each_tuple[3]] = {}
        if each_tuple[3] in temp_dict and each_tuple[2] not in \
                temp_dict[each_tuple[3]]:
            temp_dict[each_tuple[3]][each_tuple[2]] = {}
        if each_tuple[2] in temp_dict[each_tuple[3]] and each_tuple[4] not in \
                temp_dict[each_tuple[3]][each_tuple[2]]:
            temp_dict[each_tuple[3]][each_tuple[2]][each_tuple[4]] = {}
        if each_tuple[0].strftime("%Y-%m-%d") not in \
                temp_dict[each_tuple[3]][each_tuple[2]][each_tuple[4]]:
            temp_dict[each_tuple[3]][each_tuple[2]][each_tuple[4]][
                each_tuple[0].strftime("%Y-%m-%d")] = {}
        temp_dict[each_tuple[3]][each_tuple[2]][each_tuple[4]][each_tuple[0].
            strftime(
            "%Y-%m-%d")][SupportedTestClass(
        ).get_test_class_name_by_id(each_tuple[2])] = each_tuple[1]
    # dict_dqi_for_each_class is used to store
    # list of dqi for each class for each day
    dict_dqi_for_each_class = {}
    for suite_key, suite_value in temp_dict.items():
        for class_key, class_value in suite_value.items():
            for test_case_key, test_case_value in class_value.items():
                for date_key, date_value in test_case_value.items():
                    if date_key not in dict_dqi_for_each_class:
                        dict_dqi_for_each_class[date_key] = {}
                    for class_name, class_value in date_value.items():
                        if class_name not in dict_dqi_for_each_class[date_key]:
                            dict_dqi_for_each_class[date_key][class_name] = []
                        dict_dqi_for_each_class[date_key][class_name].append(
                            class_value)
    # result_dict is used to store average of each class dqi for each day and
    # average dqi for each class
    result_dict = {}
    # Calculating average of all dqi for same classes
    for key_date, dqi_values in dict_dqi_for_each_class.items():
        if key_date not in result_dict:
            result_dict[key_date] = {}
        for dqi_class, list_dqi_values in dqi_values.items():
            result_dict[key_date][dqi_class] = round(mean(list_dqi_values), 4)
    # Calculating average of all dqi for different classes
    for each_date, percentage in result_dict.items():
        result_dict[each_date]['average_dqi'] = round(mean(
            percentage.values()), 4)
    return result_dict


def get_project_dqi(project_id, start_date=None, end_date=None):
    """
    Calculates the Data Quality Index for each test case type for all the
    test cases under a given Project and for the given time fream if start date
    and end date is provided.
    Args:
        project_id (int): id of the project
        start_date (str) : start date for the query
        end_date (str) : end date for the query
    Return:
        project_dql_avg
        dqi_values
    """
    test_suite_obj_list = TestSuite.query.filter_by(
        project_id=project_id).all()
    test_suite_id_list = list()
    for test_suite_obj in test_suite_obj_list:
        test_suite_id_list.append(test_suite_obj.test_suite_id)
    test_case_obj_list = TestCase.query.filter(
        TestCase.test_suite_id.in_(test_suite_id_list)).all()
    dqi_values = dict()
    for values in SupportedTestClass.supported_test_class.values():
        dqi_values[values] = list()
    for test_case_obj in test_case_obj_list:
        if start_date and end_date:
            test_start_date = datetime.datetime.strptime(start_date,
                                                         "%Y-%m-%d")
            test_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            test_end_date += datetime.timedelta(days=1)
            test_case_log_list = TestCaseLog.query.filter_by(
                test_case_id=test_case_obj.test_case_id).filter(
                TestCase.modified_at >= test_start_date).filter(
                TestCase.modified_at <= test_end_date).all()
        else:
            test_case_log_list = TestCaseLog.query.filter_by(
                test_case_id=test_case_obj.test_case_id).all()
        for test_case_log_obj in test_case_log_list:
            if test_case_log_obj.dqi_percentage:
                dqi_values[SupportedTestClass.supported_test_class[
                    test_case_obj.test_case_class]].append(
                    test_case_log_obj.dqi_percentage)
    for key in dqi_values.keys():
        if dqi_values[key]:
            dqi_values[key] = sum(dqi_values[key]) / len(dqi_values[key])
    project_dql_avg = 0
    for key, value in dqi_values.items():
        if value:
            project_dql_avg += value
        else:
            dqi_values[key] = 0
    project_dql_avg = project_dql_avg / len(dqi_values.values())

    return project_dql_avg, dqi_values
