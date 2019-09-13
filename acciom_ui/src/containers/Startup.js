import React from 'react';
import { connect  } from 'react-redux';
import { Button } from 'react-bootstrap';
import { showProjectSwitchPage } from '../actions/appActions';
import { getAllTestSuites } from '../actions/testSuiteListActions';
import TestSuiteList from './TestSuiteList';

class Startup extends React.Component {

	constructor(props) {
		super(props);
		if (this.props.currentProject) {
			this.props.getAllTestSuites(this.props.currentProject.project_id);
		}
	}
	// componentDidMount() {
	// }

	static getDerivedStateFromProps = (nextProps, prevState) => {
		if (nextProps.refreshTestSuites) {
			nextProps.getAllTestSuites(nextProps.currentProject.project_id);
		}
		return null;
	}

	render() {
		return (
			<div className='testSuiteList'>
				<div className='page-title'>
					<h2 className="main_titles dataprofilingtitle">Data Profiling</h2>
					<div className='project-switch'>
						<Button className="button-colors switchprojectbtn" bsStyle="primary" onClick={ (e) => this.props.showProjectSwitchPage(true)}>Switch Project</Button> 
					</div>
				</div>
				<TestSuiteList />
			</div>
		);
	 }
}

const mapStateToProps = (state) => {
	return {
		currentProject: state.appData.currentProject,
		refreshTestSuites: state.testSuites.refreshTestSuites
	};
};

const mapDispatchToProps = dispatch => ({
	getAllTestSuites: (data) => dispatch(getAllTestSuites(data)),
	showProjectSwitchPage: (data) => dispatch(showProjectSwitchPage(data))
})

export default connect(	mapStateToProps, mapDispatchToProps) (Startup);
