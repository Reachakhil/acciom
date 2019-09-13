import React from 'react';
import { connect } from 'react-redux';
import { Modal, Button, FormGroup, ControlLabel, FormControl, Col } from 'react-bootstrap';
import { showProjectSwitchPage, updateSelectedProject } from '../actions/appActions';

class SwitchProject extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			selectedProjectId: ''
		};
	}

	componentDidMount() {
		this.setState({selectedProjectId: this.props.currentProject.project_id});
	}
	
	render () {
		
		const renderProjectListOptions = () => {
			let options = null;
			options = this.props.projectList.map((project) => {
				return (<option value={project.project_id}>{project.project_name}</option>);
			});
			return options;
		};

		const hidePopup  = () => {
			this.props.showProjectSwitchPage(false);
		};
		
		const handleProjectChange = (e) => {
			this.setState({selectedProjectId: e.target.value});
		};

		const onSubmit = (e) => {
			e.preventDefault();
			// 
			let selectedProject = null;
			const list = this.props.projectList;
			for(let i = 0; i < list.length; i += 1) {
				if(Number(list[i]['project_id']) === Number(this.state.selectedProjectId)) {
					selectedProject = list[i];
					break;
				}
			}
			this.props.updateSelectedProject(selectedProject);
		};

		return (

			<Modal id="orgChangeModal" show={this.props.isProjectSwitchPageVisible} 
				onHide={(event) => { hidePopup()}} container={this}
				aria-labelledby="contained-modal-title" bsSize="medium" className="switchprojectpopbox">

				<Modal.Header closeButton className="switchprojectpopbox switchprojectpopboxheader">
					<Modal.Title id="contained-modal-title" className="switchprojectpoptitle">
						Switch Project
					</Modal.Title>
				</Modal.Header>

				<Modal.Body>
					<form onSubmit={(e) => onSubmit(e)}> 
						<FormGroup controlId="project">
							<Col sm={6}><ControlLabel className="selectlabel">Select the new project: </ControlLabel></Col>
							<Col sm={6}>
								<FormControl componentClass="select" className="editbox" placeholder="select" value={this.state.selectedProjectId} onChange = {(e) => handleProjectChange(e)}>
									{ renderProjectListOptions() }
								</FormControl>
							</Col>
						</FormGroup >
						<FormGroup controlId="submit" className="submitBtn">
							<Button type="submit" className="button-colors savebtn">Save</Button>
						</FormGroup>
					</form>
				</Modal.Body>
			</Modal>

		);
	}
}

const mapStateToProps = (state) => {
	return {
		isProjectSwitchPageVisible: state.appData.isProjectSwitchPageVisible,
		projectList: state.appData.projectList,
		currentProject: state.appData.currentProject
	};
};

const mapDispatchToProps = (dispatch) => {
	return {
		showProjectSwitchPage: (data) => dispatch(showProjectSwitchPage(data)),
		updateSelectedProject: (data) => dispatch(updateSelectedProject(data)),
	}
};

export default connect(mapStateToProps, mapDispatchToProps) (SwitchProject);