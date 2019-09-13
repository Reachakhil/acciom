import React, { useEffect } from 'react';
import { connect } from 'react-redux';
	
import { makeStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import { Table } from 'react-bootstrap';
import ManageConnection from '../components/ManageConnection';
import ViewLogs from '../components/ViewLogs';
import { renderStatusLabel, renderStatusIcon } from '../components/ViewLogDetails';
import ViewTestCase from '../components/ViewTestCase';

import { 
	getAllConnections, 
	getTestCaseByTestCaseId, 
	getTestCaseLogById, 
	executeTestBySuiteId, 
	executeTestByCaseId,
	getTestCaseDetailBySuiteId,
	getEachTestCaseDetailByCaseID
} from '../actions/testSuiteListActions';

import icon_new from '../assets/images/icon_new.jpg';
import { NEW, PASS, FAIL, ERROR, INPROGRESS, INPROGRESS_ID, PASS_ID, FAIL_ID, ERROR_ID, NEW_ID } from '../constants/common';

const useStyles = makeStyles(theme => ({
	root: {
		width: '100%',
	},
	heading: {
		fontSize: theme.typography.pxToRem(13),
		fontWeight: 'bold',
		flexBasis: '33.33%',
		flexShrink: 0,
	},
	secondaryHeading: {
		fontSize: theme.typography.pxToRem(13),
		flexBasis: '33.33%',
		color: theme.palette.text.secondary,
	},
	subHeading: {
		fontSize: theme.typography.pxToRem(13),
		fontWeight: 'bold',
		flexBasis: '40%',
		flexShrink: 0,
	},
	suiteID: {
		fontSize: theme.typography.pxToRem(13),
		fontWeight: 'bold',
		flexBasis: '18.33%',
		flexShrink: 0,
	},
	manageConnection: {
		fontSize: theme.typography.pxToRem(13),
		flexBasis: '23.33%',
		color: 'brown',
	},
	rcorners: {
		border: '2px solid',
		padding: '20px',
		width: '580px',
		borderRadius: '25px',
		boxShadow: '4px',
	},
	viewConnection: {
		fontSize: theme.typography.pxToRem(13),
		flexBasis: '18.33%',
		flexShrink: 0,
		color: 'brown',
	},
	status: {
		fontSize: theme.typography.pxToRem(13),
		flexBasis: '18.33%',
		flexShrink: 0,
		fontWeight: 'bold'
	},
	statusImg: {flexBasis: '20%'},
	noRecord: {color: 'red', textAlign: 'center'},
	innerPanelWidth: {width:'1080px'},
	statusBg: {
		fontSize: theme.typography.pxToRem(13),
		fontWeight: 'bold',
		flexBasis: '18.33%',
	},
	statusBgBlue: {
		fontSize: theme.typography.pxToRem(13),
		fontWeight: 'bold',
		flexBasis: '18.33%',
	},
	statusBgRed: {
		fontSize: theme.typography.pxToRem(13),
		fontWeight: 'bold',
		flexBasis: '18.33%',
	},
	statusBgOrange: {
		fontSize: theme.typography.pxToRem(13),
		fontWeight: 'bold',
		flexBasis: '18.33%',
	},
	executionWidth: {width: '20%'},
	caseLog: {cursor: 'pointer'},
}));

let refreshTimer;
let refreshTimerLogs;

function ControlledExpansionPanels({ testSuites, allCases, projectId, getAllConnections, getTestCaseDetailBySuiteId, getTestCaseLogById, 
	getTestCaseByTestCaseId, executeTestBySuiteId, executeTestByCaseId, showConnectionsDialog, getEachTestCaseDetailByCaseID,
	eachTestCaseDetails }) {
	let project_id;
	// console.log("project id==> ", projectId)
	if(projectId && projectId.appData && projectId.appData.currentProject) {
		project_id = projectId.appData.currentProject.project_id ? projectId.appData.currentProject.project_id : 2;
		console.log("projectId==>", project_id)
	}
	const classes = useStyles();
	const [expanded, setExpanded] = React.useState(false);
	const [testCaseExpanded, setTestCaseExpanded] = React.useState(false);
	const [testSuiteIdForManageConnections, setTestSuiteIdForManageConnections] = React.useState(null);

	useEffect(() => {
		// const project_Id = projectId.appData.currentProject.project_id; // remove this hardcoded assignment
		// console.log("project id==> ", projectId)
		getAllConnections(project_id);
		return function cleanup() {
			clearInterval(refreshTimer);
			clearInterval(refreshTimerLogs);
		};
	}, []);

	const handleChange = panel => (event, isExpanded) => {
		setExpanded(isExpanded ? panel : false);
		clearInterval(refreshTimer);
		clearInterval(refreshTimerLogs);
		if (isExpanded) {
			getTestCaseDetailBySuiteId(panel);
			refreshTimer = setInterval(() => { getTestCaseDetailBySuiteId(panel) }, 5000);
		}
	};
	const handleTestCaseChange = (suiteID, caseID) => (e, isExpanded) => {
		setTestCaseExpanded(isExpanded ? caseID : false);
		clearInterval(refreshTimerLogs);
		if (isExpanded) {
			console.log('Innn');
			getTestCaseDetailBySuiteId(suiteID);
			getEachTestCaseDetailByCaseID(caseID);
			refreshTimerLogs = setInterval(() => { getEachTestCaseDetailByCaseID(caseID) }, 5000);
		}
		e.stopPropagation();
	};

	const handleManageConnection = (e, suiteID) => {
		clearInterval(refreshTimer);
		setTestSuiteIdForManageConnections(suiteID);
		getTestCaseDetailBySuiteId(suiteID, true);
		getAllConnections(project_id);
		e.stopPropagation();
	};

	const viewTestCase = (e, caseID) => {
		getTestCaseByTestCaseId(caseID);
		getAllConnections(project_id);
		e.stopPropagation();
	};

	const viewTestCaseLogs = (testCaselogId, testCaseName) => {
		getTestCaseLogById(testCaselogId, testCaseName);
	};

	const renderTestName = (status) => {
		switch(status) {
		case INPROGRESS_ID:
		case INPROGRESS:
			return classes.statusBgOrange;
		case PASS_ID:
		case PASS:
			return classes.statusBg;
		case FAIL_ID:
		case FAIL:
			return classes.statusBgRed;
		case ERROR_ID:
		case ERROR:
			return classes.statusBgRed;
		case NEW_ID:
		case NEW:
			return classes.statusBgBlue;
		default:
			return '';
		}
	};

	const runTestSuite = (e, suiteID) => {
		e.stopPropagation();
		executeTestBySuiteId(suiteID);
		getTestCaseDetailBySuiteId(suiteID);
	};

	const runTestCase = (e, suiteID,caseID) => {
		e.stopPropagation();
		executeTestByCaseId([caseID]);
		getTestCaseDetailBySuiteId(suiteID);
		getEachTestCaseDetailByCaseID(caseID);
	};

	const onHover = (e) => {
		e.currentTarget.style.color = '#337ab7';
	};

	const onHout = (e) => {
		e.currentTarget.style.color = '';
	};

	const renderTestCasesPanels = (testSuite) => {
		if (!allCases[testSuite.test_suite_id]) return null;

		return allCases[testSuite.test_suite_id].map(testCaseList => (
			<ExpansionPanel key={testCaseList.case_id} expanded={testCaseExpanded === testCaseList.case_id} onChange={handleTestCaseChange(testSuite.test_suite_id, testCaseList.case_id)}>
				<ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
					<Typography className={classes.subHeading}>{testCaseList.case_name}</Typography>
					<Typography className={classes.viewConnection}><span  onMouseOver={e => onHover(e)} onMouseOut={e => onHout(e)} onClick={e => viewTestCase(e, testCaseList.case_id)}>View</span></Typography>
					<Typography className={classes.status}>Status&nbsp;&nbsp;&nbsp;{renderStatusIcon(testCaseList.test_status)}</Typography>
					<Typography className={renderTestName(testCaseList.test_status)}>{testCaseList.test_class_name}</Typography>
					<Typography><i className="far fa-play-circle statusPlayIcon" onMouseOver={e => onHover(e)} onMouseOut={e => onHout(e)} onClick={(e) => runTestCase(e, testSuite.test_suite_id, testCaseList.case_id)} aria-hidden="true"></i></Typography>
				</ExpansionPanelSummary>

				<ExpansionPanelDetails>
					<div>
						{ renderTestCaseLogDetails(testCaseList, testCaseList.case_id) }
					</div>
				</ExpansionPanelDetails>

			</ExpansionPanel>
		));
	};

	const renderTestCaseLogDetails = (testCaseList, caseID) => {
		if (!eachTestCaseDetails[caseID]) {
			return (
				<span className="red">Loading test case log...</span>
			); 
		} else if (eachTestCaseDetails[caseID].length === 0) {
			return (
				<span className="red">No Logs found.</span>
			);
		} else if (eachTestCaseDetails[caseID].length > 0) {
			return (
				<Table striped bordered hover size="sm" id="RoundedTable">
					<thead>
						<tr>
							<th className="testLogHeading">Execution Status</th>
							<th className="testLogHeading">Execution At</th>
							<th className="testLogHeading">Logs</th>	
						</tr>
					</thead>
					<tbody>
						{ eachTestCaseDetails[caseID] && eachTestCaseDetails[caseID].map(testCaseLog => (
							<tr key={testCaseLog.test_case_log_id}>
								<td className="testLogData">{renderStatusLabel(testCaseLog.test_execution_status)}</td>
								<td className="testLogData">{testCaseLog.executed_at}</td>
								{ (testCaseLog.test_execution_status != NEW_ID && testCaseLog.test_execution_status != INPROGRESS_ID) ?
									<td className={classes.caseLog} onClick={e => viewTestCaseLogs(testCaseLog.test_case_log_id, testCaseList.test_class_name)}>
										<i className="far fa-sticky-note logsIcon"></i>
									</td>
									: <td>---</td> }
							</tr>
						))}
					</tbody>
				</Table>
			);
		}
	};
	
	return (
		<div className={classes.root}>
			{ 
				(testSuites) ? testSuites.map(testSuite => (
					<ExpansionPanel className="panelbg" key={testSuite.test_suite_id} expanded={expanded === testSuite.test_suite_id} onChange={handleChange(testSuite.test_suite_id)}>
						
						<ExpansionPanelSummary
							expandIcon={<ExpandMoreIcon />}
							aria-controls="panel1bh-content"
							id="panel1bh-header">
							<Typography className={classes.heading}>{testSuite.test_suite_name}</Typography>
							<Typography className={classes.manageConnection}><span onMouseOver={e => onHover(e)} onMouseOut={e => onHout(e)} onClick={e => handleManageConnection(e, testSuite.test_suite_id)}>Manage Connections</span></Typography>
							<Typography className={classes.suiteID}>SuiteID: {testSuite.test_suite_id}</Typography>
							<Typography className={classes.secondaryHeading}>Uploaded at:  {testSuite.created_at}</Typography>
							<i className="far fa-play-circle statusPlayIcon" onMouseOver={e => onHover(e)} onMouseOut={e => onHout(e)} onClick={(e) => runTestSuite(e, testSuite.test_suite_id)} aria-hidden="true"></i>
						</ExpansionPanelSummary>

						<ExpansionPanelDetails className="backtablebg">
							<div className={classes.innerPanelWidth}>

								{ renderTestCasesPanels(testSuite) }
							
							</div>
						</ExpansionPanelDetails>

					</ExpansionPanel>
				)) : null
			}
			{ 
				showConnectionsDialog && testSuiteIdForManageConnections ?
					<ManageConnection testSuiteId={testSuiteIdForManageConnections}></ManageConnection>
					: null
			}
			<ViewTestCase></ViewTestCase>
			<ViewLogs></ViewLogs>
		</div>
	);
};

const mapStateToProps = (state) => {
	return {
		testSuites: state.testSuites.testSuiteList? state.testSuites.testSuiteList: [],
		showConnectionsDialog: state.testSuites.connectionsList.showConnectionsDialog,
		allCases: state.testSuites.connectionsList? state.testSuites.connectionsList.allCases: {},
		eachTestCaseDetails: state.testSuites.eachTestCaseDetails? state.testSuites.eachTestCaseDetails: [],
		projectId: state  
	};
};

export default connect(mapStateToProps, {
	getAllConnections, 
	getTestCaseLogById, 
	getTestCaseByTestCaseId, 
	executeTestBySuiteId, 
	executeTestByCaseId,
	getTestCaseDetailBySuiteId,
	getEachTestCaseDetailByCaseID
})(ControlledExpansionPanels);