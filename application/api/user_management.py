"""File to handle User Management related APIs."""

import re

from flask_restful import reqparse, Resource

from application.common.api_permission import USER_API_GET, USER_ROLE_API_GET, \
    USER_ROLE_API_DELETE
from application.common.common_exception import (ResourceNotAvailableException,
                                                 GenericBadRequestException,
                                                 IllegalArgumentException)
from application.common.constants import APIMessages
from application.common.constants import GenericStrings
from application.common.response import (api_response, STATUS_OK,
                                         STATUS_CREATED, STATUS_BAD_REQUEST)
from application.common.token import (token_required)
from application.common.utils import generate_hash
from application.helper.permission_check import (check_valid_id_passed_by_user,
                                                 check_permission)
from application.model.models import (UserOrgRole, UserProjectRole, User,
                                      Project, Role, Session, Permission)
from index import db


class UserAPI(Resource):
    """API to handle User related calls."""

    @token_required
    def get(self, session):
        """
        API returns users present in given org.

        Args:
            session (object): Session Object

        Returns: API response with Users in org
        """
        parser = reqparse.RequestParser()
        parser.add_argument('org_id',
                            help=APIMessages.PARSER_MESSAGE,
                            required=True, type=int, location='args')
        user_api_parser = parser.parse_args()
        check_valid_id_passed_by_user(org_id=user_api_parser['org_id'])
        # TODO: Add a check to verify user management permission
        check_permission(user_object=session.user,
                         list_of_permissions=USER_API_GET,
                         org_id=user_api_parser["org_id"])
        user_project_role = UserProjectRole.query.filter(
            UserProjectRole.org_id == user_api_parser['org_id']).distinct(
            UserProjectRole.user_id).all()
        user_org_role = UserOrgRole.query.filter(
            UserOrgRole.org_id == user_api_parser['org_id']).distinct(
            UserOrgRole.user_id).all()
        user_id_list_in_project = [each_user.user_id for each_user in
                                   user_project_role]
        user_id_list_in_org = [each_user.user_id for each_user in
                               user_org_role]
        user_id_list = [user_id_list_in_org, user_id_list_in_project]
        unique_user_id_list = set().union(*user_id_list)
        all_user_details = User.query.filter(
            User.user_id.in_(unique_user_id_list)).order_by(User.user_id).all()
        final_data = []
        for each_user in all_user_details:
            temp_dict = dict()
            temp_dict['user_id'] = each_user.user_id
            temp_dict['first_name'] = each_user.first_name
            temp_dict['last_name'] = each_user.last_name
            temp_dict['email'] = each_user.email
            final_data.append(temp_dict)
        data = {"org_id": user_api_parser['org_id'],
                "users": final_data}
        return api_response(True, APIMessages.SUCCESS, STATUS_OK, data)


class UserRoleAPI(Resource):
    """Class to handle POST user role API."""

    @token_required
    def post(self, session):
        """
        Post to create UserProjectRole and UserOrgRole records.

        Args:
            session (object):

        Returns: Standard API Response with HTTP status code
        """
        parser = reqparse.RequestParser()
        parser.add_argument('org_id',
                            help=APIMessages.PARSER_MESSAGE,
                            required=True, type=int, location='json')
        parser.add_argument('user_id',
                            help=APIMessages.PARSER_MESSAGE,
                            required=False, type=int, location='json')
        parser.add_argument('email_id',
                            help=APIMessages.PARSER_MESSAGE,
                            required=False, type=str, location='json')
        parser.add_argument('project_role_list',
                            help=APIMessages.PARSER_MESSAGE,
                            required=True, type=list, location='json')
        parser.add_argument('org_allowed_role_list',
                            help=APIMessages.PARSER_MESSAGE,
                            required=True, type=list, location='json')
        parser.add_argument('first_name',
                            help=APIMessages.PARSER_MESSAGE,
                            required=False, type=str, location='json')
        parser.add_argument('last_name',
                            help=APIMessages.PARSER_MESSAGE,
                            required=False, type=str, location='json')
        create_role_api_parser = parser.parse_args()
        # check if user and org id is valid if user id is passed
        if create_role_api_parser['user_id']:
            check_valid_id_passed_by_user(
                org_id=create_role_api_parser['org_id'],
                user_id=create_role_api_parser['user_id'])
        # Check if org id is valid if user id is not passed
        if not create_role_api_parser['user_id']:
            check_valid_id_passed_by_user(
                org_id=create_role_api_parser['org_id'])

        # TODO: Check if user management permission exists
        # check if project ids passed are related to org
        list_of_projects_passed = []
        if create_role_api_parser['project_role_list']:
            list_of_projects_passed = \
                [each_project['project_id'] for each_project in
                 create_role_api_parser['project_role_list']]
        projects_under_given_org = Project.query.filter_by(
            org_id=create_role_api_parser['org_id'],
            is_deleted=False).all()
        list_projects_under_org = \
            [project.project_id for project in projects_under_given_org]
        if not (set(list_of_projects_passed).issubset(
                set(list_projects_under_org))):
            raise GenericBadRequestException(APIMessages.PROJECT_NOT_UNDER_ORG)
        # check if role Ids passed are related to passed org
        passed_roles_list = list()
        for each_project_and_role in create_role_api_parser[
            'project_role_list']:
            passed_roles_list.extend(
                each_project_and_role['allowed_role_list'])
        passed_roles_list.extend(
            create_role_api_parser['org_allowed_role_list'])

        # TODO: Need to enable & optimise check_permission
        # check_permission(user_object=session.user,
        #                  list_of_permissions=USER_ROLE_API_POST,
        #                  org_id=create_role_api_parser["org_id"])

        # get all roles under the given org
        valid_roles_under_org = Role.query.filter_by(
            org_id=create_role_api_parser['org_id']).all()
        valid_role_ids_under_org = \
            [each_role.role_id for each_role in valid_roles_under_org]
        if not set(passed_roles_list).issubset(valid_role_ids_under_org):
            raise GenericBadRequestException(APIMessages.ROLE_NOT_UNDER_ORG)

        # check if email is passed in request
        if create_role_api_parser['email_id'] and \
                not create_role_api_parser['user_id']:
            # get user_id based on email_id
            get_user_record = User.query.filter(
                User.email.ilike(
                    create_role_api_parser['email_id']),
                User.is_deleted == False).first()
            if get_user_record:
                # User record is present with given email id
                user_id = get_user_record.user_id
            else:
                # User record is not present for given email id.
                # Create a new user
                if not (re.search(GenericStrings.EMAIL_FORMAT_REGEX,
                                  create_role_api_parser['email_id'])):
                    raise GenericBadRequestException(
                        APIMessages.VALID_EMAIL)
                # First name and last name should not be None for New User.
                if create_role_api_parser['first_name'] is None or \
                        create_role_api_parser['last_name'] is None:
                    raise GenericBadRequestException(
                        APIMessages.FIRST_LAST_NAME)
                create_user_args = \
                    {'first_name': create_role_api_parser['first_name'],
                     'last_name': create_role_api_parser['last_name'],
                     'password': create_role_api_parser['email_id'],
                     'is_verified': True}
                user_id = create_new_user(
                    create_role_api_parser['email_id'], **create_user_args)
        if create_role_api_parser['user_id'] and \
                not create_role_api_parser['email_id']:
            user_id = create_role_api_parser['user_id']

        # Deleting all UserProjectRole records with given User and Org Id
        UserProjectRole.query.filter_by(
            org_id=create_role_api_parser['org_id'],
            user_id=user_id).delete()
        UserOrgRole.query.filter_by(
            org_id=create_role_api_parser['org_id'],
            user_id=user_id).delete()

        # add project roles
        if create_role_api_parser['project_role_list']:
            for each_project_role in \
                    create_role_api_parser['project_role_list']:
                for each_roles_given in \
                        set(each_project_role['allowed_role_list']):
                    add_user_project_role = UserProjectRole(
                        user_id=user_id,
                        org_id=create_role_api_parser['org_id'],
                        project_id=each_project_role['project_id'],
                        role_id=each_roles_given, owner_id=session.user_id)
                    add_user_project_role.save_to_db()

        # Add Org Roles
        if create_role_api_parser['org_allowed_role_list']:
            for each_org_role in \
                    set(create_role_api_parser['org_allowed_role_list']):
                new_user_org_role = UserOrgRole(
                    user_id=user_id,
                    org_id=create_role_api_parser['org_id'],
                    role_id=each_org_role, owner_id=session.user_id)
                new_user_org_role.save_to_db()
        return api_response(True, APIMessages.ADD_ROLE, STATUS_CREATED)

    @token_required
    def get(self, session):
        """
        GET call to retrieve UserProjectRole and UserOrgRole records.

        Args:
            session (object): User Session

        Returns: Standard API Response with HTTP status code
        """
        # TODO: Need to reduce DB hit
        parser = reqparse.RequestParser()
        parser.add_argument('org_id',
                            help=APIMessages.PARSER_MESSAGE,
                            required=True, type=int, location='args')
        parser.add_argument('user_id',
                            help=APIMessages.PARSER_MESSAGE,
                            required=False, type=int, location='args')
        parser.add_argument('email_id',
                            help=APIMessages.PARSER_MESSAGE,
                            required=False, type=str, location='args')
        get_role_api_parser = parser.parse_args()
        result_dict = {}

        # Checking if User Id or Email Id is mandatorily passed
        if not get_role_api_parser['user_id'] and \
                not get_role_api_parser['email_id']:
            return api_response(False, APIMessages.EMAIL_USER,
                                STATUS_BAD_REQUEST)
        if get_role_api_parser['user_id'] and get_role_api_parser['email_id']:
            raise GenericBadRequestException(APIMessages.ONLY_USER_OR_EMAIL)

        # checking if User Id is valid
        valid_org, valid_project, valid_user = None, None, None
        if get_role_api_parser['user_id']:
            valid_org, valid_project, valid_user = check_valid_id_passed_by_user(
                org_id=get_role_api_parser['org_id'],
                user_id=get_role_api_parser['user_id'])
        check_permission(user_object=session.user,
                         list_of_permissions=USER_ROLE_API_GET,
                         org_id=get_role_api_parser["org_id"])

        # Get user Id based on email Id passed
        if get_role_api_parser['email_id'] and \
                not get_role_api_parser['user_id']:
            valid_org, valid_project, valid_user = check_valid_id_passed_by_user(
                org_id=get_role_api_parser['org_id'])
            valid_user = User.query.filter(
                User.email.ilike(get_role_api_parser['email_id']),
                User.is_deleted == False).first()
            if not valid_user:
                return api_response(True, APIMessages.NO_ROLES,
                                    STATUS_OK)

        if get_role_api_parser['org_id'] and valid_user.user_id:
            # Get Project Role list
            project_role_list = list()
            temp_dict = {}
            user_project_roles = UserProjectRole.query.filter_by(
                org_id=get_role_api_parser['org_id'],
                user_id=valid_user.user_id).all()
            for each_project_role in user_project_roles:
                if each_project_role.project_id not in temp_dict.keys():
                    # Add a key with value as role_id
                    temp_dict[each_project_role.project_id] = \
                        [each_project_role.role_id]
                else:
                    temp_dict[each_project_role.project_id].append(
                        each_project_role.role_id)
            for key, value in temp_dict.items():
                project_role_list.append({'project_id': key,
                                          'allowed_role_list': value})
            result_dict['project_role_list'] = project_role_list
            # Get Org Roles
            user_org_roles = UserOrgRole.query.filter_by(
                org_id=get_role_api_parser['org_id'],
                user_id=valid_user.user_id).all()
            result_dict['is_org_user'] = True if user_org_roles else False
            result_dict['org_allowed_role_list'] = []
            if user_org_roles:
                for each_user_org_role in user_org_roles:
                    result_dict['org_allowed_role_list'].append(
                        each_user_org_role.role_id)
            if not (result_dict['org_allowed_role_list'] or result_dict[
                'project_role_list']):
                return api_response(True, APIMessages.NO_ROLES,
                                    STATUS_OK)

            result_dict['user_id'] = valid_user.user_id
            result_dict['email_id'] = valid_user.email
            result_dict['first_name'] = valid_user.first_name
            result_dict['last_name'] = valid_user.last_name
            result_dict['user_id'] = valid_user.user_id
            result_dict['org_id'] = get_role_api_parser['org_id']

            return api_response(True, APIMessages.SUCCESS, STATUS_OK,
                                result_dict)

    @token_required
    def delete(self, session):
        """
               DELETE call to delete UserProjectRole and UserOrgRole records.

               Args:
                   session (object): User Session

               Returns: Standard API Response with HTTP status code
        """
        parser = reqparse.RequestParser()
        parser.add_argument('org_id',
                            help=APIMessages.PARSER_MESSAGE,
                            required=True, type=int, location='args')
        parser.add_argument('user_id',
                            help=APIMessages.PARSER_MESSAGE,
                            required=False, type=int, location='args')
        parser.add_argument('email_id',
                            help=APIMessages.PARSER_MESSAGE,
                            required=False, type=str, location='args')
        delete_role_api_parser = parser.parse_args()
        result_dict = {}
        # Checking if User Id or Email Id is mandatorily passed
        if not delete_role_api_parser['user_id'] and \
                not delete_role_api_parser['email_id']:
            return api_response(False, APIMessages.EMAIL_USER,
                                STATUS_BAD_REQUEST)
        if delete_role_api_parser['user_id'] and delete_role_api_parser[
            'email_id']:
            raise GenericBadRequestException(APIMessages.ONLY_USER_OR_EMAIL)
        # Storing user id if user id is passed
        user_id = delete_role_api_parser['user_id'] \
            if delete_role_api_parser['user_id'] else None
        # checking if User Id is valid
        if delete_role_api_parser['user_id']:
            check_valid_id_passed_by_user(
                org_id=delete_role_api_parser['org_id'],
                user_id=delete_role_api_parser['user_id'])
        check_permission(user_object=session.user,
                         list_of_permissions=USER_ROLE_API_DELETE,
                         org_id=delete_role_api_parser["org_id"])
        # Get user Id based on email Id passed
        if delete_role_api_parser['email_id'] and \
                not delete_role_api_parser['user_id']:
            check_valid_id_passed_by_user(
                org_id=delete_role_api_parser['org_id'])
            user_record = User.query.filter(
                User.email.ilike(delete_role_api_parser['email_id']),
                User.is_deleted == False).first()
            if not user_record:
                raise ResourceNotAvailableException("User")
            user_id = user_record.user_id
            result_dict['email_id'] = user_record.email
        user_project_role_obj = UserProjectRole.query.filter(
            UserProjectRole.org_id == delete_role_api_parser["org_id"],
            UserProjectRole.user_id == user_id).all()
        user_org_role_obj = UserOrgRole.query.filter(
            UserOrgRole.org_id == delete_role_api_parser["org_id"],
            UserOrgRole.user_id == user_id).all()
        session_obj = Session.query.filter(
            Session.user_id == user_id).all()
        for each_project_org_session_role in (
                user_project_role_obj, user_org_role_obj, session_obj):
            for each_role in each_project_org_session_role:
                db.session.delete(each_role)
        db.session.commit()
        return api_response(True,
                            APIMessages.USER_ROLE_DELETED.format(
                                delete_role_api_parser["org_id"]),
                            STATUS_CREATED)


def create_new_user(email_id, **kwargs):
    """
    Method to create New User based on email_id and other args.

    Args:
        email_id (str): email Id
        **kwargs (dict): pass required arguments for User table

    Returns: User Id created from User Table
    """
    new_user_record = User(
        email=email_id.lower(), first_name=kwargs['first_name'],
        last_name=kwargs['last_name'],
        password_hash=generate_hash(kwargs['password']),
        is_verified=kwargs['is_verified'])
    new_user_record.save_to_db()
    return new_user_record.user_id


class UserProfileAPI(Resource):
    """ API to handle GET,PUT calls for getting and updating current user
    details."""

    @token_required
    def get(self, session):
        """
        Method to return current user details.

        Args:
            session (object): Session Object

        Returns: Standard API Response with message(returns message saying
        success), data and http status code.
        """
        user_dict = {}
        user_dict["email_id"] = session.user.email
        user_dict["first_name"] = session.user.first_name
        user_dict["last_name"] = session.user.last_name
        return api_response(True,
                            APIMessages.SUCCESS,
                            STATUS_CREATED, user_dict)

    @token_required
    def put(self, session):
        """
        Method to update user details into the DB.

        Args:
            session (object):By using this object we can get the user_id.

        Returns:
            Standard API Response with message(returns message user details
            updated successfully), data and http status code.
        """

        user_parser = reqparse.RequestParser(bundle_errors=True)
        user_parser.add_argument('first_name', type=str, location='json')
        user_parser.add_argument('last_name', type=str, location='json')
        user_details = user_parser.parse_args()
        for key, value in dict(user_details).items():
            if value == None:
                del user_details[key]
        for key, value in dict(user_details).items():
            user_details[key] = value.strip()
        current_user_obj = User.query.filter(
            User.user_id == session.user_id).first()
        for key, value in user_details.items():
            if key == "first_name":
                if value == "":
                    return api_response(False, APIMessages.PASS_FIRST_NAME,
                                        STATUS_BAD_REQUEST)
                if len(value) > 50:
                    raise IllegalArgumentException(
                        APIMessages.INVALID_LENGTH.format("50"))
                current_user_obj.first_name = value
            if key == "last_name":
                if value == "":
                    return api_response(False, APIMessages.PASS_LAST_NAME,
                                        STATUS_BAD_REQUEST)
                if len(value) > 50:
                    raise IllegalArgumentException(
                        APIMessages.INVALID_LENGTH.format("50"))
                current_user_obj.last_name = value
        current_user_obj.save_to_db()
        return api_response(
            True, APIMessages.USER_DETAILS_UPDATED, STATUS_CREATED)


class DefaultProjectOrg(Resource):
    """ API to handle PUT call,to update default project and organization"""

    @token_required
    def put(self, session):
        """
        Method to update default project and organization in user table.

        Args:
            session (object):By using this object we can get the user_id.

        Returns:
            Standard API Response with message(returns message default
            organization and project set successfully), data and http
            status code.
        """

        project_parser = reqparse.RequestParser(bundle_errors=True)
        project_parser.add_argument('project_id', type=int, required=True)
        project_details = project_parser.parse_args()
        project_obj = Project.query.filter(
            Project.project_id == project_details["project_id"],
            Project.is_deleted == False).first()
        if not project_obj:
            raise ResourceNotAvailableException("Project")
        current_user_obj = User.query.filter(
            User.user_id == session.user_id).first()
        default_org_project = {}
        default_org_project["default_org_id"] = project_obj.org_id
        default_org_project["default_project_id"] = project_details[
            "project_id"]
        current_user_obj.asset = default_org_project
        current_user_obj.save_to_db()
        return api_response(
            True, APIMessages.SET_SUCCESS, STATUS_CREATED)


class PermissionDetail(Resource):
    """ API to handle GET call for getting all permission names."""

    @token_required
    def get(self, session):
        """
        Method to return all permission names.

        Args:
            session (object): Session Object

        Returns: Standard API Response with message(returns message saying
        success), data and http status code.
        """
        # TODO : Add Check Permission and give proper permissions.
        permission_dict = {}
        all_permissions = db.session.query(
            Permission.permission_name).distinct().all()
        permission_list = [permission for permission, in all_permissions]
        permission_dict["permissions"] = permission_list
        return api_response(True,
                            APIMessages.SUCCESS,
                            STATUS_CREATED, permission_dict)
