"""File to store all constants."""


class APIMessages:
    """Messages to be sent in API Responses."""

    EMPTY_FIELD = "{} field cannot be blank"
    USER_EXISTS = "User with email as {} already exists"
    VERIFY_EMAIL = "Please verify your email address"
    USER_CREATED = "User with email as {} was created"
    INTERNAL_ERROR = "An Internal Server Error has occurred"
    USER_NOT_EXIST = "User with email as {} does not exist"
    INVALID_UID_PWD = "Please enter valid Username and Password"
    VERIFY_USER = "User verification is pending. Please verify through email"
    USER_LOGIN = "Logged in as {}"
    RESET_REQUEST = "Password Reset Request"
    RESET_EMAIL = "Reset Email was sent to your email"
    INVALID_TOKEN = "Invalid Token"
    RESET_PAGE = "Page for Password Reset"
    PASSWORD_CHANGE = "Password was successfully changed"
    USER_VERIFIED = "User Verification is completed"
    INVALID_PASSWORD = "The Old password you have entered is Invalid"
    NEW_TOKEN = "Access Token is generated"
    INVALID_EMAIL_PASSWORD = "Email or Password Password."
    DELETED_USER = "Please contact Admin, your account is not active."
    ADD_DATA = "Test suite uploaded successfully"
    RETURN_SUCCESS = "success"
    JOB_SUBMIT = "Job submitted successfully"
    PARSER_MESSAGE = "field is required"
    CREATE_RESOURCE = "{} is successfully created"
    UPDATE_RESOURCE = "{} is updated successfully"
    SUCCESS = "success"
    NO_RESOURCE = "{} is not available"
    DB_DETAILS_ADDED = "DbDetails added successfully"
    DATA_LOADED = "Data loaded successfully"
    DBID_NOT_IN_DB = "DB details for DB ID {},does not exist"
    DB_DETAILS_UPDATED = "DB details updated for connection id {} successfully"
    ABSENCE_OF_DBID = "Please pass DB Connection ID"
    CONNECTION_CREATE = "Connection can be created"
    CONNECTION_CANNOT_CREATE = "Connection could not be created, {}"
    NO_DB_UNDER_PROJECT = "No db details exist under this project id"
    PASS_DBID_or_PROJECTID = "Please pass db id or project id"
    TEST_CASE_DELETED = "Test case with test case id {} deleted successfully"
    PASS_TESTCASEID = "Please pass test case id"
    TEST_CASE_NOT_IN_DB = "Test case details for TestCase ID {},does not exist"
    TEST_CASE_DETAILS_UPDATED = "Test case details updated successfully"
    DB_TYPE_NAME = "DataBase Name is not valid. Supported Databases" \
                   " are postgresql, mysql, mssql, oracle, sqlite"
    INVALID_PROJECT_ID = " the given project does not exist"
    INVALID_ORG_ID = "the given Organization does not exist "
    RESOURCE_EXISTS = "{} already exists"
    NO_PERMISSION = "User does not have required permissions"
    SOURCE = "source"
    DESTINATION = "target"
    EMAIL_NOT_CORRECT = "Your Email id is not correct"
    MAIL_SENT = "Mail sent your Email id"
    PAGE_TO_PASSWORD_RESET = "Page to password reset"
    TOKEN_MISMATCH = "Token Mismatch"
    PROJECT_NOT_EXIST = "Project does not exist"
    SUITE_NOT_EXIST = "suite does not exist"
    TESTCASELOGID_NOT_IN_DB = "testcase log id {} not present in db"
    ADD_ROLE = "Roles added Successfully"
    EMAIL_USER = "Either User Id or Email Id is mandatory"
    DATE_FORMAT = "Date should be passed in YYYY-MM-DD format"
    START_END_DATE = "Both start and end date are required"
    NO_NAME_DEFINE = "No name define"
    DEFAULT_DB_CONNECTION_PREFIX = "Connection"
    TESTSUITE_NOT_IN_DB = "Test suite {} not present in db"
    DB_DETAILS_ALREADY_PRESENT = "Db details already exist"
    DB_CONNECTION_NAME_ALREADY_PRESENT = "Db details with this connection name " \
                                         "already exist"
    NO_SPACES = "User name or host name cannot contain spaces"
    UNAUTHORIZED = "Unauthorized Access"
    PROJECT_NOT_UNDER_ORG = "Project Id provided is not under given org"
    TEST_SUITE_ADDED = "Test suite added successfully"
    PASS_DB_ID = "Please pass DB ID"
    DB_DELETED = "Data Base with db id {} Deleted Sucessfully"
    TEST_SUITE_UPDATED = "Test Suite updated successfully"
    NEW_TEST_SUITE_CREATED = "New Test Suite created"
    ROLE_NOT_UNDER_ORG = "Role Ids provided are not under given Org"
    NO_TEST_CASE = "This test case not present in any test suite"
    TEST_SUITE_NAME_ALREADY_PRESENT = "Test suite name already exist"
    QUALITY_SUITE = "Quality Suite"
    NO_DB_ID = "No data base under this project"
    ORG_PROJECT_REQUIRED = "Either Org Id or Project Id are mandatory"
    ONLY_ORG_OR_PROJECT = "Pass only Org Id or Project Id"
    PERMISSION_LIST = "permission_id_list should not be blank"
    NO_ROLES = "There are no roles associated with given Organization"
    ONLY_USER_OR_EMAIL = "Pass only User id or Email"
    DB_NOT_EXIST = "Db not exist"
    PROJECT_CONTAIN_SUITE_NOT_EXIST = "Project containing this suite not exist"
    TEST_CASE_ABSENT = "Test case passed is absent"
    TEST_SUITE_ABSENT = "Test suite for selected test case is absent"
    TEST_SUITE_NAME_CANNOT_BE_BLANK = "TestSuite name cannot be Blank"
    CONNECTION = "Connection "
    UNKNOWN_DATABASE = "Unknown database '{}'"
    AUTHENTICATION_FAILED = "Authentication failed for user '{}'"
    CANNOT_CONNECT_TO_SERVER = "Can't connect to {} server on '{}' (Name or service not known)"
    UNKNOWN_DB_AUTHENTICATION_FAILED = "Unknown database '{}' or Authentication failed for user '{}'"
    CANNOT_CONNECT_TO_REMOTE_SERVER_MYSQL = "Host is not allowed to connect to this MySQL server"
    PASSWORD_CANNOT_EMPTY = "Password cannot be empty"
    DB_NAME_CANNOT_EMPTY = "Data base name cannot be empty"
    HOSTNAME_CANNOT_EMPTY = "Hostname cannot be empty"
    USERNAME_CANNOT_EMPTY = "Usename cannot be empty"
    TEST_CLASS_NAME = "Test Class Name is not valid. Supported Testclass are" \
                      " are CountCheck, NullCheck, DuplicateCheck, DDLCheck, Datavalidation"
    DELETE_DB_WARNING = "DB connection is associate with existing test case, you cannot delete it."
    DELETE_DB_VERIFY_DELETE = "Data Base with db id {} can be Deleted."


class GenericStrings:
    """Class to store generic strings that are referenced in code."""

    ORACLE_DRIVER = "{ODBC Driver 17 for SQL Server}"
    UNKNOWN_DATABASE_MYSQL = "Unknown database"
    AUTHENTICATION_FAILED_MYSQL = "Access denied for user"
    CANNOT_CONNECT_TO_SERVER_MYSQL = "Can't connect to"
    CANNOT_CONNECT_TO_REMOTE_SERVER_MYSQL = "is not allowed to connect to this"
    UNKNOWN_DATABASE_POSTGRES = "database"
    AUTHENTICATION_FAILED_POSTGRES = "password authentication failed for"
    CANNOT_CONNECT_TO_SERVER_POSTGRES = "could not translate"
    UNKNOWN_DB_AUTHENTICATION_FAILED_ORACLE = "listener does not currently know of service"
    CANNOT_CONNECT_TO_SERVER_ORACLE = "could not resolve the connect identifier specified"


class TimeOuts:
    """Timeouts to be referenced in the code."""

    TEN_DAYS_IN_HOURS = 240
    HUNDRED_DAYS = 100
    ONE_DAY_IN_SECONDS = 60 * 60 * 24


class TestClass:
    """Test Class Constants"""
    COUNT_CHECK = "countcheck"
    NULL_CHECK = "nullcheck"
    DDL_CHECK = "ddlcheck"
    DUPLICATE_CHECK = "duplicatecheck"
    DATA_VALIDATION = "datavalidation"


class TestClassDisplay:
    COUNT_CHECK = 'Count Check'
    NULL_CHECK = "Null Check"
    DDL_CHECK = "DDL Check"
    DUPLICATE_CHECK = "Duplicate Check"
    DATA_VALIDATION = "Data Validation"


class TestTypeDisplay:
    COMPLETENESS = "Completeness"
    NULLS = "Nulls"
    DUPLICATES = "Duplicates"
    CONSISTENCY = "Consistency"
    CORRECTNESS = "Correcteness"


class DQIClassNameMapping:
    """Class to map display value and db value of jobs."""

    dqi_class_name_mapping = \
        {TestClass.COUNT_CHECK: TestTypeDisplay.COMPLETENESS,
         TestClass.NULL_CHECK: TestTypeDisplay.NULLS,
         TestClass.DUPLICATE_CHECK: TestTypeDisplay.DUPLICATES,
         TestClass.DDL_CHECK: TestTypeDisplay.CONSISTENCY,
         TestClass.DATA_VALIDATION: TestTypeDisplay.CORRECTNESS
         }


class SupportedDBType:
    """Class to return Name and Id of the DataBase."""

    supported_db_type = {1: "PostgreSQL", 2: "MySQL", 3: "MsSQL", 4: "Oracle",
                         5: "SQLite"}

    def get_db_name_by_id(self, db_id):
        """
        Method to return database name by passing Id.

        Args:
            db_id: (int) Id of the DB

        Returns:(str) name of the database
        """
        # Returns None if Id does not exist
        return self.supported_db_type.get(db_id)

    def get_db_id_by_name(self, name):
        """
        Method to return database Id by passing name.

        Args:
            name: (str) name of the database
        Returns: (int) Id of the database
        """
        for key, value in self.supported_db_type.items():
            # Name will be converted to lower case and compared
            if value.lower() == name.lower():
                return key
            # Returns None if Name does not exist


class SupportedTestClass:
    """Class to return Test Class Name and Id."""

    supported_test_class = {1: TestClass.COUNT_CHECK, 2: TestClass.NULL_CHECK,
                            3: TestClass.DDL_CHECK,
                            4: TestClass.DUPLICATE_CHECK,
                            5: TestClass.DATA_VALIDATION}
    supported_test_class_display_name = {1: TestClassDisplay.COUNT_CHECK,
                                         2: TestClassDisplay.NULL_CHECK,
                                         3: TestClassDisplay.DDL_CHECK,
                                         4: TestClassDisplay.DUPLICATE_CHECK,
                                         5: TestClassDisplay.DATA_VALIDATION}

    def get_test_class_name_by_id(self, test_class_id):
        """
        Method to return test class name by passing Id.

        Args:
            test_class_id: (int) Id of the test class
        Returns: (str) name of the test class
        """
        return self.supported_test_class.get(test_class_id)

    def get_test_class_id_by_name(self, name):
        """
        Method to return test class Id by passing name.

        Args:
            name: (str) name of the test class
        Returns: (int) Id of the test class
        """
        for key, value in self.supported_test_class.items():
            if value == name.lower():
                return key

    def get_test_class_display_name_by_id(self, test_class_id):
        """
                Method to return test class name by passing Id.
                Args:
                    test_class_id: (int) Id of the test class
                Returns: (str) name of the test class
        """
        return self.supported_test_class_display_name.get(test_class_id)


class ExecutionStatus:
    """Class to return Name and Id of the DataBase."""

    execution_status = {0: "inprogress", 1: "pass", 2: "fail", 3: "error",
                        4: "new"}

    def get_execution_status_by_id(self, execution_id):
        """
        Method to return execution status by passing Id.

        Args:
            execution_id: (int) Id of the status

        Returns:(str) Execution status
        """
        return self.execution_status.get(execution_id)

    def get_execution_status_id_by_name(self, name):
        """
        Method to return execution status Id by passing status.

        Args:
            name: (str) execution status

        Returns: (int) Id of the status

        """
        for key, value in self.execution_status.items():
            if value == name.lower():
                return key
