import React from 'react';
import { connect } from 'react-redux';
import { Modal, Button } from 'react-bootstrap';
import { Table, FormGroup, FormControl} from 'react-bootstrap';

import { 
	hideTestCaseDialog, 
	showTestCaseEditEnabled, 
	showTestCaseViewEnabled, 
	updateTestCase
} from '../actions/testSuiteListActions';

const styles = theme => ({
	root: {
		margin: 0,
		padding: theme.spacing(1),
		width: '600px',
	},
	closeButton: {
		position: 'absolute',
		right: theme.spacing(1),
		top: theme.spacing(1),
		color: theme.palette.grey[500],
		},
	textField: {
		marginLeft: theme.spacing(1),
		marginRight: theme.spacing(1),
		width: 200,
	},
	selectWidth: {width: 156},
});

class TestCaseDetails extends React.Component {

	constructor(props) {
		super(props);

		this.state = {
			formData: {}, // Contains login form data
			errors: {}, // Contains login field errors
			formSubmitted: false, // Indicates submit status of login form 
			loading: false // Indicates in progress state of login form
		};
	}

	handleInputChange = ({target}) => {
		const { value, name } = target;

		const { formData } = this.state;
		formData[name] = value;

		this.setState({
			formData
		});
	}

	handleCaseDialogBoxClose = () => {
		this.props.hideTestCaseDialog();
		this.props.showTestCaseViewEnabled();
	};

	handleTestCaseEditMode = () => {
		this.props.showTestCaseEditEnabled();
		
	};

	handleTestCaseViewMode = () => {
		this.props.showTestCaseViewEnabled();
	
	};

	getSnapshotBeforeUpdate = (prevProps, prevState) => {
		if (!prevProps.viewTestCase.showTestCaseDialog && this.props.viewTestCase.showTestCaseDialog) {
			this.setState({
				...this.state,
				formData: {
					...this.state.formData,
					testCaseId: this.props.viewTestCase.test_case_id,

					// check the below 2 props
					sourceConnection: this.props.viewTestCase.src_db_id,
					targetConnection: this.props.viewTestCase.target_db_id,

					sourceTable: this.props.viewTestCase.src_table,
					targetTable: this.props.viewTestCase.target_table,
					column: this.props.viewTestCase.column,
					sourceQuery: this.props.viewTestCase.sourceqry,
					targetQuery: this.props.viewTestCase.targetqry
				}
			})
			return this.props.viewTestCase.showTestCaseDialog;
		}
		return null;
	}

	renderConnectionsOptions = () => {
		return this.props.allConnections.map(connection => (
			connection ?
				<option key={connection.db_connection_id} value={connection.db_connection_id}>{connection.db_connection_name}</option> : null
		));
	}

	handleTestCaseUpdate = () => {
		const payload = {
			test_case_id: this.state.formData.testCaseId,
			src_table: this.state.formData.sourceTable,
			target_table: this.state.formData.targetTable,
			src_db_id: this.state.formData.sourceConnection,
			target_db_id: this.state.formData.targetConnection,
			src_qry: this.state.formData.sourceQuery,
			target_qry: this.state.formData.targetQuery,
			column: this.state.formData.column
		}
		this.props.updateTestCase(payload);
	}
	 handleCloseDialog = ()  => setShow(false)

	render() {
		return (
			<div>
				{ this.props.viewTestCase ?
					<Modal
						show={this.props.showTestCaseDialog}
						size="lg"
						aria-labelledby="contained-modal-title-vcenter"
						onHide={this.handleCaseDialogBoxClose}
						className="ModalMargin">
						<Modal.Header closeButton>
							<Modal.Title id="contained-modal-title-vcenter">
								<label className="testViewHeading">Case-Details:&nbsp;</label>
								<label className="testViewData">{this.props.viewTestCase.test_case_class}</label>
								{ this.props.showTestCaseEdit ? 
									<label onClick={this.handleTestCaseViewMode} className="viewEditLabel">
										<i className="fas fa-long-arrow-alt-left"></i>&nbsp;View Details </label> :
									<label onClick={this.handleTestCaseEditMode} className="viewEditLabel">Edit&nbsp;
										<i className="fas fa-pencil-alt"></i>
									</label>
								}
								{/* closeButton = {} */}
								
							</Modal.Title>
						</Modal.Header>
						<Modal.Body>
							{ this.props.showTestCaseEdit ?
								<form id="testEditMode">
									<Table id="editMode">
										<tbody>
											<tr>
												<td className="manageConnectionLabel"><label className="testViewDataLabel">Source Connection:</label></td>
												<td>
													<select className="form-control selectconnection"
														value={this.state.formData.sourceConnection}
														onChange={this.handleInputChange}
														name="sourceConnection"
													>
														{ this.renderConnectionsOptions() }
													</select>
												</td>
											</tr>
											<tr>
												<td className="manageConnectionLabel">
													<label className="testViewDataLabel">Target Connection:</label>
												</td>
												<td>
													<select className="form-control selectconnection"
														value={this.state.formData.targetConnection}
														onChange={this.handleInputChange}
														name="targetConnection"
													>
														{ this.renderConnectionsOptions() }
													</select>
												</td>
											</tr>
											<tr>
												<td className="manageConnectionLabel">
													<label className="testViewDataLabel">Source Table:</label>
												</td>
												<td>
													<FormGroup>
														<FormControl type="textbox" name="sourceTable"  value={this.state.formData.sourceTable} onChange={this.handleInputChange}/>
													</FormGroup>
												</td>
											</tr>
											<tr>
												<td className="manageConnectionLabel"><label className="testViewDataLabel">Target Table:</label></td>
												<td>
													<FormGroup>
														<FormControl type="textbox" name="targetTable" value={this.state.formData.targetTable} onChange={this.handleInputChange}/>
													</FormGroup>
												</td>
											</tr>
											
											<tr>
												<td className="manageConnectionLabel"><label className="testViewDataLabel">Column:</label></td>
												<td>
													<FormGroup>
														<FormControl type="textbox" name="column" value={this.state.formData.column} onChange={this.handleInputChange}/>
													</FormGroup>
												</td>
											</tr>

											<tr>
												<td className="manageConnectionLabel"><label className="testViewDataLabel">Source Query:</label></td>
												<td>
													<FormGroup>
														<textarea name="sourceQuery" value={this.state.formData.sourceQuery} onChange={this.handleInputChange}/>
													</FormGroup>
												</td>
											</tr>
											<tr>
												<td className="manageConnectionLabel"><label className="testViewDataLabel">Target Query:</label></td>
												<td>
													<FormGroup>
														<textarea name="targetQuery" value={this.state.formData.targetQuery} onChange={this.handleInputChange}/>
													</FormGroup>
												</td>
											</tr>
											<tr>
												<td className="manageConnectionLabel"></td>
												<td>
													<Button className="btn btn-primary viewUpdateBtn" onClick={e => this.handleTestCaseUpdate(e)}>
														Update
													</Button>
												</td>
											</tr>
										</tbody>
									</Table>
								</form>
								:  
								<Table className="manageConnection" id="viewMode">
									<tbody>
										<tr>
											<td className="manageConnectionLabel"><label className="testViewDataLabel">Source Connection:</label></td>
											<td>{this.props.viewTestCase.src_connection_name}</td>
										</tr>
										<tr>
											<td className="manageConnectionLabel"><label className="testViewDataLabel">Target Connection:</label></td>
											<td>{this.props.viewTestCase.target_connection_name}</td>
										</tr>
										<tr>
											<td className="manageConnectionLabel"><label className="testViewDataLabel">Source Table:</label></td>
											<td>{this.props.viewTestCase.src_table}</td>
										</tr>
										<tr>
											<td className="manageConnectionLabel"><label className="testViewDataLabel">Target Table:</label></td>
											<td>{this.props.viewTestCase.target_table}</td>
										</tr>
										<tr>
											<td className="manageConnectionLabel"><label className="testViewDataLabel">Column:</label></td>
											<td>{this.props.viewTestCase.column}</td>
										</tr>
										<tr>
											<td className="manageConnectionLabel"><label className="testViewDataLabel">Source Query:</label></td>
											<td>{this.props.viewTestCase.sourceqry}</td>
										</tr>
										<tr>
											<td className="manageConnectionLabel"><label className="testViewDataLabel">Target Query:</label></td>
											<td>{this.props.viewTestCase.targetqry}</td>
										</tr>
									</tbody>
								</Table>
							}
						</Modal.Body>
						<Modal.Footer>
						</Modal.Footer>
					</Modal> : null
				}
			</div>
		);
	}
}

const mapStateToProps = (state) => {
	return {
		showTestCaseDialog: state.testSuites.testCase.showTestCaseDialog,
		showTestCaseEdit:state.testSuites.showTestCaseEditEnabled,
		viewTestCase:state.testSuites.testCase,
		allConnections: state.testSuites.connectionsList && state.testSuites.connectionsList.allConnections? 
			state.testSuites.connectionsList.allConnections: []
	};
};

export default connect(mapStateToProps, {
	showTestCaseEditEnabled, 
	showTestCaseViewEnabled, 
	hideTestCaseDialog,
	updateTestCase,
})(TestCaseDetails);
