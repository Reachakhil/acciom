"""File to handle DQI reports."""
import datetime
from collections import OrderedDict
from datetime import date
from datetime import datetime as dt
from statistics import mean

from flask_restful import Resource, reqparse
from sqlalchemy import Date

from application.common.common_exception import (ResourceNotAvailableException,
                                                 GenericBadRequestException)
from application.common.constants import (APIMessages, SupportedTestClass,
                                          TestTypeDisplay, TestClass,
                                          DQIClassNameMapping)
from application.common.response import (api_response, STATUS_OK)
from application.common.token import token_required
from application.helper.permission_check import check_permission
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
        # check if project Id exists
        check_valid_project = Project.query.filter_by(
            project_id=project_dql_args['project_id'],
            is_deleted=False).first()
        if not check_valid_project:
            raise ResourceNotAvailableException("Project")
        # checking if user is authorized to make this call
        check_permission(session.user, list_of_permissions=["view_project"],
                         org_id=check_valid_project.org_id,
                         project_id=project_dql_args['project_id'])
        # Check if both start and end date are passed instead either of them
        if (project_dql_args['start_date']
            and not project_dql_args['end_date']) or \
                (not project_dql_args['start_date'] and
                 project_dql_args['end_date']):
            raise GenericBadRequestException(APIMessages.START_END_DATE)
        try:
            # check if user passed dates in yyyy-mm-dd format
            start_date, end_date = "", ""
            if project_dql_args['start_date'] and project_dql_args['end_date']:
                start_date = dt.strptime(
                    project_dql_args['start_date'] + " 00:00:00",
                    "%Y-%m-%d %H:%M:%S")
                end_date = dt.strptime(
                    project_dql_args['end_date'] + " 23:59:59",
                    "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise GenericBadRequestException(APIMessages.DATE_FORMAT)
        dqi_name_casting = OrderedDict(
            [(TestTypeDisplay.COMPLETENESS, TestClass.COUNT_CHECK),
             (TestTypeDisplay.NULLS, TestClass.NULL_CHECK),
             (TestTypeDisplay.DUPLICATES, TestClass.DUPLICATE_CHECK),
             (TestTypeDisplay.CONSISTENCY, TestClass.DDL_CHECK),
             (TestTypeDisplay.CORRECTNESS, TestClass.DATA_VALIDATION)])
        list_of_project_dqi, project_dqi_average, starting_date, \
        ending_date = get_project_dqi(
            project_dql_args['project_id'], start_date, end_date)
        dqi_list = list()
        for each_display_class in dqi_name_casting.keys():
            if each_display_class in list_of_project_dqi.keys():
                dqi_dict = dict()
                dqi_dict['name'] = each_display_class
                dqi_dict['value'] = list_of_project_dqi[each_display_class]
                dqi_list.append(dqi_dict)
        project_dql_data = dict()
        project_dql_data['project_name'] = check_valid_project.project_name
        project_dql_data['project_id'] = check_valid_project.project_id
        project_dql_data['project_dqi_percentage'] = project_dqi_average
        project_dql_data['project_dqi_detail'] = dqi_list
        project_dql_data['start_date'] = str(starting_date)
        project_dql_data['end_date'] = str(ending_date)
        return api_response(True, APIMessages.SUCCESS, STATUS_OK,
                            project_dql_data)


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
        valid_org = Organization.query.filter_by(org_id=org_dql_args[
            "org_id"], is_deleted=False).first()
        if not valid_org:
            raise ResourceNotAvailableException("Organization")
        # checking if user is authorized to make this call
        check_permission(session.user,
                         list_of_permissions=["view_org"],
                         org_id=org_dql_args['org_id'])
        # Check if both start and end date are passed instead either of them
        if (org_dql_args['start_date']
            and not org_dql_args['end_date']) or \
                (not org_dql_args['start_date'] and
                 org_dql_args['end_date']):
            raise GenericBadRequestException(APIMessages.START_END_DATE)
        try:
            # check if user passed dates in yyyy-mm-dd format
            start_date, end_date = "", ""
            if org_dql_args['start_date'] and org_dql_args['end_date']:
                start_date = dt.strptime(
                    org_dql_args['start_date'] + " 00:00:00",
                    "%Y-%m-%d %H:%M:%S")
                end_date = dt.strptime(
                    org_dql_args['end_date'] + " 23:59:59",
                    "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise GenericBadRequestException(APIMessages.DATE_FORMAT)
        project_obj_list = Project.query.filter_by(
            org_id=valid_org.org_id, is_deleted=False).all()
        project_list = list()
        for project_obj in project_obj_list:
            project_dict = dict()
            dqi_dict, project_dql_avg, starting_date, ending_date = \
                get_project_dqi(project_obj.project_id, start_date, end_date)
            project_dict['project_id'] = project_obj.project_id
            project_dict['project_name'] = project_obj.project_name
            project_dict['project_dqi_percentage'] = project_dql_avg
            project_list.append(project_dict)
        org_data = dict()
        org_data['org_name'] = valid_org.org_name
        org_data['org_id'] = valid_org.org_id
        org_data['start_date'] = str(starting_date)
        org_data['end_date'] = str(ending_date)
        org_data['projects'] = project_list
        return api_response(True, APIMessages.SUCCESS, STATUS_OK, org_data)


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
            project_id=dqi_history_data['project_id'],
            is_deleted=False).first()
        if not check_valid_project:
            raise ResourceNotAvailableException("Project")
            # checking if user is authorized to make this call
        check_permission(session.user, list_of_permissions=["view_project"],
                         org_id=check_valid_project.org_id,
                         project_id=dqi_history_data['project_id'])
        # Check if both start and end date are passed instead either of them
        if (dqi_history_data['start_date']
            and not dqi_history_data['end_date']) or \
                (not dqi_history_data['start_date'] and
                 dqi_history_data['end_date']):
            raise GenericBadRequestException(APIMessages.START_END_DATE)
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
            raise GenericBadRequestException(APIMessages.DATE_FORMAT)
        # calling get_project_dqi_history to get day wise data
        daily_dqi = get_project_dqi_history(
            dqi_history_data['project_id'], start_date=start_date,
            end_date=end_date)
        dqi_response = OrderedDict()
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
    temp_dict = dict()
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
    dict_dqi_for_each_class = dict()
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
    result_dict = dict()
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
    sorted_result_dict = OrderedDict()
    for each_sorted_key in sorted(result_dict.keys()):
        sorted_result_dict[each_sorted_key] = result_dict[each_sorted_key]
    return sorted_result_dict


def get_project_dqi(project_id, start_date=None, end_date=None):
    """
    Calculates the Data Quality Index for each test case type for all the
    test cases under a given Project and for the given time frame if start date
    and end date is provided.
    Args:
        project_id (int): id of the project
        start_date (str) : start date for the query
        end_date (str) : end date for the query
    Return:
        project_dql_avg
        dqi_values
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
    dqi_for_each_day = db.session.query(TestCaseLog.modified_at.cast(Date),
                                        TestCaseLog.dqi_percentage,
                                        TestCase.test_case_class,
                                        TestSuite.test_suite_id,
                                        TestCase.test_case_id).distinct(
        TestCase.test_case_id,
        TestSuite.test_suite_id).order_by(
        TestCase.test_case_id,
        TestSuite.test_suite_id).order_by(
        TestCaseLog.modified_at.desc()).filter(
        TestCaseLog.modified_at >= start_date,
        TestCaseLog.modified_at <= end_date,
        TestCaseLog.dqi_percentage != None).join(
        TestCase, TestCaseLog.test_case_id == TestCase.test_case_id).join(
        TestSuite, TestCase.test_suite_id == TestSuite.test_suite_id).join(
        Project, TestSuite.project_id == Project.project_id).filter(
        Project.project_id == project_id).all()
    list_of_dqi_values_for_each_class = {}
    for each_tuple in dqi_for_each_day:
        if SupportedTestClass().get_test_class_name_by_id(each_tuple[2]) \
                not in list_of_dqi_values_for_each_class:
            list_of_dqi_values_for_each_class[
                SupportedTestClass().get_test_class_name_by_id(
                    each_tuple[2])] = []
        list_of_dqi_values_for_each_class[
            SupportedTestClass().get_test_class_name_by_id(
                each_tuple[2])].append(each_tuple[1])
    if not isinstance(start_date, str) and not isinstance(end_date, str):
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

    project_dql_average = 0  # TODO: Need change it to Null and send flag in UI.
    dqi_dict = dict()
    for class_key, class_values in list_of_dqi_values_for_each_class.items():
        dqi_dict[DQIClassNameMapping.dqi_class_name_mapping[class_key]] = \
            round(mean(class_values), 4)
    if dqi_dict:
        project_dql_average = round(mean(dqi_dict.values()), 4)
    return dqi_dict, project_dql_average, start_date, end_date
