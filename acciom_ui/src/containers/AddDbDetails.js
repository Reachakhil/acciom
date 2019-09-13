import React, { Component } from "react";
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { FormGroup, ControlLabel, FormControl, Button, Panel, Form, Col} from 'react-bootstrap';

import { addDatabaseDetails, getDBDetailsById, updateDBDetails, checkDbConnection, redirectToViewDbPageComplete, resetSelectedDbDetails} from '../actions/dbDetailsActions';

class AddDbDetails extends Component {

	constructor(props) {
		super(props);
		this.initialiseFormState();
	}

	componentDidMount() {
		const dbTypeId = this.state.formData['db_connection_id'];
		if (dbTypeId)  {
			this.setState({isEditMode:true});
			this.props.getDBDetailsById(dbTypeId);
		}else{
			this.setState({isEditMode:false});			
		}
	}

	static getDerivedStateFromProps = (nextProps, prevState) => {
		if (prevState.isEditMode && prevState.loading && !prevState.selectedDbDetails && nextProps.selectedDbDetails) {
			return {
				...prevState,
				formData: {
					...prevState.formData,
					'db_connection_name' : nextProps.selectedDbDetails.db_connection_name,
					'db_type' : nextProps.selectedDbDetails.db_type,
					'db_name' : nextProps.selectedDbDetails.db_name,
					'db_hostname' : nextProps.selectedDbDetails.db_hostname,
					'db_username' : nextProps.selectedDbDetails.db_username,
					'db_password' : nextProps.selectedDbDetails.db_password
				},
				loading : false
			};
		} else if (nextProps.redirectToViewDBPage) {
			nextProps.redirectToViewDbPageComplete();
			nextProps.history.push('/view_db_details');
		} 
		return null;
	}

	initialiseFormState = () => {
		const dbTypeId= (this.props.match && this.props.match.params) ? this.props.match.params.id : null;
		this.state = {
			formData: this.getInitialFormData(dbTypeId),
			errors: {}, 
			formSubmitted: false, 
			loading: true,
			selectedDbDetails: null,
			isEditMode: false,
			updatedDbDetails:false
		};
	}
	
	getInitialFormData = (dbConnectionId) => {
		const formDataObj = {'project_id': this.props.currentProject.project_id};
		if (dbConnectionId) {
			formDataObj['db_connection_id'] = dbConnectionId;
		}
		return formDataObj;
	}

	handleInputChange = ({target}) => {
		const { value, name } = target;

		const formData = { ...this.state.formData };
		formData[name] = value;

		this.setState({
			formData
		});
	}
	
	formSubmit = (e) => {
		e.preventDefault();
		const errors = true;

		if (errors === true){
			if (this.state.isEditMode) {
				this.props.updateDBDetails(JSON.stringify(this.state.formData));
			} else {
				this.props.addDatabaseDetails(JSON.stringify(this.state.formData));
			}
		} else {
			this.setState({
				errors,
				formSubmitted: true
			});
		}
	};

	checkConnection = () => {
		const dbdata = this.state.formData;
		this.props.checkDbConnection(JSON.stringify({
			'db_type' : dbdata.db_type,
			'db_name' : dbdata.db_name,
			'db_hostname' : dbdata.db_hostname,
			'db_username' : dbdata.db_username,
			'db_password' : dbdata.db_password
		}));
	}

	formValidation = () => {
		return [
			this.state.formData.db_connection_name,
			this.state.formData.db_type,
			this.state.formData.db_name,
			this.state.formData.db_hostname,
			this.state.formData.db_username,
			this.state.formData.db_password,
		].every(Boolean);
	};

	render() {
		const inValid = !this.formValidation();
 		return (
			<div className="addDbDetailsForm">
				<Panel>
					<Panel.Heading className="editpanelhead">Add DB Details</Panel.Heading>
					<Panel.Body>
						<Form noValidate onSubmit={this.formSubmit} horizontal>
							<FormGroup controlId="formControlsConnName">
								<Col sm={4}><ControlLabel>Connection Name</ControlLabel></Col>
								<Col sm={8}><FormControl value={this.state.formData.db_connection_name} type="textbox" name="db_connection_name" onChange={this.handleInputChange} /></Col>
							</FormGroup >
							<FormGroup controlId="formControlsDbType">
								<Col sm={4}><ControlLabel>Database Type</ControlLabel></Col>
								<Col sm={8}><FormControl value={this.state.formData.db_type} type="textbox" name="db_type" onChange={this.handleInputChange} /></Col>
							</FormGroup >
							<FormGroup controlId="formControlsDbName">
								<Col sm={4}><ControlLabel>Database Name</ControlLabel></Col>
								<Col sm={8}><FormControl value={this.state.formData.db_name} type="textbox" name="db_name" onChange={this.handleInputChange} /></Col>
							</FormGroup >
							<FormGroup controlId="formControlsHostName">
								<Col sm={4}><ControlLabel>Host Name</ControlLabel></Col>
								<Col sm={8}><FormControl value={this.state.formData.db_hostname} type="textbox" name="db_hostname" onChange={this.handleInputChange} /></Col>
							</FormGroup >
							<FormGroup controlId="formControlsUsername">
								<Col sm={4}><ControlLabel>User Name</ControlLabel></Col>
								<Col sm={8}><FormControl value={this.state.formData.db_username} type="textbox" name="db_username" onChange={this.handleInputChange} /></Col>
							</FormGroup >
							<FormGroup controlId="formControlsPassword">
								<Col sm={4}><ControlLabel>Password</ControlLabel></Col>
								<Col sm={8}><FormControl value={this.state.formData.db_password} type="password" name="db_password" onChange={this.handleInputChange} /></Col>
							</FormGroup >

							<FormGroup className="formFooter">
								<Link to={'/view_db_details'} className="backbtn">
									<Button className="backbtnbackgroundcolor">Back</Button>
								</Link>
								<Button className="button-colors testconnbtn" type="button" onClick={(e) => {this.checkConnection()}} disabled={inValid} >Test Connection</Button>
								<Button className="button-colors submitbtn" type="submit" disabled={inValid} >Submit</Button>
							</FormGroup>
						</Form>
					</Panel.Body>
				</Panel>
			</div>
		);
	}
	
	componentWillUnmount() {
		console.log('ddDbdetails component unmounted');
		this.props.resetSelectedDbDetails();
	};
};


const mapStateToProps = (state) => {
	return {
		updatedDbDetails: state.dbDetailsData.updatedDbDetails,
		selectedDbDetails: state.dbDetailsData.selectedDbDetails,
		redirectToViewDBPage: state.dbDetailsData.redirectToViewDBPage,
		currentProject: state.appData.currentProject
	};
};

const mapDispatchToProps = dispatch => ({
	addDatabaseDetails: (data) => dispatch(addDatabaseDetails(data)),
	getDBDetailsById: (data) => dispatch(getDBDetailsById(data)),
	updateDBDetails: (data) => dispatch(updateDBDetails(data)),
	checkDbConnection: (data) => dispatch(checkDbConnection(data)),
	redirectToViewDbPageComplete: () => dispatch(redirectToViewDbPageComplete()),
	resetSelectedDbDetails: () => dispatch(resetSelectedDbDetails())
});

export default connect(mapStateToProps, mapDispatchToProps)(AddDbDetails);