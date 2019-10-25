import React from 'react';
import { connect } from 'react-redux';
import { Route, BrowserRouter as Router, Redirect  } from 'react-router-dom';
import styled from 'styled-components';
import Startup from '../containers/Startup';
import TestSuiteUpload from '../containers/TestSuiteUpload';
import Dashboard from '../containers/Dashboard';
import NavigationBar from '../containers/NavigationBar';
import Login from '../containers/Login';
import ViewDbDetails from '../containers/ViewDbDetails';
import AddDbDetails from '../containers/AddDbDetails';
import UserManagement from '../containers/UserManagement';
import RootContent from '../containers/RootContent';
import ForgotPassword from './ForgotPassword';
import AuthToken from './AuthToken';
import ChangePasswordComponent from './ChangePassword';
import EditUserRoles from '../containers/EditUserRoles';
import EditTestCase from '../containers/EditTestCase';
import ViewSuite from '../containers/ViewSuite';
import CreateSuite from '../containers/CreateSuite';
import UserProfile from '../containers/UserProfile';

import ProjectManagement from '../containers/ProjectManagement';
import ManageUserRole from './ManageUserRole'
import OrganizationManagement from '../containers/OrganizationManagement';


const RootContainer = styled.div`
	font-size: 0.8rem;	
`;

const Sidebar = styled.div`
	display: inline-block;
`;

const Content = styled.div`
	display: inline-block;
	position: relative;
	left:100px;
	top: 100px;
	width: -webkit-calc(100% - 250px);
    width:    -moz-calc(100% - 250px);
    width:         calc(100% - 250px);
`;

const PrivateRoute = ({ component: Component, ...rest }) => (
	<Route {...rest} render={(props) => {
		return (
			rest.authTokenExpired === true ?
				<Redirect to='/login' /> : <Component {...props} />
		)}} 
	/>
)
  
const App = (props) => (
	<RootContainer>
		<Router>
			<Sidebar>
				<NavigationBar />
			</Sidebar>
			<Content>
				<RootContent></RootContent>
				<Route path="/" exact component={Dashboard} />
				<Route path="/login" component={Login} />
				<PrivateRoute path="/dashboard" authTokenExpired={props.authTokenExpired} component={Dashboard} />
				<PrivateRoute path="/startup" authTokenExpired={props.authTokenExpired} component={Startup} />
				<PrivateRoute path="/test_suite_upload" authTokenExpired={props.authTokenExpired} component={TestSuiteUpload} />
				<PrivateRoute path="/add_db_details" authTokenExpired={props.authTokenExpired} component={AddDbDetails} />
				<PrivateRoute path="/add_db_details/:id" authTokenExpired={props.authTokenExpired} component={AddDbDetails} />
				<PrivateRoute path="/view_db_details" authTokenExpired={props.authTokenExpired} component={ViewDbDetails} />
				<PrivateRoute path="/forgot_password" authTokenExpired={props.authTokenExpired} component={ForgotPassword} />
				<PrivateRoute path="/change_password" authTokenExpired={props.authTokenExpired} component={ChangePasswordComponent} />
				<PrivateRoute path="/access_token" authTokenExpired={props.authTokenExpired} component={AuthToken} />
				<PrivateRoute path="/user_management" authTokenExpired={props.authTokenExpired} component={UserManagement} />
				<PrivateRoute path="/projects" authTokenExpired={props.authTokenExpired} component={ProjectManagement} />
			    <PrivateRoute path="/organization" authTokenExpired={props.authTokenExpired} component={OrganizationManagement} />
				<PrivateRoute path="/edit_user_role/:id" authTokenExpired={props.authTokenExpired} component={EditUserRoles} />
				<PrivateRoute path="/edit_test_case/:suite_id" authTokenExpired={props.authTokenExpired} component={EditTestCase} /> 
				<PrivateRoute path="/create_suite" authTokenExpired={props.authTokenExpired} component={CreateSuite} /> 
				<PrivateRoute path = "/view_suites" authTokenExpired={props.authTokenExpired} component={ViewSuite}/>
				<PrivateRoute path="/ManageUserRole" authTokenExpired={props.authTokenExpired} component={ManageUserRole} />
				<PrivateRoute path="/user_profile" authTokenExpired={props.authTokenExpired} component={UserProfile} />
				

			</Content>
		</Router>
	</RootContainer>
);

const mapStateToProps = (state) => {
	return {
		authTokenExpired: state.loginData.authTokenExpired
	};
};

export default connect(mapStateToProps)(App);
