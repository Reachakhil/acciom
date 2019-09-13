import React, { Component } from "react";
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { Panel, Table, Button, Modal} from 'react-bootstrap';

import { showProjectSwitchPage } from '../actions/appActions';
import { getAllDBDetails, deleteDBDetails } from '../actions/dbDetailsActions';
import EditIcon from '@material-ui/icons/Edit';
import DeleteIcon from '@material-ui/icons/Delete';
import '../css/Db-ui-styles.css';

class ViewDbDetails extends Component {

	constructor(props){
		super(props);
		this.state = {
			showDeleteConfirmationDialog: false,
			deleteConnectionID: null
		};
	}

	static getDerivedStateFromProps = (nextProps, prevState) => {
		if (nextProps.refreshDBDetails) {
			nextProps.getAllDBDetails(nextProps.currentProject.project_id);
		}
		return prevState;
	};

	handleSwitchProject = () => {
		this.props.showProjectSwitchPage(true);
	};

	deleteViewDBDetails = (deleteConnectionID) => {
		this.setState({showDeleteConfirmationDialog: true, deleteConnectionID}); 
	}

	onNoBtnClickHandler = () => {
		this.hideConfirmationopup();
	}

	onYesBtnClickHandler = () => {
		this.hideConfirmationopup();
		this.props.deleteDBDetails(this.state.deleteConnectionID);
	}

	hideConfirmationopup = () => {
		this.setState({showDeleteConfirmationDialog: false, deleteConnectionID: null})
	}

	renderDeleteConfirmationPopup = () => {
		return (
			<Modal show={true} className="deleteconfirmpopupbox" bsSize="small">
				<Modal.Header className="popboxheader">
					<Modal.Title className="sub_title">Confirmation</Modal.Title>
				</Modal.Header>

				<Modal.Body >
					<div className="deleteconfirmpopupfieldtext">Do You Want to Delete this DB ?</div>
				</Modal.Body>

				<Modal.Footer className="popboxfooter">
					<Button className="onDeleteDbYesBtnClick button-colors" bsStyle="primary" onClick={ (e) => {this.onYesBtnClickHandler()}}>Yes</Button>
					<Button className="onDeleteDbNoBtnClick nobtnbgcolor" onClick={ (e) => {this.onNoBtnClickHandler()}}>No</Button>
				</Modal.Footer>
			</Modal>
		)
		// this.props.deleteDBDetails(connectionID);
	}

	renderDBDetailsList = (dbDetailsList) => {
		return dbDetailsList.map((item, index) => {
			return (
				<tr key={index}>
					<td>{item.project_name}</td>
					<td>{item.db_connection_name}</td>
					<td>{item.db_type}</td>
					<td>{item.db_name}</td>
					<td>{item.db_hostname}</td>
					<td>{item.db_username}</td>
					<td>
						<Link to={`/add_db_details/${item.db_connection_id}`}>
							{/* <label className="addDBDetails">Edit</label> */}
							<EditIcon fontSize="small"  style={{color:"#696969"}} />
						</Link> &nbsp;
						{/*<label onClick={ (e) => {this.deleteViewDBDetails(item.db_connection_id)}} className="deleteDBDetails">Delete</label> */}
						<DeleteIcon fontSize="small" style={{color:"#696969"}} onClick={ (e) => {this.deleteViewDBDetails(item.db_connection_id)}} />
					</td>
				</tr>	
			);
		});
	};

	render() {
 		return (
			<div className="viewDbDetailsForm">
				<div className='btnContainer'>
				<i class="fa fa-database" id="db_icon" aria-hidden="true"></i>
				<label className="db_page_title main_titles">Manage Database Connections</label>
					<div className='project-switch'><Button className="button-colors" bsStyle="primary" onClick={ (e) => this.handleSwitchProject()}>Switch Project</Button> </div>
					<Link to={`/add_db_details`}>
						<Button className="button-colors addDbBtn" type="button" bsStyle="primary"> Add DB Details </Button>
					</Link>
				</div>
				<Table responsive className="manage-db-table">
					<thead className="table_head">
						<tr>
							<th>Project Name</th>
							<th>Connection Name</th>
							<th>Database Type</th>
							<th>Database Name</th>
							<th>Host Name</th>
							<th>User Name</th>
							<th>Actions</th>
						</tr>
					</thead>
					<tbody className="table_body">
						{ this.renderDBDetailsList(this.props.dbDetailsList) }
					</tbody>
				</Table>

				{ 
					this.state.showDeleteConfirmationDialog ?
						this.renderDeleteConfirmationPopup()
						: null
				}
			</div>
		);
	}
};

const mapStateToProps = (state) => {
	return {
		dbDetailsList: state.dbDetailsData.dbDetailsList?state.dbDetailsData.dbDetailsList: [],
		refreshDBDetails: state.dbDetailsData.refreshDBDetails,
		currentProject: state.appData.currentProject
	};
};

const mapDispatchToProps = dispatch => ({
	getAllDBDetails: (data) => dispatch(getAllDBDetails(data)),
	showProjectSwitchPage: (data) => dispatch(showProjectSwitchPage(data)),
	deleteDBDetails: (data) => dispatch(deleteDBDetails(data))
});

export default connect(mapStateToProps, mapDispatchToProps)(ViewDbDetails);