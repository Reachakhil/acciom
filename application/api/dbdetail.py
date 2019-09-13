"""File to handle Database connection operations."""

from datetime import datetime

from flask_restful import Resource, reqparse, inputs

from application.common.constants import APIMessages, SupportedDBType
from application.common.response import (api_response, STATUS_BAD_REQUEST,
                                         STATUS_CREATED, STATUS_OK,
                                         STATUS_CONFLICT)
from application.common.token import token_required
from application.common.utils import validate_empty_fields
from application.helper.encrypt import encrypt
from application.helper.permission_check import check_permission
from application.model.models import (DbConnection, Project, Organization,
                                      TestCase)
from index import db


class DbDetails(Resource):
    """
    Class to handle GET, POST, PUT APIs.

    Helper Methods for storing, getting, and Updating DB Details.
    """

    @token_required
    def post(self, session):
        """
        Method to store the Database Details provided by the user into the DB.

        Args:
             session (object):By using this object we can get the user_id.

        Returns:
            Standard API Response with message(returns message saying
            that db details added successfully), data and http status code.
        """
        post_db_detail_parser = reqparse.RequestParser(bundle_errors=True)
        post_db_detail_parser.add_argument('project_id', required=True,
                                           type=int,
                                           help=APIMessages.PARSER_MESSAGE)
        post_db_detail_parser.add_argument('db_connection_name',
                                           required=False, type=str,
                                           help=APIMessages.PARSER_MESSAGE)
        post_db_detail_parser.add_argument('db_type', required=True,
                                           type=str,
                                           help=APIMessages.PARSER_MESSAGE)
        post_db_detail_parser.add_argument('db_name', required=True,
                                           type=str,
                                           help=APIMessages.PARSER_MESSAGE)
        post_db_detail_parser.add_argument('db_hostname', required=True,
                                           type=str,
                                           help=APIMessages.PARSER_MESSAGE)
        post_db_detail_parser.add_argument('db_username', required=True,
                                           type=str,
                                           help=APIMessages.PARSER_MESSAGE)
        post_db_detail_parser.add_argument('db_password', required=True,
                                           type=str,
                                           help=APIMessages.PARSER_MESSAGE)
        db_detail = post_db_detail_parser.parse_args()
        project_id = db_detail["project_id"]
        project_obj = Project.query.filter(
            Project.project_id == db_detail["project_id"],
            Project.is_deleted == False).first()
        if not project_obj:
            return api_response(False, APIMessages.PROJECT_NOT_EXIST,
                                STATUS_BAD_REQUEST)
        for key, value in dict(db_detail).items():
            db_detail[key] = str(value).strip()
        list_of_args = [arg.name for arg in post_db_detail_parser.args]
        request_data_validation = validate_empty_fields(db_detail,
                                                        list_of_args)
        if request_data_validation:
            return api_response(success=False,
                                message=request_data_validation,
                                http_status_code=STATUS_BAD_REQUEST,
                                data={})
        check_permission(session.user, ["add_db_details"],
                         project_obj.org_id, db_detail["project_id"])
        # check whether combination of db_type,db_name,db_username,
        # db_hostname,project_id is already present in db or not
        temp_connection = DbConnection.query.filter(
            DbConnection.project_id == project_id,
            DbConnection.db_type == SupportedDBType().get_db_id_by_name(
                db_detail['db_type']),
            DbConnection.db_name == db_detail['db_name'],
            DbConnection.db_hostname.ilike(
                db_detail['db_hostname']),
            DbConnection.db_username == db_detail['db_username'],
            DbConnection.is_deleted == False).first()
        if temp_connection:
            return api_response(False, APIMessages.
                                DB_DETAILS_ALREADY_PRESENT,
                                STATUS_BAD_REQUEST)
        else:
            # Check Db connection name already exist in db or not
            temp_connection = DbConnection.query.filter(
                DbConnection.db_connection_name == db_detail[
                    "db_connection_name"],
                DbConnection.project_id == project_id,
                DbConnection.is_deleted == False).first()
            if temp_connection:
                return api_response(False, APIMessages.
                                    DB_CONNECTION_NAME_ALREADY_PRESENT,
                                    STATUS_BAD_REQUEST)
            # Checking spaces in username and hostname
            spacecount_dbusername = db_detail["db_username"].find(" ")
            spacecount_dbhostanme = db_detail["db_hostname"].find(" ")
            if spacecount_dbusername > -1 or spacecount_dbhostanme > -1:
                return api_response(False, APIMessages.
                                    NO_SPACES,
                                    STATUS_BAD_REQUEST)
            if SupportedDBType().get_db_id_by_name(
                    db_detail['db_type']) is None:
                return api_response(success=False,
                                    message=APIMessages.DB_TYPE_NAME,
                                    http_status_code=STATUS_BAD_REQUEST,
                                    data={})
            db_password = encrypt(db_detail["db_password"])
            new_db = DbConnection(project_id=project_id,
                                  owner_id=session.user_id,
                                  db_connection_name=db_detail[
                                      'db_connection_name'],
                                  db_type=SupportedDBType().
                                  get_db_id_by_name(
                                      db_detail['db_type']),
                                  db_name=db_detail['db_name'],
                                  db_hostname=db_detail["db_hostname"],
                                  db_username=db_detail["db_username"],
                                  db_encrypted_password=db_password, )
            new_db.save_to_db()
            return api_response(True, APIMessages.DB_DETAILS_ADDED,
                                STATUS_CREATED)

    @token_required
    def get(self, session):
        """
        Method to fetch all connections for the given project_id.

        or particular connection for the db id

        Args:
            session (object):By using this object we can get the user_id.

        Returns:
            Standard API Response with message, data(returns dbdetails for the
            user passed id) and http status code.
        """
        get_db_detail_parser = reqparse.RequestParser()
        get_db_detail_parser.add_argument('project_id', required=False,
                                          type=int,
                                          location='args')
        get_db_detail_parser.add_argument('db_connection_id', required=False,
                                          type=int,
                                          location='args')
        database_id = get_db_detail_parser.parse_args()
        db_connection_id = database_id.get("db_connection_id")
        if db_connection_id:
            db_obj = DbConnection.query.filter(
                DbConnection.db_connection_id == db_connection_id,
                DbConnection.is_deleted == False).first()
            if not db_obj:
                return api_response(False,
                                    APIMessages.DBID_NOT_IN_DB.format(
                                        db_connection_id),
                                    STATUS_BAD_REQUEST)
            project_id_org_id = db.session.query(
                Organization.org_id,
                Project.project_id).filter(
                Organization.is_deleted == False).join(
                Project,
                Organization.org_id == Project.org_id).filter(
                Project.project_id == db_obj.project_id,
                Project.is_deleted == False
            ).first()
            if project_id_org_id == () or project_id_org_id == None:
                return api_response(False,
                                    APIMessages.NO_DB_ID,
                                    STATUS_BAD_REQUEST)
            check_permission(session.user, ["view_db_details"],
                             project_id_org_id[0],
                             project_id_org_id[1])
            return api_response(
                True, APIMessages.DATA_LOADED, STATUS_CREATED,
                {'project_id': db_obj.project_id,
                 'db_connection_name': db_obj.db_connection_name,
                 'db_connection_id': db_obj.db_connection_id,
                 'db_type': SupportedDBType().get_db_name_by_id(
                     db_obj.db_type),
                 'db_type_id': db_obj.db_type,
                 "db_name": db_obj.db_name,
                 'db_hostname': db_obj.db_hostname,
                 'db_username': db_obj.db_username,
                 })
        dbproject_id = get_db_detail_parser.parse_args()
        project_id = dbproject_id.get("project_id")
        if project_id:
            project_obj = DbConnection.query.filter(
                DbConnection.project_id == project_id,
                DbConnection.is_deleted == False).first()
            project_name_obj = Project.query.filter_by(
                project_id=project_id).first()

            if not project_name_obj:
                return api_response(False,
                                    APIMessages.PROJECT_NOT_EXIST,
                                    STATUS_BAD_REQUEST)
            check_permission(session.user, ["view_db_details"],
                             project_name_obj.org_id, project_id)

            def to_json(projectid):
                return {
                    'project_id': projectid.project_id,
                    'project_name': project_name_obj.project_name,
                    'db_connection_name': projectid.db_connection_name,
                    'db_connection_id': projectid.db_connection_id,
                    'db_type':
                        SupportedDBType().get_db_name_by_id(
                            projectid.db_type),
                    'db_type_id': projectid.db_type,
                    'db_name': projectid.db_name,
                    'db_hostname': projectid.db_hostname,
                    'db_username': projectid.db_username}

            db_detail_dic = {}
            db_list = DbConnection.query.filter_by(
                project_id=project_id).order_by(
                DbConnection.created_at).all()
            db_connection_list = [each_db for each_db in db_list if
                                  each_db.is_deleted == False]
            db_detail_dic["db_details"] = list(
                map(lambda db_connection_id: to_json(db_connection_id),
                    db_connection_list))
            return api_response(True, APIMessages.DATA_LOADED,
                                STATUS_CREATED,
                                db_detail_dic)
        else:
            return api_response(False,
                                APIMessages.PASS_DBID_or_PROJECTID,
                                STATUS_BAD_REQUEST)

    @token_required
    def put(self, session):
        """
        Method to Update database details into the DB based on the db id.

        provided by the user.

        Args:
            session (object):By using this object we can get the user_id.

        Returns:
            Standard API Response with message(returns message db details
            uploaded successfully), data and http status code.
        """

        put_db_detail_parser = reqparse.RequestParser(bundle_errors=True)
        put_db_detail_parser.add_argument('db_connection_id', required=True,
                                          type=int)
        put_db_detail_parser.add_argument('db_connection_name', type=str)
        put_db_detail_parser.add_argument('db_type', type=str)
        put_db_detail_parser.add_argument('db_name', type=str)
        put_db_detail_parser.add_argument('db_hostname', type=str)
        put_db_detail_parser.add_argument('db_username', type=str)
        put_db_detail_parser.add_argument('db_password', type=str)
        db_detail = put_db_detail_parser.parse_args()
        db_details = put_db_detail_parser.parse_args()
        db_connection_id = db_detail["db_connection_id"]
        # Remove keys which contain None values in db_details dictionary
        del db_detail["db_connection_id"]
        for key, value in dict(db_detail).items():
            if value == None:
                del db_detail[key]
        for key, value in dict(db_detail).items():
            db_detail[key] = value.strip()
        if not db_connection_id:
            return api_response(False, APIMessages.ABSENCE_OF_DBID,
                                STATUS_BAD_REQUEST)
        db_obj = DbConnection.query.filter(
            DbConnection.db_connection_id == db_connection_id,
            DbConnection.is_deleted == False).first()
        if not db_obj:
            return api_response(False,
                                APIMessages.DBID_NOT_IN_DB.format(
                                    db_connection_id),
                                STATUS_BAD_REQUEST)
        project_id = db_obj.project_id
        project_id_org_id = db.session.query(
            Organization.org_id,
            Project.project_id).filter(
            Organization.is_deleted == False).join(
            Project,
            Organization.org_id == Project.org_id).filter(
            Project.project_id == db_obj.project_id,
            Project.is_deleted == False
        ).first()
        if project_id_org_id == () or project_id_org_id == None:
            return api_response(False,
                                APIMessages.NO_DB_ID,
                                STATUS_BAD_REQUEST)
        check_permission(session.user, ["edit_db_details"],
                         project_id_org_id[0],
                         project_id_org_id[1])
        # Updating values present in database with user given values
        data_base_dict = db_obj.__dict__
        data_base_dict.update(db_detail)
        # check passed db type name is valid or not
        if db_details["db_type"] != None:
            if SupportedDBType().get_db_id_by_name(
                    db_detail['db_type']) is None:
                return api_response(success=False,
                                    message=APIMessages.DB_TYPE_NAME,
                                    http_status_code=STATUS_BAD_REQUEST,
                                    data={})
        # check whether combination of db_type,db_name,db_username,
        # db_hostname,project_id is already present in db or not
        if db_details["db_type"] != None:
            data_base_dict[
                'db_type'] = SupportedDBType().get_db_id_by_name(
                data_base_dict['db_type'])
        db_obj = DbConnection.query.filter(
            DbConnection.db_connection_id != db_connection_id,
            DbConnection.db_type == data_base_dict['db_type'],
            DbConnection.db_name == data_base_dict['db_name'],
            DbConnection.db_username == data_base_dict[
                'db_username'],
            DbConnection.db_hostname.ilike(
                data_base_dict['db_hostname']),
            DbConnection.project_id == data_base_dict[
                'project_id'], DbConnection.is_deleted == False).all()
        if db_obj != []:
            return api_response(False, APIMessages.
                                DB_DETAILS_ALREADY_PRESENT,
                                STATUS_BAD_REQUEST)
        else:
            # Check Db connection name already exist in db or not
            if db_details["db_connection_name"] != None:
                db_obj = DbConnection.query.filter(
                    DbConnection.db_connection_id != db_connection_id,
                    DbConnection.db_connection_name == db_detail[
                        "db_connection_name"],
                    DbConnection.project_id == project_id,
                    DbConnection.is_deleted == False).first()
                if db_obj:
                    return api_response(False, APIMessages.
                                        DB_CONNECTION_NAME_ALREADY_PRESENT,
                                        STATUS_BAD_REQUEST)
            # Checking spaces in username and hostname
            if db_details["db_username"] != None:
                spacecount_dbusername = db_detail[
                    "db_username"].find(" ")
                if spacecount_dbusername > -1:
                    return api_response(False, APIMessages.
                                        NO_SPACES,
                                        STATUS_BAD_REQUEST)
            if db_details["db_hostname"] != None:
                spacecount_dbhostname = db_detail[
                    "db_hostname"].find(" ")
                if spacecount_dbhostname > -1:
                    return api_response(False, APIMessages.
                                        NO_SPACES, STATUS_BAD_REQUEST)
            db_obj = DbConnection.query.filter(
                DbConnection.db_connection_id == db_connection_id,
                DbConnection.is_deleted == False).first()
            for key, value in db_detail.items():
                if key == 'db_password':
                    if value == "":
                        return APIMessages.PASSWORD_CANNOT_EMPTY
                    db_password = encrypt(value)
                    db_obj.db_encrypted_password = db_password
                elif key == 'db_connection_name':
                    if value == "":
                        now = datetime.now()
                        date_time_now = now.strftime("%d-%m-%Y %H:%M:%S")
                        value = APIMessages.CONNECTION + date_time_now
                    db_obj.db_connection_name = value
                    db_obj.save_to_db()
                elif key == 'db_type':
                    db_obj.db_type = SupportedDBType(). \
                        get_db_id_by_name(value)
                elif key == 'db_name':
                    if value == "":
                        return APIMessages.DB_NAME_CANNOT_EMPTY
                    db_obj.db_name = value
                elif key == 'db_hostname':
                    if value == "":
                        return APIMessages.HOSTNAME_CANNOT_EMPTY
                    db_obj.db_hostname = value
                elif key == 'db_username':
                    if value == "":
                        return APIMessages.USERNAME_CANNOT_EMPTY
                    db_obj.db_username = value
            db_obj.save_to_db()
            return api_response(
                True, APIMessages.DB_DETAILS_UPDATED.format(
                    db_connection_id), STATUS_CREATED)

    @token_required
    def delete(self, session):
        """
        To delete the data base for the user provided data base id.

        Args:
            session (object):By using this object we can get the user_id.

        Returns:
            Standard API Response with message(returns message saying
            that Data Base Deleted Successfully) and http status code.
        """
        delete_db_detail_parser = reqparse.RequestParser()
        delete_db_detail_parser.add_argument('db_connection_id',
                                             required=True,
                                             type=int,
                                             location='args')
        delete_db_detail_parser.add_argument('verify_delete',
                                             required=False,
                                             type=inputs.boolean,
                                             location='args',
                                             default=False)
        deletedata = delete_db_detail_parser.parse_args()
        data_base_id = deletedata.get("db_connection_id")
        if not data_base_id:
            return api_response(False,
                                APIMessages.PASS_DB_ID,
                                STATUS_BAD_REQUEST)
        del_obj = DbConnection.query.filter(
            DbConnection.db_connection_id == data_base_id,
            DbConnection.is_deleted == False).first()
        if not del_obj:
            return api_response(False,
                                APIMessages.DBID_NOT_IN_DB.format(
                                    data_base_id),
                                STATUS_BAD_REQUEST)
        project_id_org_id = db.session.query(
            Organization.org_id,
            Project.project_id).filter(Organization.is_deleted == False).join(
            Project,
            Organization.org_id == Project.org_id).filter(
            Project.project_id == del_obj.project_id,
            Project.is_deleted == False
        ).first()
        if project_id_org_id == () or project_id_org_id == None:
            return api_response(False,
                                APIMessages.NO_DB_ID,
                                STATUS_BAD_REQUEST)
        check_permission(session.user, ["delete_db_details"],
                         project_id_org_id[0],
                         project_id_org_id[1])

        # check whether passed db conection id is associated with any testcases
        data_base_ids = db.session.query(
            TestCase.test_case_detail["src_db_id"],
            TestCase.test_case_detail["target_db_id"]).filter(
            TestCase.is_deleted == False).all()
        idset = set()
        for tupleid in data_base_ids:
            for id in tupleid:
                idset.add(id)
        if data_base_id in idset:
            return api_response(False, APIMessages.DELETE_DB_WARNING,
                                STATUS_CONFLICT)
        if deletedata["verify_delete"] is True:
            del_obj.is_deleted = True
            del_obj.save_to_db()
            return api_response(True,
                                APIMessages.DB_DELETED.format(
                                    data_base_id),
                                STATUS_CREATED)
        else:
            return api_response(True,
                                APIMessages.DELETE_DB_VERIFY_DELETE.format(
                                    data_base_id), STATUS_OK)


class SupportedDBTypes(Resource):
    """Class to get available database types"""

    @token_required
    def get(self, session):
        """
        this method returns list of all the available database types supported
        in the Acciom
        Args:
            session: to get the User Id

        Returns: list of all the available database types supported
        in the Acciom

        """
        supported_db_type_list = []
        supported_db_type_dict = {}
        x = SupportedDBType()
        for i in x.supported_db_type:
            supported_db_type_dict = {}
            supported_db_type_dict[i] = x.supported_db_type[i]
            supported_db_type_list.append(supported_db_type_dict)
        payload = {"data": supported_db_type_list}

        return api_response(True, APIMessages.RETURN_SUCCESS,
                            STATUS_CREATED, payload)
