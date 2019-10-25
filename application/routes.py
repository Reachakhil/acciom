"""File to handle API routes."""
import os

from flask import send_from_directory

from application.api.checkconnection import CheckConnection
from application.api.connectiondetail import (SelectConnection, DbConnection,
                                              CaseDetails)
from application.api.dashboard import SideBarMenu
from application.api.data_quality_index import (ProjectDQI, OrganizationDQI,
                                                ProjectDQIHistory)
from application.api.dbdetail import DbDetails, SupportedDBTypes, \
    SupportedTestClasses
from application.api.login import (Login, LogOut, AddUser, ForgotPassword,
                                   ForgotPasswordVerifyToken, ResetPassword,
                                   GetToken, ChangePassword)
from application.api.menu import MenuAPI
from application.api.organization import (OrganizationAPI, DashBoardStatus)
from application.api.project import ProjectAPI
from application.api.query_analyser import (QueryAnalyser, QueryExporter)
from application.api.role import RoleAPI
from application.api.testcase import (TestCaseJob, TestCaseSparkJob,
                                      EditTestCase, TestCaseJobExternal)
from application.api.testsuite import (TestSuiteAPI, TestCaseLogDetail,
                                       ExportTestLog, TestCaseLogAPI,
                                       AddTestSuiteManually,
                                       CreateNewTestSuite)
from application.api.user_management import (UserAPI, UserRoleAPI,
                                             UserProfileAPI, DefaultProjectOrg,
                                             PermissionDetail)
from application.common.common_exception import (UnauthorizedException,
                                                 ResourceNotAvailableException,
                                                 GenericBadRequestException,
                                                 IllegalArgumentException)
from application.common.constants import APIMessages
from application.common.response import (api_response, STATUS_FORBIDDEN,
                                         STATUS_SERVER_ERROR,
                                         STATUS_BAD_REQUEST)
from application.model.models import db
from index import (app, api, static_folder)

db


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
    Serve HTML/React Static content i.e. HTML, CSS, JS, image, font files.

    Args:
        path(str): path for acciom_ui folder or resource in case of backend api

    Returns: return HTML/React Static content i.e. HTML, CSS, JS file

    """
    if path != "" and os.path.exists(
            static_folder + path):  # for UI path ex: /login, /register
        return send_from_directory(static_folder, path)
    elif not (os.path.exists(static_folder + path) or (
            str(path).startswith(
                "api/"))):  # for Backend Path ex: /api/register
        return send_from_directory(static_folder, 'index.html')
    elif path == "":
        return send_from_directory(static_folder, 'index.html')


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle Generic Exception."""
    return api_response(False, APIMessages.INTERNAL_ERROR, STATUS_SERVER_ERROR,
                        {'error_log': str(e)})


@app.errorhandler(UnauthorizedException)
def handle_unauthorized_exception(e):
    """Handle Unauthorized Access Exception."""
    return api_response(False, APIMessages.FORBIDDEN, STATUS_FORBIDDEN)


@app.errorhandler(ResourceNotAvailableException)
def handle_resource_not_available_exception(e):
    """Handle Resource Not Available Exception."""
    return api_response(
        False, APIMessages.NO_RESOURCE.format(e), STATUS_BAD_REQUEST)


@app.errorhandler(GenericBadRequestException)
def handle_bad_request_exception(e):
    """Handle Generic Bad Request Exception."""
    return api_response(False, str(e), STATUS_BAD_REQUEST)


@app.errorhandler(IllegalArgumentException)
def handle_bad_request_exception(e):
    """Handle  Illegal Argument Exception."""
    return api_response(False, str(e), STATUS_BAD_REQUEST)


@app.errorhandler(IllegalArgumentException)
def handle_bad_request_exception(e):
    """Handle  Illegal Argument Exception."""
    return api_response(False, str(e), STATUS_BAD_REQUEST)


api.add_resource(Login, '/api/login')
api.add_resource(LogOut, '/api/logout')
api.add_resource(AddUser, '/api/register')
api.add_resource(TestSuiteAPI, '/api/test-suite')
api.add_resource(TestCaseLogAPI, '/api/each-case-detail')
api.add_resource(TestCaseJob, '/api/test-case-job')
api.add_resource(TestCaseSparkJob,
                 '/api/spark-job-status/<int:test_case_log_id>')
api.add_resource(TestCaseLogDetail,
                 '/api/test-case-log')
api.add_resource(ExportTestLog, '/api/export')
api.add_resource(ProjectAPI, '/api/project')
api.add_resource(OrganizationAPI, '/api/organization/')
api.add_resource(DbDetails, '/api/db-detail')
api.add_resource(CheckConnection, '/api/check-connection')
api.add_resource(DbConnection, '/api/db-connection-detail')
api.add_resource(CaseDetails, '/api/test-case-detail')
api.add_resource(EditTestCase, '/api/edit-test-case')
api.add_resource(SelectConnection, '/api/select-connection')
api.add_resource(SideBarMenu, '/api/sidebar-menu')
api.add_resource(ProjectDQI, '/api/project-data-quality-index')
api.add_resource(OrganizationDQI, '/api/organization-data-quality-index')
api.add_resource(DashBoardStatus, '/api/dash-board-status')
api.add_resource(RoleAPI, '/api/role')
api.add_resource(ForgotPassword, '/api/forgot-password')
api.add_resource(ForgotPasswordVerifyToken,
                 '/api/forgot-password-verify-token')
api.add_resource(ResetPassword, '/api/reset-password')
api.add_resource(GetToken, '/api/generate-token')
api.add_resource(TestCaseJobExternal, '/api/test-case-job-external')
api.add_resource(ChangePassword, '/api/change-password')
api.add_resource(UserAPI, '/api/user')
api.add_resource(UserRoleAPI, '/api/user-role')
api.add_resource(ProjectDQIHistory, '/api/project-dqi-history')
api.add_resource(MenuAPI, '/api/menu')
api.add_resource(AddTestSuiteManually, '/api/add-test-suite-manually')
api.add_resource(CreateNewTestSuite, '/api/create-new-test-suite')
api.add_resource(SupportedDBTypes, '/api/supported-database-type')
api.add_resource(QueryAnalyser, '/api/query-analyser')
api.add_resource(QueryExporter, '/api/query-exporter')
api.add_resource(SupportedTestClasses, '/api/supported-test-class-type')
api.add_resource(UserProfileAPI, '/api/user-profile')
api.add_resource(DefaultProjectOrg, '/api/default-project-org')
api.add_resource(PermissionDetail, '/api/permission')
