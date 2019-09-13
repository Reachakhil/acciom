import React from 'react';
import { connect } from 'react-redux';
import { Table } from 'react-bootstrap';

import { 
	ICON_STATUS_SUCCESS, 
	ICON_STATUS_FAIL, 
	ICON_STATUS_ERROR, 
	ICON_STATUS_INPROGRESS 
} from '../constants/icons';

import {
	COUNT_CHECK, NULL_CHECK, DUPLICATE_CHECK, DDL_CHECK, DATA_VALIDATION,
	NEW, PASS, FAIL, ERROR, INPROGRESS, INPROGRESS_ID, PASS_ID, FAIL_ID, ERROR_ID, NEW_ID
} from '../constants/common';

export const renderStatusLabel = (status) => {
	let labelColor = '';
	let  label = '';
	switch(status) {
	case INPROGRESS_ID:
	case INPROGRESS:
		labelColor = '#f3a563';
		label = 'In Progress';
		break;

	case PASS_ID:
	case PASS:	
		labelColor = 'green';
		label = 'Pass';
		break;

	case FAIL_ID:
	case FAIL:
		labelColor = 'red';
		label = 'Fail';
		break;

	case ERROR_ID:
	case ERROR:
		labelColor = 'red';
		label = 'Error';
		break;
	
	case NEW_ID:
	case NEW:
		labelColor = 'blue';
		label = 'New';
		break;

	default:
		break;
	}
	return <label style={{ color: labelColor }}>{label}</label>;
};

export const renderStatusIcon = (status) => {
	let iconClassName = '';
	switch(status) {
	case INPROGRESS:
	case INPROGRESS_ID:
		iconClassName = ICON_STATUS_INPROGRESS;
		break;
		// return <img alt={status} src={icon_new} />;

	case PASS:
	case PASS_ID:
		iconClassName = ICON_STATUS_SUCCESS;
		break;
	
	case FAIL:
	case FAIL_ID:
		iconClassName = ICON_STATUS_FAIL;
		break;

	case ERROR:
	case ERROR_ID:
		iconClassName = ICON_STATUS_ERROR;
		break;
	
	case NEW:
	case NEW_ID:
		return 'New';

	default:
	}

	return <i className={iconClassName} aria-hidden="true"></i>;
};

class CaseLogDetails extends React.Component {

	handleMessage = (status, name) => {
		let message = null;
		if (status === PASS) {
			if (name === COUNT_CHECK) {
				message = 'Source and Target Records Count Matches.';
			} else if (name === DUPLICATE_CHECK) {
				message = 'No Duplicate rows found in Target Table.';
			} else if (name === NULL_CHECK) {
				message = 'No Null values found in Target Table.';
			} else if (name === DDL_CHECK || name === DATA_VALIDATION) {
				message = 'Source and Target Schema are Same.';
			}
		} else {
			if (name === COUNT_CHECK) {
				message = 'Source and Target Records Count do not Match.';
			} else if (name === DUPLICATE_CHECK) {
				message = 'Duplicates Found.';
			} else if (name === NULL_CHECK) {
				message = 'Records found with Null value(s).';
			} else if (name === DDL_CHECK || name === DATA_VALIDATION) {
				message = "Source and Target Schema didn't Match.";
			}
		}
		return message;
	};

	render() {
		return (
			<div>
				{ this.props.testCaseName == 'countcheck' ?
					// CountCheck
					<Table id="viewLogDetails">
						<tbody>
							<tr>
								<td className="testCaseLogLabel">
									<label className="testViewDataLabel">{this.props.testCaseDisplayName} </label>
								</td>
							</tr>
							<tr>
								<td className="testCaseLogLabel">
									<label className="testViewDataLabel">Result: </label>&nbsp;&nbsp;
									<label className="resultLog">
										{renderStatusLabel(this.props.TestCaseLogDetails.Execution_status)}
									</label>&nbsp;&nbsp;
									{ renderStatusIcon(this.props.TestCaseLogDetails.Execution_status) }
								</td>
							</tr>
							<tr>
								<td className="testCaseLogMessage">
									<label className="testViewDataLabel">
										{this.handleMessage(this.props.TestCaseLogDetails.Execution_status, this.props.testCaseName)} 
									</label>
								</td>
							</tr>
							<tr>
								<Table striped bordered hover size="sm" className="executionLog">
									<tr>
										<td className="testCaseLogLabel">
											<label className="testViewDataLabel">Source Table Execution</label>
										</td>
										<td className="testCaseLogLabel">
											<label className="testViewDataLabel">Target Table Execution</label>
										</td>
									</tr>
									<tr>
										<td className="testCaseLogLabel">
											{ this.props.TestCaseLogDetails.Execution_log ?
												<label className="testViewExecution">{this.props.TestCaseLogDetails.Execution_log['source_execution_log']}</label>
												:
												null
											}
										</td>
										<td className="testCaseLogLabel">
											{ this.props.TestCaseLogDetails.Execution_log ?
												<label className="testViewExecution">{this.props.TestCaseLogDetails.Execution_log['dest_execution_log']}</label>
												:
												null
											}
										</td>
									</tr>
								</Table>
							</tr>
						</tbody>
					</Table>
					: 
					this.props.testCaseName == 'duplicatecheck' ?
						// DuplicateCheck
						<Table id="viewLogDetails">
							<tbody>
								<tr>
									<td className="testCaseLogLabel">
										<label className="testViewDataLabel">{this.props.testCaseDisplayName} </label>
									</td>
								</tr>
								<tr>
									<td className="testCaseLogLabel">
										<label className="testViewDataLabel">Result: </label> &nbsp;&nbsp;
										<label className="resultLog">
											{renderStatusLabel(this.props.TestCaseLogDetails.Execution_status)}
										</label>&nbsp;&nbsp;
										{ renderStatusIcon(this.props.TestCaseLogDetails.Execution_status) }
									</td>
								</tr>
								<tr>
									<td className="testCaseLogMessage">
										<label className="testViewDataLabel">
											{this.handleMessage(this.props.TestCaseLogDetails.Execution_status, this.props.testCaseName)} 
										</label>
									</td>
								</tr>
								{ this.props.TestCaseLogDetails.Execution_status !== 'pass' && this.props.TestCaseLogDetails.Execution_log && this.props.TestCaseLogDetails.Execution_log.hasOwnProperty('dest_execution_log') && this.props.TestCaseLogDetails.Execution_log['dest_execution_log'].length > 0 ?
								<tr>
									<Table className="executionLog">
										{
											this.props.TestCaseLogDetails.Execution_log['dest_execution_log'].map(log => (
											<tr>
												{log.map(details => (
													<td className="testCaseLogLabel">{details}</td>
												))}
											</tr>
											))											
										}
									</Table>
									</tr>
								: null }
							</tbody>
						</Table>

						// NullCheck
						: this.props.testCaseName == 'nullcheck' ?
						<Table id="viewLogDetails">
							<tbody>
								<tr>
									<td className="testCaseLogLabel">
										<label className="testViewDataLabel">{this.props.testCaseDisplayName} </label>
									</td>
								</tr>
								<tr>
									<td className="testCaseLogLabel">
										<label className="testViewDataLabel">Result: </label> &nbsp;&nbsp;
										<label className="resultLog">
											{renderStatusLabel(this.props.TestCaseLogDetails.Execution_status)}
										</label>&nbsp;&nbsp;
										{ renderStatusIcon(this.props.TestCaseLogDetails.Execution_status) }
									</td>
								</tr>
								<tr>
									<td className="testCaseLogMessage">
										<label className="testViewDataLabel">
											{this.handleMessage(this.props.TestCaseLogDetails.Execution_status, this.props.testCaseName)} 
										</label>
									</td>
								</tr>
								{this.props.TestCaseLogDetails.Execution_status !== 'pass' && this.props.TestCaseLogDetails.Execution_log && this.props.TestCaseLogDetails.Execution_log.hasOwnProperty('dest_log') && this.props.TestCaseLogDetails.Execution_log['dest_log'].length > 0 ?
								<tr>
									<Table className="executionLog">
									{this.props.TestCaseLogDetails.Execution_log['dest_log'].map(log => (
										<tr>
											{log.map(details => (
												<td className="testCaseLogLabel" nowrap>
													<label className="testViewDataLabel">{details === null ? 'null' : details}</label>
												</td>
											))}	
										</tr>
									))}
									</Table>
								</tr>
								: null }
							</tbody>
						</Table> : 

						// DDL Check
						this.props.testCaseName == 'ddlcheck' ?
						<Table id="viewLogDetails">
							<tbody>
								<tr>
									<td className="testCaseLogLabel">
										<label className="testViewDataLabel">{this.props.testCaseDisplayName} </label>
									</td>
								</tr>
								<tr>
									<td className="testCaseLogLabel">
										<label className="testViewDataLabel">Result: </label>&nbsp;&nbsp;
										<label className="resultLog">
											{renderStatusLabel(this.props.TestCaseLogDetails.Execution_status)}
										</label>&nbsp;&nbsp;
										{ renderStatusIcon(this.props.TestCaseLogDetails.Execution_status) }
									</td>
								</tr>
								<tr>
									<td className="testCaseLogMessage">
										<label className="testViewDataLabel">
											{this.handleMessage(this.props.TestCaseLogDetails.Execution_status, this.props.testCaseName)} 
										</label>
									</td>
								</tr>
								{ this.props.TestCaseLogDetails.Execution_status === 'fail' && this.props.TestCaseLogDetails.Execution_log && this.props.TestCaseLogDetails.Execution_log.hasOwnProperty('source_execution_log') && this.props.TestCaseLogDetails.Execution_log['source_execution_log'].length > 0 ?
								<td className="executionLog">
										{
											this.props.TestCaseLogDetails.Execution_log['source_execution_log'].map(log => (
											<tr>
												{log}
											</tr>
											))											
										}
									</td>
								: null }
								{ this.props.TestCaseLogDetails.Execution_status === 'fail' && this.props.TestCaseLogDetails.Execution_log && this.props.TestCaseLogDetails.Execution_log.hasOwnProperty('dest_execution_log') && this.props.TestCaseLogDetails.Execution_log['dest_execution_log'].length > 0 ?
								<td className="executionLog">
										{
											this.props.TestCaseLogDetails.Execution_log['dest_execution_log'].map(log => (
											<tr>
												{log}
											</tr>
											))											
										}
									</td>
								: null }
							</tbody>
						</Table>
						: this.props.testCaseName == 'datavalidation' ?
						// Datavalidation
						<Table id="viewLogDetails">
							<tbody>
								<tr>
									<td className="testCaseLogLabel">
										<label className="testViewDataLabel">{this.props.testCaseDisplayName} </label>
									</td>
								</tr>
								<tr>
									<td className="testCaseLogLabel">
										<label className="testViewDataLabel">Result: </label>&nbsp;&nbsp;
										<label className="resultLog">
											{renderStatusLabel(this.props.TestCaseLogDetails.Execution_status)}
										</label>&nbsp;&nbsp;
										{ renderStatusIcon(this.props.TestCaseLogDetails.Execution_status) }
									</td>
								</tr>
								<tr>
									<td className="testCaseLogMessage">
										<label className="testViewDataLabel">
											{this.handleMessage(this.props.TestCaseLogDetails.Execution_status, this.props.testCaseName)} 
										</label>
									</td>
								</tr>
								<tr>
									<td className="testCaseLogMessage">
										<label className="testViewDataLabel">
											Source Count : 
											{ this.props.TestCaseLogDetails.Execution_log ?
												<span className="red">{this.props.TestCaseLogDetails.Execution_log['src_count']}</span>
												: null
											} 
										</label>
									</td>
								</tr>
								<tr>
									<td className="testCaseLogMessage">
										<label className="testViewDataLabel">
											Target Count : 
											{ this.props.TestCaseLogDetails.Execution_log ?
												<span className="red">{this.props.TestCaseLogDetails.Execution_log['dest_count']}</span> 
												: null
											}
										</label>
									</td>
								</tr>
								{this.props.TestCaseLogDetails.Execution_log ?		
									<tr>
										<td className="testCaseLogMessage">
											<label className="testViewDataLabel">
												Number of Mismatch Records found in Source : <span className="red">{this.props.TestCaseLogDetails.Execution_log['src_to_dest_count']}</span> 
											</label>
										</td>
									</tr>
								 : null }
								 {this.props.TestCaseLogDetails.Execution_log ?	
									<tr>
										<td className="testCaseLogMessage">
											<label className="testViewDataLabel">
												Number of Mismatch Records found in Target : <span className="red">{this.props.TestCaseLogDetails.Execution_log['dest_to_src_count']}</span> 
											</label>
										</td>
									</tr>
								: null }
								{ this.props.TestCaseLogDetails.Execution_status === 'fail' && this.props.TestCaseLogDetails.Execution_log && this.props.TestCaseLogDetails.Execution_log.hasOwnProperty('source_execution_log') && this.props.TestCaseLogDetails.Execution_log['source_execution_log'] !== null && this.props.TestCaseLogDetails.Execution_log['source_execution_log'].length > 0 ?
								<td>
									<Table className="executionLog" style={{width:"50%"}}>
										{
											this.props.TestCaseLogDetails.Execution_log.source_execution_log.map(log => (
											<tr>
												{log.map(details => (
													<td className="testCaseLogLabel">{details}</td>
												))}
											</tr>
											))											
										}
									</Table>
								</td>
								: null }
								{ this.props.TestCaseLogDetails.Execution_status === 'fail' && this.props.TestCaseLogDetails.Execution_log && this.props.TestCaseLogDetails.Execution_log.hasOwnProperty('dest_execution_log') && this.props.TestCaseLogDetails.Execution_log['dest_execution_log'] !== null && this.props.TestCaseLogDetails.Execution_log['dest_execution_log'].length > 0 ?
								<td>
									<Table className="executionLog" style={{width:"50%"}}>
										{
											this.props.TestCaseLogDetails.Execution_log.dest_execution_log.map(log => (
											<tr>
												{log.map(details => (
													<td className="testCaseLogLabel">{details}</td>
												))}
											</tr>
											))											
										}
									</Table>
									</td>
								: null }	
							</tbody>
						</Table> 
						: 'No Logs Found!' }
				</div>
		);
	}
}

const mapStateToProps = (state) => {
	return {
		testCaseName: state.testSuites.testCaseLog.logData.test_case_class_name,
		testCaseDisplayName: state.testSuites.testCaseLog.logData.test_case_class_display_name,
		TestCaseLogDetails: state.testSuites.testCaseLog.logData 
	};
};

export default connect(mapStateToProps)(CaseLogDetails);