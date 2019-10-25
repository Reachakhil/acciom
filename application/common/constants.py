"""File to store all constants."""


class APIMessages:
    """Messages to be sent in API Responses."""

    EMPTY_FIELD = "{} cannot be blank"
    USER_EXISTS = "User with Email ID {} already exists"
    VERIFY_EMAIL = "Please verify your Email Address"
    USER_CREATED = "User Created with Email ID {}"
    INTERNAL_ERROR = "An Internal Server Error has occurred"
    USER_NOT_EXIST = "User with Email ID {} does not exist"
    INVALID_UID_PWD = "Please enter valid Username and Password"
    VERIFY_USER = "User verification is pending. Please verify through email"
    USER_LOGIN = "Logged in as {}"
    RESET_REQUEST = "Password Reset Request"
    RESET_EMAIL = "Password Reset Email was sent to your email"
    INVALID_TOKEN = "Invalid Token"
    RESET_PAGE = "Page for Password Reset"
    PASSWORD_CHANGE = "Password Changed Successfully"
    USER_VERIFIED = "User Verification is Complete"
    INVALID_PASSWORD = "Invalid Password"
    NEW_TOKEN = "Access Token has been generated"
    INVALID_EMAIL_PASSWORD = "Invalid Email or Password"
    DELETED_USER = "Your account is not active, Please contact Administrator"
    ADD_DATA = "Test Suite Uploaded Successfully"
    JOB_SUBMIT = "Job Submitted Successfully"
    PARSER_MESSAGE = "Field is Mandatory"
    CREATE_RESOURCE = "{} is Successfully Created"
    UPDATE_RESOURCE = "{} is Updated Successfully"
    SUCCESS = "Success"
    NO_RESOURCE = "{} is not available"
    DB_DETAILS_ADDED = "Database details added Successfully"
    DATA_LOADED = "Data Loaded Successfully"
    DBID_NOT_IN_DB = "Database details for DB ID {}, does not exist"
    DB_DETAILS_UPDATED = "Database details updated Successfully"
    ABSENCE_OF_DBID = "Please Pass Database Connection ID"
    CONNECTION_CREATE = "Test Connection Successfull"
    CONNECTION_CANNOT_CREATE = "Unable to Establish Connection to Database, {}"
    NO_DB_UNDER_PROJECT = "No Database Connections available for this Project"
    PASS_DBID_or_PROJECTID = "Please pass Database ID or Project ID"
    TEST_CASE_DELETED = "Test Case with test case ID {} Deleted Successfully"
    PASS_TESTCASEID = "Please pass Test Case ID"
    TEST_CASE_NOT_IN_DB = "Test Case details for TestCase ID {}, does not exist"
    TEST_CASE_DETAILS_UPDATED = "Test Case details Updated Successfully"
    DB_TYPE_NAME = "DataBase Name is not valid. Supported Databases" \
                   " are PostgreSQL, MYSQL, MSSQL, Oracle, SQLite"
    INVALID_PROJECT_ID = "Invalid Project"
    INVALID_ORG_ID = "Invalid Organization"
    RESOURCE_EXISTS = "{} already exists"
    NO_PERMISSION = "User does not have required Permissions"
    SOURCE = "Source"
    DESTINATION = "Target"
    EMAIL_NOT_CORRECT = "Incorrect Email ID"
    MAIL_SENT = "Mail sent to your Email ID"
    PAGE_TO_PASSWORD_RESET = "Redirect to Password Reset Page"
    TOKEN_MISMATCH = "Token Mismatch"
    PROJECT_NOT_EXIST = "Project does not exist"
    SUITE_NOT_EXIST = "Suite does not exist"
    TESTCASELOGID_NOT_IN_DB = "Testcase Log ID {} not present in DB"
    ADD_ROLE = "Roles added Successfully"
    EMAIL_USER = "Either User ID or Email ID is mandatory"
    DATE_FORMAT = "Date should be passed in YYYY-MM-DD format"
    START_END_DATE = "Both Start and End Date are required"
    NO_NAME_DEFINE = "Description Not Available"
    DEFAULT_DB_CONNECTION_PREFIX = "Connection"
    TESTSUITE_NOT_IN_DB = "Test Suite {} not present in Database"
    DB_DETAILS_ALREADY_PRESENT = "Database Details already exist"
    DB_CONNECTION_NAME_ALREADY_PRESENT = "DB Details with this connection name " \
                                         "already exist"
    NO_SPACES = "Spaces not allowed in Database Name or User Name or Host Name"
    UNAUTHORIZED = "Unauthorized Access"
    PROJECT_NOT_UNDER_ORG = "Project ID provided is not under given Organization"
    TEST_SUITE_ADDED = "Test Suite added Successfully"
    PASS_DB_ID = "Please Pass Database ID"
    DB_DELETED = "Database with DB ID {} Deleted Successfully"
    TEST_SUITE_UPDATED = "Test Suite updated Successfully"
    NEW_TEST_SUITE_CREATED = "New Test Suite Created"
    ROLE_NOT_UNDER_ORG = "Role IDs provided are not under given Organization"
    NO_TEST_CASE = "Invalid Test Case"
    TEST_SUITE_NAME_ALREADY_PRESENT = "Test Suite Name already exist"
    QUALITY_SUITE = "Quality Suite"
    NO_DB_ID = "No Active Database Connections"
    ORG_PROJECT_REQUIRED = "Either of Organization or Project ID is mandatory"
    ONLY_ORG_OR_PROJECT = "Pass only Organization or Project ID"
    PERMISSION_LIST = "permission_id_list should not be blank"
    NO_ROLES = "There are No Roles associated with given Organization"
    ONLY_USER_OR_EMAIL = "Pass only User id or Email"
    DB_NOT_EXIST = "Database does not exist"
    PROJECT_CONTAIN_SUITE_NOT_EXIST = "Invalid Test Suite"
    TEST_CASE_ABSENT = "Invalid Test Case(s)"
    TEST_SUITE_ABSENT = "Test Suite Not Exists for a Selected Test Case"
    TEST_SUITE_NAME_CANNOT_BE_BLANK = "Test Suite Name cannot be Blank"
    UNKNOWN_DATABASE = "Unknown Database '{}'"
    AUTHENTICATION_FAILED = "Authentication failed for user '{}'"
    CANNOT_CONNECT_TO_SERVER = "Can't connect to {} Server on '{}' (Name or Service not known)"
    UNKNOWN_DB_AUTHENTICATION_FAILED = "Unknown database '{}' or Authentication failed for User '{}'"
    CANNOT_CONNECT_TO_REMOTE_SERVER_MYSQL = "Host not allowed to connect to MySQL Server"
    PASSWORD_CANNOT_EMPTY = "Password cannot be Blank"
    DB_NAME_CANNOT_EMPTY = "Database Name cannot be Blank"
    HOSTNAME_CANNOT_EMPTY = "Host Name cannot be Blank"
    USERNAME_CANNOT_EMPTY = "User Name cannot be Blank"
    TEST_CLASS_NAME = "Test Class Name is not valid. Supported Test Class Names are" \
                      " CountCheck, NullCheck, DuplicateCheck, DDLCheck, DataValidation"
    DELETE_DB_WARNING = "Database Connection is associated with existing Test Case, hence cannot be Deleted"
    DELETE_DB_VERIFY_DELETE = "Database with DB ID {} can be Deleted"
    TOKEN_DELETED = "Personal Access Token '{}' is Deleted"
    CONNECTION_SETUP = "Connection Setup Successful"
    AVERAGE_DQI = "Average DQI"
    USER_ROLE_DELETED = "User Role for org id {} is Deleted"
    FIRST_LAST_NAME = "First Name and Last Name are Compulosry"
    VALID_EMAIL = "Please pass Valid Email ID"
    NULL_CHECK_RESULT = "Total {} Records with Null value(s)"
    DUPLICATE_CHECK_RESULT = "{} Duplicates Found"
    INVALID_LENGTH = "Max field Length is {} Characters"
    WRONG_DB_CONNECTION = "The given DB conncetion does not belong to the project"
    WRONG_QUERY_ID = "The given query id is not valid"
    INVALID_LENGTH = "Max field Length is {} Characters"
    FORBIDDEN = "Not Authorized to view the data"
    DELETE_PROJECT_TRUE = "Project '{}' is deleted"
    DELETE_PROJECT_FALSE = "Project '{}' can not be deleted"
    FORBIDDEN = "Not Authorized to View"
    NOT_AVAILABLE = "Not Available"
    COLUMN = "Column Name"
    IS_NULLABLE = "IS Nullable"
    DATA_TYPE = "Data Type"
    TEST_CASE_ADDED = "Test Case Added Successfully"
    PASS_TABLES = "Table names are Compulsory"
    PASS_TEST_CASE_CLASS = "Please provide Test Class Name"
    USER_DETAILS_UPDATED = "User details Updated Successfully"
    ORG_DELETED = "Organization Deleted Successfully"
    DELETE_ORG_FALSE = "Organization cannot be deleted"
    SET_SUCCESS = "Default Organization and Project set Successfully"
    PASS_FIRST_NAME = "Please Pass First Name"
    PASS_LAST_NAME = "Please Pass Last Name"
    ROLE_NAME_CANNOT_BLANK = "Role Name cannot be Blank"
    ROLE_DESCRIPTION_CANNOT_BLANK = "Role Description cannot be Blank"
    ROLE_UPDATED = "Role Updtaed Successfully"


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
    EMAIL_FORMAT_REGEX = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


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
    NULLS = "Valid"
    DUPLICATES = "Uniqueness"
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
    supported_test_class_test_type_display_name = {
        1: TestTypeDisplay.COMPLETENESS,
        2: TestTypeDisplay.NULLS,
        3: TestTypeDisplay.CONSISTENCY,
        4: TestTypeDisplay.DUPLICATES,
        5: TestTypeDisplay.CORRECTNESS}

    def get_test_class_name_by_id(self, test_class_id):
        """
        Method to return test class name by passing Id.

        Args:
            test_class_id: (int) Id of the test class
        Returns: (str) name of the test class
        """
        return self.supported_test_class.get(test_class_id)

    def get_test_type_display_name_by_id(self, test_class_id):
        """
        Method to return test type display name by passing id.

        Args:
            test_class_id(int): Id of the test class.

        Returns(str):test type display name of the test class.
        """
        return self.supported_test_class_test_type_display_name.get(
            test_class_id)

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
