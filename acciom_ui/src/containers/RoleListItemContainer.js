import React, { Component } from 'react';
import { connect } from 'react-redux'; 
import { getRolesByProjectId, getRolesByOrgId } from '../actions/userManagementActions';
import { roleTypes } from '../reducers/userManagementReducer';
import Select from '@material-ui/core/Select';
import Chip from '@material-ui/core/Chip';
import MenuItem from '@material-ui/core/MenuItem';
import Button from '@material-ui/core/Button';

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
		// if (nextProps.orgProjectList.length > 0 && (!nextProps.selectedOrgProject)) {
		// 	nextProps.onOrgProjectChange(nextProps.index, nextProps.orgProjectList[0], nextProps.category);
		// }
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
		if (selectedOrgProject.target.value === this.props.selectedOrgProject) {
			return;
		};
		this.props.onOrgProjectChange(this.props.index, selectedOrgProject.target.value , this.props.category);
	};

	handleRoleChange = (roles) => {
		this.props.onRoleChange(this.props.index, roles, this.props.category);
	};

	addRow = () => {
		this.props.onAddRowClick();
	};
	
	deleteRow = (type, index) => {
		this.props.onDeleteRowClick(type, index);
	};

	render() {
		const styles = {
			option: (styles, state) => ({
			...styles,
			color: state.isSelected ? "black" : null
			})
		};

		return (
			<div>
				<Select
					className="editUserProjectSelect"
					value = {this.props.selectedOrgProject}
					onChange = { (item) => this.handleOrgProjectChange(item) }
					>
					{this.props.orgProjectList.map((data, index) => (
						<MenuItem key={index} value={data}>{ data.label }</MenuItem>
					))}					
				</Select>
				<Select
					className="editUserRoleSelect"
					multiple
					value={this.state.selectedRoles}
					onChange={ (item) => this.handleRoleChange(item)}
					renderValue={() => (
						<div>
						{this.state.selectedRoles.map((value, index) => (
							<Chip  className="roleChip" key={index} label={value.label} />
						))}
						</div>
					)}
					>
					{this.state.rolesList.map((data,index) => (
						<MenuItem key={index} value={data}>
						{data.label}
						</MenuItem>
					))}
				</Select>
				{ this.props.showDeleteBtn ? 
					<i className='fas fa-minus-circle minusCircle minuscirclecolor' onClick={() => this.deleteRow(this.props.roleType, this.props.index)}></i>
					: null
				}
				<br/>
				{ this.props.showAddBtn ? 
					<Button variant="contained" className="addProjectPlusIcon" onClick={() => this.addRow()}><i className='fas fa-plus-circle' ></i>&nbsp;&nbsp;Add</Button>
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