import React from 'react';
import { connect } from 'react-redux';
import { Modal, Button, FormGroup, ControlLabel, FormControl, Col } from 'react-bootstrap';
import { showOrgChangePage, updateSelectedOrganization, getProjectListByOrgId } from '../actions/appActions';

class ChangeOrganisation extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			selectedOrgId: ''
		};
	}

	componentDidMount() {
		this.setState({selectedOrgId: this.props.currentOrg.org_id});
	}

	render () {
		
		const renderOrgListOptions = () => {
			let options = null;
			options = this.props.orgList.map((org) => {
				return (<option value={org.org_id}>{org.org_name}</option>);
			});
			return options;
		};

		const handleShowOrg  = (isShow) => {
			this.props.showOrgChangePage(isShow);
		};
		
		const handleOrgChange = (e) => {
			this.setState({selectedOrgId: e.target.value});
		};

		const onChangeOrgSubmit = (e) => {
			e.preventDefault();
			// 
			let selectedOrg = null;
			for(let i = 0; i <  this.props.orgList.length; i += 1) {
				if(Number(this.props.orgList[i]['org_id']) === Number(this.state.selectedOrgId)) {
					selectedOrg = this.props.orgList[i];
					break;
				}
			}
			this.props.updateSelectedOrganization(selectedOrg);
			this.props.getProjectListByOrgId(selectedOrg.org_id);
		};

		return (
			<Modal id="orgChangeModal" show={this.props.isOrgChangePageVisible} 
				onHide={(event) => { handleShowOrg(false);}} container={this}
				aria-labelledby="contained-modal-title" bsSize="medium" className="switchprojectpopbox">

				<Modal.Header closeButton className="switchprojectpopboxheader">
					<Modal.Title id="contained-modal-title" className="sub_title">
						Change Organisation
					</Modal.Title>
				</Modal.Header>

				<Modal.Body>
					<form onSubmit={(e) => onChangeOrgSubmit(e)}> 
						<FormGroup controlId="organisation">
							<Col sm={6}><ControlLabel className="chnageorglabel label2">Select the organisation to be changed</ControlLabel></Col>
							<Col sm={6}>
								<FormControl componentClass="select" className="chngorgeditbox" placeholder="select" value={this.state.selectedOrgId} onChange = {(e) => handleOrgChange(e)}>
									{ renderOrgListOptions() }
								</FormControl>
							</Col>
						</FormGroup >
						<FormGroup controlId="submit" className="submitBtn">
							<Button type="submit" className="button-colors chngorgsavebtn">Save</Button>
						</FormGroup>
					</form>
				</Modal.Body>
			</Modal>
		);
	}
}

const mapStateToProps = (state) => {
	return {
		isOrgChangePageVisible: state.appData.isOrgChangePageVisible,
		orgList: state.appData.organizationList,
		currentOrg: state.appData.currentOrg
	};
};

const mapDispatchToProps = (dispatch) => {
	return {
		showOrgChangePage: (data) => dispatch(showOrgChangePage(data)),
		updateSelectedOrganization: (data) => dispatch(updateSelectedOrganization(data)),
		getProjectListByOrgId: (data) => dispatch(getProjectListByOrgId(data))
	}
};

export default connect(mapStateToProps, mapDispatchToProps) (ChangeOrganisation);