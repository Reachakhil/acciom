"""File to handle Organization API calls."""
from datetime import date
from datetime import datetime
from datetime import timedelta

from flask_restful import Resource, reqparse

from application.common.api_permission import ORGANIZATION_API_PUT, \
    DASH_BOARD_STATUS_GET, ORG_DELETE
from application.common.common_exception import ResourceNotAvailableException
from application.common.constants import APIMessages
from application.common.response import (STATUS_CREATED,
                                         STATUS_OK, STATUS_FORBIDDEN,
                                         STATUS_UNAUTHORIZED)
from application.common.response import api_response
from application.common.token import token_required
from application.helper.permission_check import check_permission
from application.model.models import (Organization, Job, TestSuite,
                                      Project, UserProjectRole, UserOrgRole,
                                      User)
from index import db


class OrganizationAPI(Resource):
    """Class to handle Organization related GET, POST and PUT API."""

    @token_required
    def post(self, session):
        """
        Post call to create Organization with name.

        Args:
            session(object): User session

        Returns: Standard API Response with HTTP status code

        """
        user_id = session.user_id
        user_obj = User.query.filter_by(user_id=user_id,
                                        is_deleted=False).first()

        create_org_parser = reqparse.RequestParser(bundle_errors=True)
        create_org_parser.add_argument(
            'org_name', help=APIMessages.PARSER_MESSAGE,
            required=True, type=str)
        create_org_parser.add_argument(
            'org_description', help=APIMessages.PARSER_MESSAGE,
            required=True, type=str)
        create_org_data = create_org_parser.parse_args()
        check_permission(user_obj)
        create_organization = Organization(create_org_data['org_name'],
                                           create_org_data['org_description'],
                                           session.user_id)
        create_organization.save_to_db()
        organization_data = {'org_id': create_organization.org_id,
                             'org_name': create_organization.org_name,
                             'org_description': create_organization.org_description}
        return api_response(
            True, APIMessages.CREATE_RESOURCE.format('Organization'),
            STATUS_CREATED, organization_data)

    @token_required
    def put(self, session):
        """
        PUT call to Update Organization name.

        Args:
            session(object): User session

        Returns: Standard API Response with HTTP status code

        """
        update_org_parser = reqparse.RequestParser(bundle_errors=True)
        update_org_parser.add_argument(
            'org_id', help=APIMessages.PARSER_MESSAGE,
            required=True, type=int, location='json')
        update_org_parser.add_argument(
            'org_name', help=APIMessages.PARSER_MESSAGE,
            required=True, type=str, location='json')
        update_org_parser.add_argument(
            'org_description', help=APIMessages.PARSER_MESSAGE,
            required=True, type=str, location='json')

        update_org_data = update_org_parser.parse_args()
        user_obj = User.query.filter_by(user_id=session.user_id,
                                        is_deleted=False).first()

        current_org = Organization.query.filter_by(
            org_id=update_org_data['org_id'], is_deleted=False).first()
        if not current_org:
            raise ResourceNotAvailableException(
                "Organization")
        check_permission(user_obj, list_of_permissions=ORGANIZATION_API_PUT,
                         org_id=current_org.org_id)
        current_org.org_name = update_org_data['org_name']
        current_org.org_description = update_org_data['org_description']
        current_org.save_to_db()
        return api_response(
            True, APIMessages.UPDATE_RESOURCE.format('Organization'),
            STATUS_OK)

    @token_required
    def get(self, session):
        """
        GET call to retrieve all Organizations.

        Args:
            session(object): User session

        Returns: Standard API Response with HTTP status code
        """
        # Storing all active projects in a list
        if session.user.is_super_admin:
            list_of_active_orgs = Organization.query.filter(
                Organization.is_deleted == False).all()
        else:
            org_id_from_org_role = db.session.query(UserOrgRole.org_id).filter(
                UserOrgRole.user_id == session.user_id).distinct().all()
            org_id_in_org_role = [org_id for org_id, in org_id_from_org_role]
            org_id_from_project_role = db.session.query(
                UserProjectRole.org_id).filter(
                UserProjectRole.user_id == session.user_id).distinct().all()
            org_id_in_project_role = [org_id for org_id, in
                                      org_id_from_project_role]
            active_org = org_id_in_org_role + org_id_in_project_role
            list_of_active_orgs = Organization.query.filter(
                Organization.org_id.in_(set(active_org)),
                Organization.is_deleted == False).all()
        if not list_of_active_orgs:
            return api_response(
                False, APIMessages.NO_RESOURCE.format('Organization'),
                STATUS_FORBIDDEN)
        # list of projects to be returned in the response
        org_details_to_return = list()
        for each_org in list_of_active_orgs:
            org_details_to_return.append(
                {'org_id': each_org.org_id,
                 'org_name': each_org.org_name,
                 'org_description': each_org.org_description})
        return api_response(
            True, APIMessages.SUCCESS, STATUS_OK,
            {"organization_details": org_details_to_return})

    @token_required
    def delete(self, session):
        """
        DELETE call to delete organization details.

        Args:
            session(object): User session

        Returns: Standard API Response with HTTP status code

        """
        projects = []
        user_associated = []
        get_org_parser = reqparse.RequestParser()
        get_org_parser.add_argument(
            'org_id', help=APIMessages.PARSER_MESSAGE,
            required=True, type=int)
        get_org_data = get_org_parser.parse_args()
        org_obj = Organization.query.filter_by(
            org_id=get_org_data['org_id'],
            is_deleted=False).first()
        if not org_obj:
            return api_response(False,
                                APIMessages.NO_RESOURCE.format('Organization'),
                                STATUS_UNAUTHORIZED)
        check_permission(user_object=session.user,
                         list_of_permissions=ORG_DELETE,
                         org_id=get_org_data['org_id'])
        project_obj = Project.query.filter_by(
            org_id=get_org_data["org_id"], is_deleted=False).order_by(
            Project.project_id).all()
        user_org_role_obj = UserOrgRole.query.filter_by(
            org_id=get_org_data["org_id"]).distinct(
            UserOrgRole.user_id).with_entities(
            UserOrgRole.user_id).all()
        if not project_obj and not user_org_role_obj:
            org_obj.is_deleted = True
            org_obj.save_to_db()
            return api_response(
                True, APIMessages.ORG_DELETED, STATUS_OK)
        else:
            for each_obj in project_obj:
                projects.append(
                    {"project_id": each_obj.project_id,
                     "project_name": each_obj.project_name})
            user_obj_list = User.query.filter(
                User.user_id.in_(user_org_role_obj)).order_by(
                User.user_id).all()
            for each_user in user_obj_list:
                user_associated.append({"user_id": each_user.user_id,
                                        "email_id": each_user.email})
            return api_response(
                False, APIMessages.DELETE_ORG_FALSE, STATUS_OK, {
                    "org_id": get_org_data['org_id'],
                    "project_name": org_obj.org_name,
                    "associated_project": projects,
                    "asociated_users": user_associated})


class DashBoardStatus(Resource):
    """ To handle GET API,to get count of active projects,users,jobs."""

    @token_required
    def get(self, session):
        """
        To get active projects,users and jobs for a particular org id.

        Returns:
            Standard API Response with message, data(count of active projects,
            users and jobs) and http status code.
        """
        get_org_parser = reqparse.RequestParser()
        get_org_parser.add_argument('org_id', required=True,
                                    type=int,
                                    location='args')
        get_org_parser.add_argument('start_time', required=False,
                                    type=str,
                                    location='args')
        get_org_parser.add_argument('end_time', required=False,
                                    type=str,
                                    location='args')
        org_detail = get_org_parser.parse_args()
        result_dic = {}

        org_obj = Organization.query.filter_by(
            org_id=org_detail["org_id"]).first()
        if not org_obj:
            raise ResourceNotAvailableException("org_id")
        check_permission(user_object=session.user,
                         list_of_permissions=DASH_BOARD_STATUS_GET,
                         org_id=org_detail["org_id"])
        result_dic["org_id"] = org_obj.org_id
        result_dic["org_name"] = org_obj.org_name

        project_obj = Project.query.filter_by(
            org_id=org_detail["org_id"]).all()
        list_project_id = [each_user_grp.project_id for each_user_grp in
                           project_obj]
        active_projects = len(project_obj)
        result_dic["active_projects"] = active_projects

        user_project_role_object = UserProjectRole.query.filter(
            UserProjectRole.org_id == org_detail['org_id']).distinct(
            UserProjectRole.user_id).all()

        user_org_role_object = UserOrgRole.query.filter(
            UserOrgRole.org_id == org_detail['org_id']).distinct(
            UserOrgRole.user_id).all()

        list_user_id_in_user_project_role_object = [each_user_grp.user_id
                                                    for each_user_grp in
                                                    user_project_role_object]
        list_user_id_in_user_org_role_object = [each_user_grp.user_id
                                                for each_user_grp in
                                                user_org_role_object]
        user_id_list = [list_user_id_in_user_project_role_object,
                        list_user_id_in_user_org_role_object]
        list_user_id = set().union(*user_id_list)

        result_dic["active_users"] = len(list_user_id)

        all_project_test_suite_id_list = []
        for project_id in list_project_id:
            test_suite_object = TestSuite.query.filter_by(
                project_id=project_id).all()
            list_test_suite_id = [each_user_grp.test_suite_id for
                                  each_user_grp
                                  in
                                  test_suite_object]

            all_project_test_suite_id_list.extend(list_test_suite_id)

        if (org_detail["start_time"] and org_detail["end_time"]):
            datetime_object_start = datetime.strptime(
                org_detail["start_time"],
                "%Y-%m-%d")
            datetime_object_end = datetime.strptime(
                org_detail["end_time"],
                "%Y-%m-%d")

            all_jobs = Job.query.filter(
                Job.test_suite_id.in_(all_project_test_suite_id_list),
                Job.modified_at >= datetime_object_start,
                Job.modified_at < datetime_object_end).all()
            result_dic["active_jobs"] = len(all_jobs)
            result_dic["start_time"] = str(datetime_object_start)
            result_dic["end_time"] = str(datetime_object_end)
        else:
            current_day = date.today()
            currentday = datetime.strptime(
                str(current_day), "%Y-%m-%d")
            current_month_first_day = date.today().replace(day=1)
            datetime_object_start = datetime.strptime(
                str(current_month_first_day), "%Y-%m-%d")
            end_date_obj = datetime.now() + timedelta(days=1)
            all_jobs = Job.query.filter(
                Job.test_suite_id.in_(all_project_test_suite_id_list),
                Job.modified_at >= datetime_object_start,
                Job.modified_at < end_date_obj).all()
            result_dic["active_jobs"] = len(all_jobs)
            result_dic["start_time"] = str(datetime_object_start)
            result_dic["end_time"] = str(currentday)

        return api_response(
            True, APIMessages.DATA_LOADED, STATUS_CREATED,
            result_dic)
