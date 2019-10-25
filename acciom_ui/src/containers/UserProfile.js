import React, { Component } from 'react';
import { connect } from 'react-redux';
import PersonIcon from '@material-ui/icons/Person';
import { showOrgChangePage, updateSelectedOrganization, getProjectListByOrgId } from '../actions/appActions';
import { showProjectSwitchPage, updateSelectedProject } from '../actions/appActions';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import Button from '@material-ui/core/Button';


class UserProfile extends Component{

    useStyles = makeStyles(theme => ({
        root: {
        padding: theme.spacing(3, 2),
        },
    }));
    constructor(props) {
		super(props);
		this.state = {
            selectedOrgId: '',
            selectProjectId:'',
		};
	}

	// componentDidMount() {
    //     const currentOrg = { value: this.props.currentOrg.org_id, label: this.props.currentOrg.org_name };
    //     this.setState({selectedOrgId: currentOrg.value});
    //     const currentProject = { value: this.props.currentProject.project_id, label: this.props.currentProject.project_name };
    //     this.setState({selectProjectId: currentProject.value},()=>{
    //     });
    // }
    
    renderOrgListOptions = () => {
		const options = this.props.orgList.map((item) => {
			return { value: item.org_id, label: item.org_name} ;
		});
        return options;
	};
	handleOrgChange = (e) => {
		this.setState({selectedOrgId: e.target.value});
    };
    renderProjectListOptions=()=>{
        const options = this.props.projectList.map((item) => {
			return { value: item.project_id, label: item.project_name} ;
		});
		return options;

    };
    handleProjectChange =(e)=>{
        this.setState({selectProjectId:e.target.value})
    };

    render(){
        return(
            <div>
                <table>
                    <tr>
                        <td><PersonIcon className="userAccount"/></td>
                        <td><label className="main_titles userProfileTitle" >User Profile</label></td>
                    </tr>
                </table>
            <Paper className="UserProfilePaper">
                <table>
                    <tr>
                        <td>
                        <TextField
                        className="userProfileFname"
						name="firstname"
						label="First Name"
						margin="normal"
						/>
                        </td>
                        <td>
                        <TextField
						className="userProfileLname"
						name="lastname"
						label="Last Name"
						margin="normal"
						/>
                        </td>
                        <td>
                        <TextField
                        className="userProfileEmail"
						name="email"
						label="Email"
                        margin="normal"
                        readOnly value="user1@accionlabs.com" />
                        </td>
                        <td><Button className="button-colors userSubmitButton">Submit</Button></td>
                    </tr>
                </table>
                <div>
                    <table>
                        <tr>
                            <td><label className="userProfileLabel">Set Default Organization</label></td>
                            <td><label className="userProfileProjectLabel">Set Default Project</label></td>
                        </tr>
                        <tr>
                            <td>
                            <Select  
                            className="select_organization_default"
                            value={this.state.selectedOrgId}
                            onChange={ (item) => this.handleOrgChange(item) }
                            >
                            {this.renderOrgListOptions().map((data, index) => (
                            <MenuItem key={index} value={data.value}>{ data.label }</MenuItem>
                            ))}
                            </Select>
                            </td>
                            <td>
                            <Select 
                            className="select_Project_default"
                            value={this.state.selectProjectId}
                            onChange={ (item) => this.handleProjectChange(item) }
                            >
                            {this.renderProjectListOptions().map((data, index) => (
                            <MenuItem key={index} value={data.value}>{ data.label }</MenuItem>
                            ))}
                            </Select>
                            </td>
                        </tr>
                    </table>
                </div>
            </Paper>
            </div>
        );
    }
}

const mapStateToProps = (state) => {
    console.log(state.appData,"dddd")
	return {
		orgList: state.appData.organizationList,
        currentOrg: state.appData.currentOrg,
        projectList:state.appData.projectList,
        currentProject:state.appData.currentProject
	};
};

const mapDispatchToProps = (dispatch) => {
	return {
		updateSelectedOrganization: (data) => dispatch(updateSelectedOrganization(data)),
        getProjectListByOrgId: (data) => dispatch(getProjectListByOrgId(data)),
        showProjectSwitchPage: (data) => dispatch(showProjectSwitchPage(data)),
        updateSelectedProject: (data) => dispatch(updateSelectedProject(data)),
	}
};

export default connect(mapStateToProps, mapDispatchToProps)(UserProfile)