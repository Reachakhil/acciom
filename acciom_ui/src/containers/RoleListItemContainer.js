import React, { Component } from 'react';
import Select from 'react-select';
import { connect } from 'react-redux'; 
import { getRolesByProjectId, getRolesByOrgId } from '../actions/userManagementActions';
import { roleTypes } from '../reducers/userManagementReducer';

const formatRoleListData = (rolesList) => {
	let formatedList = [];
	if (rolesList) {
		formatedList = rolesList.map((item) => {
			return { value: item.role_id, label: item.role_name };
		});
	}
	return formatedList;
};

const getSelectedRoleItems = (rolesList, selectedRoles) => {
	const selectedItems = rolesList.filter(role => {
		return selectedRoles.includes(role.value);
	});
	return selectedItems;
};

class RoleListItemContainer extends Component {
	constructor(props) {
		super(props);
		this.state = {
			rolesList:[],
			selectedRoles:[]
		};
	}

	componentDidMount() {
		if (this.props.selectedOrgProject) {
			this.getRolesByOrgRProject(this.props.selectedOrgProject);
		}
	}

	static getDerivedStateFromProps = (nextProps, prevState) => {
		if (nextProps.selectedOrgProject) {	
			if (nextProps.orgProjectRolesList.hasOwnProperty(nextProps.selectedOrgProject.value)) {
				const rolesList = formatRoleListData(nextProps.orgProjectRolesList[nextProps.selectedOrgProject.value]);
				const selectedRoles = getSelectedRoleItems(rolesList, nextProps.selectedRoles);
				return {
					...prevState,
					rolesList,
					selectedRoles
				};
			}
		}
		return prevState;
	}

	getRolesByOrgRProject = (selectedOrgProject) => {
		if (this.props.orgProjectRolesList.hasOwnProperty(selectedOrgProject.value)) return;

		if (selectedOrgProject.roleType ===  roleTypes.ORGANIZATION ) {
			this.props.getRolesByOrgId(selectedOrgProject.uid, selectedOrgProject.value);
		} else if (selectedOrgProject.roleType ===  roleTypes.PROJECT ) {
			this.props.getRolesByProjectId(selectedOrgProject.uid, selectedOrgProject.value);
		}
	}

	handleOrgProjectChange = selectedOrgProject => {
		if (selectedOrgProject === this.props.selectedOrgProject) {
			return;
		};
		this.props.onOrgProjectChange(this.props.index, selectedOrgProject);
	};

	handleRoleChange = (roles) => {
		this.props.onRoleChange(this.props.index, roles);
	};

	addRow = () => {
		this.props.onAddRowClick();
	};
	
	deleteRow = (type, index) => {
		this.props.onDeleteRowClick(type, index);
	};

	render() {
		return (
			<div>
				<Select 
					className='singleSelect'
					theme={theme => ({ ...theme, borderRadius: 5, colors: { ...theme.colors, primary25: '#d38d92', primary: '#b7c0ce', primary50: '#b7c0ce' }, })}
					value={this.props.selectedOrgProject}
					onChange={ (item) => this.handleOrgProjectChange(item) }
					options= { this.props.orgProjectList }
				/>

				<Select
					className='multiSelect'
					isMulti='true'
					theme={theme => ({ ...theme, borderRadius: 5, colors: { ...theme.colors, primary25: '#d38d92', primary: '#b7c0ce', primary50: '#b7c0ce' }, })}
					value={this.state.selectedRoles}
					onChange={ (item) => this.handleRoleChange(item) }
					options={ this.state.rolesList }
				/>

				{ this.props.showDeleteBtn ? 
					<i className='fas fa-minus-circle minusCircle minuscirclecolor' onClick={() => this.deleteRow(this.props.roleType, this.props.index)}></i>
					: null
				}
				<br/>
				{ this.props.showAddBtn ? 
					<i className='fas fa-plus-circle plusCircle minuscirclecolor' onClick={() => this.addRow()}></i>
					: null
				}
			</div>
		);
	};
}

const mapStateToProps = (state) => {
	return {
		orgProjectRolesList: state.userManagementData.orgProjectRolesList,
	};
};

const mapDispatchToProps = dispatch => ({
	getRolesByOrgId: (orgId, key) => dispatch(getRolesByOrgId(orgId, key)),
	getRolesByProjectId: (projectId, key) => dispatch(getRolesByProjectId(projectId, key))
});

export default connect(mapStateToProps, mapDispatchToProps) (RoleListItemContainer);