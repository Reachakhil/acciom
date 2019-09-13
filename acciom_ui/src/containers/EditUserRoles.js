import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { Button } from 'react-bootstrap';
import { retriveUserRoleByUserId, updateUserRoles } from '../actions/userManagementActions';
import { roleTypes } from '../reducers/userManagementReducer';
import RoleListItemContainer from './RoleListItemContainer';

const formatOrgProjectList = (currentOrg, projectList) => {
	const orgList = [{
		value: `o_${currentOrg.org_id}`, 
		label: currentOrg.org_name, 
		roleType: roleTypes.ORGANIZATION,
		uid: currentOrg.org_id
	}];

	const formattedProjectList = projectList.map((item) => {
		return { value: `p_${item.project_id}`, label: item.project_name, roleType: roleTypes.PROJECT, uid: item.project_id} ;
	});

	return [...orgList, ...formattedProjectList];
};

const getObjFromList = (list, key, value)=> list.find(v => v[key] === value);

class EditUserRoles extends Component {

	constructor (props) {
		super(props);
		this.state = {
			selectedUser: null,
			userRoleList: [],
			orgProjectList: []
		};
	}

	componentDidMount () {
		const userId = (this.props.match && this.props.match.params) ? this.props.match.params.id : null;
		this.props.getSelectedUser(this.props.currentOrg.org_id, userId);
	}

	static getDerivedStateFromProps = (nextProps, prevState) => {
		if (nextProps.redirectToUserMgmtHome) {
			nextProps.history.push('/user_management');
		} else if (!prevState.selectedUser && nextProps.selectedUser) {
			
			const orgProjectList = formatOrgProjectList(nextProps.currentOrg, nextProps.projectList);

			let userRoleList = [];

			// organization roles
			if (nextProps.selectedUser.org_allowed_role_list.length > 0) {
				userRoleList = [{
					id: `o_${nextProps.currentOrg.org_id}`, 
					allowed_role_list: nextProps.selectedUser.org_allowed_role_list, 
					roleType: roleTypes.ORGANIZATION,
					uid: nextProps.currentOrg.org_id
				}];
			}

			// project roles
			if (nextProps.selectedUser.project_role_list.length > 0) {
				const userProjectRoleList = nextProps.selectedUser.project_role_list.map((item) => {
					return {
						id: `p_${item.project_id}`, 
						allowed_role_list: item.allowed_role_list, 
						roleType: roleTypes.PROJECT,
						uid: item.project_id
					};
				});
				userRoleList = userRoleList.concat(userProjectRoleList);
			}
			
			return {
				...prevState,
				selectedUser: nextProps.selectedUser,
				userRoleList,
				orgProjectList
			};
		}

		return prevState;
	};

	onAddRowClick = () => {
		const userRoleList = [...this.state.userRoleList].concat(
			[{ id: Math.floor(Math.random()*1000000), allowed_role_list: [], roleType: roleTypes.NEW }]
		);

		this.setState({userRoleList});
	};

	onDeleteRowClick = (type, index) => {
		const userRoleList = [...this.state.userRoleList];
		userRoleList.splice(index, 1);
		this.setState({userRoleList});
	};

	onOrgProjectChange = (index, selectedOrgProject) => {
		const userRoleList = [...this.state.userRoleList];
		userRoleList.splice(index, 1, 
			{	
				id: selectedOrgProject.value, 
				roleType: selectedOrgProject.roleType, 
				uid: selectedOrgProject.uid,  
				allowed_role_list:[]
			}
		);
		this.setState({userRoleList});
	};

	onRoleChange = (index, roles) => {
		const userRoleList = [...this.state.userRoleList];
		const listItem = userRoleList[index];

		const allowed_role_list = roles.map((role) =>{
			return role.value;
		});
		
		userRoleList.splice(index, 1, {...listItem, allowed_role_list});
		this.setState({userRoleList});
	};

	getSelectedOrgProject = (id) => {
		return getObjFromList(this.state.orgProjectList, 'value', id);
	};

	getRoleItemComponent = (list) => {
		let roleElements = [];
		const count = list.length;

		roleElements = list.map((item, index) => {
			let showAdd = false;
			let showDelete = true;
			if (count === 1) {
				showDelete = false;
			}
			if (count-1 === index) {
				showAdd = true;
			}

			return (
				<li key={`${item.roleType}${index}`}>
					<RoleListItemContainer 
						onAddRowClick={this.onAddRowClick}
						onDeleteRowClick={this.onDeleteRowClick}
						showAddBtn={showAdd && list.length === (index+1)}
						showDeleteBtn={(!showDelete && list.length === 1)? false : true }
						index={index} 
						roleType={item.roleType}
						orgProjectList = {this.state.orgProjectList}
						selectedOrgProject = { getObjFromList(this.state.orgProjectList, 'value', item.id) }
						id={item.id}
						selectedRoles = {item.allowed_role_list}
						onOrgProjectChange = {this.onOrgProjectChange}
						onRoleChange = {this.onRoleChange}
					/>
				</li>
			);
		});

		return roleElements;
	};

	renderUserRoles = () => {
		let element = null; 

		if (this.state.userRoleList.length > 0) {
			element = this.getRoleItemComponent(this.state.userRoleList);
			if (element.length > 0) {
				element.push(
					(<div class='footer'>
						<Link to={`/user_management`}>
							<Button type="button" className="userbackbtn" bsStyle="primary">Back To User List</Button>
						</Link>
						<Button type="button" className="button-colors" bsStyle="primary" onClick={(e) => {this.onSaveUserRoles()}}>Save</Button>
					</div>)
				);
			}
		}

		return element;
	};

	onSaveUserRoles = () => {
		// build payload
		const projectRoleList = [];
		let orgAllowedRoleList = []; 
		this.state.userRoleList.forEach((item) => {
			if (item.roleType === roleTypes.PROJECT) {
				projectRoleList.push(
					{
						'project_id': item.uid,
						'allowed_role_list': item.allowed_role_list
					}
				);
			} else if (item.roleType === roleTypes.ORGANIZATION) {
				orgAllowedRoleList = orgAllowedRoleList.concat([...item.allowed_role_list]);
			}

		});
		const payload = {
			'org_id': this.props.currentOrg.org_id,
			// 'user_id': this.props.selectedUser.user_id,
			'email_id': this.props.selectedUser.email_id,
			'project_role_list': projectRoleList,
			'org_allowed_role_list': orgAllowedRoleList
		};
		this.props.updateUserRoles(JSON.stringify(payload));
	};
	
	render() {
		return (
			<div id="editUserRoles">
				<h3 className="usermanagetitle">Manage Role</h3>
				<div className = "DescriptionHeader submailtitle">Email</div>
				<input type="text" value={this.props.selectedUser? this.props.selectedUser.email_id: ''} className="Description" disabled/>

				{ this.renderUserRoles() }

			</div>
		);
	 }
}

const mapStateToProps = (state) => {
	return {
		currentOrg: state.appData.currentOrg,
		selectedUser: state.userManagementData.selectedUser,
		projectList: state.appData.projectList,
		userOrgRoleList: state.userManagementData.userOrgRoleList,
		userProjectRoleList: state.userManagementData.userProjectRoleList,
		userNewRoleList: state.userManagementData.userNewRoleList,
		redirectToUserMgmtHome: state.userManagementData.redirectToUserMgmtHome
	};
};

const mapDispatchToProps = dispatch => ({
	getSelectedUser: (org_id, user_id) => dispatch(retriveUserRoleByUserId(org_id, user_id)),
	updateUserRoles: (data) => dispatch(updateUserRoles(data))
});

export default connect(mapStateToProps, mapDispatchToProps)(EditUserRoles);