import React, { Component } from 'react';
import { connect }from 'react-redux'
import { Row, Button, FormGroup, FormControl, ControlLabel, HelpBlock, Panel } from 'react-bootstrap';
import { changePassword } from '../actions/loginActions';

class ChangePasswordComponent extends Component {
	constructor(props) {
		super(props);
		this.state = {
			formData: {}, // Contains login form data
			errors: {}, // Contains login field errors
			formSubmitted: false, // Indicates submit status of login form 
			loading: false // Indicates in progress state of login form
		};
	}
  
	getConfirmtionMessage() {
		let element = null;
		if (this.props.changePassword) {
			element = (
				<div>Password Changed SuccessFully.</div>
			) 
		}
		return element;
	}

	handleInputChange = ({target}) => {
		const { value, name } = target;

		const { formData } = this.state;
		formData[name] = value;

		this.setState({
			formData
		});
	}

	submitNewPassWord = (e) => {
		e.preventDefault();
		let formData = this.state.formData;
		let formObj = {
			'old_password': formData.old_password,
			'new_password': formData.new_password
		};
		this.props.changePassword(JSON.stringify(formObj));
	};

	render() {
		const { errors, formSubmitted } = this.state;

		const goBack = () => {
			return <div>Hi there</div>
		};

		return(
			<div className="loginForm">
				<Panel className="passw_chng_panel_margin">
					<Panel.Heading className="chgpasswtable">Change Password</Panel.Heading>
					<Panel.Body>
						<form onSubmit={this.submitNewPassWord}>
							<FormGroup controlId="email" >
								<FormGroup controlId="password" validationState={ formSubmitted ? (errors.password ? 'error' : 'success') : null }>
									<FormControl type="password" name="old_password"  placeholder="Old Password" onChange={this.handleInputChange} />
									{ errors.password && 
										<HelpBlock>{errors.password}</HelpBlock> 
									}
								</FormGroup>

								<FormControl type="text" name="new_password" placeholder="New Password" onChange={this.handleInputChange} />
								{ errors.email && 
									<HelpBlock>{errors.email}</HelpBlock> 
								}
							</FormGroup >
							<FormGroup controlId="password">
								<FormControl type="password" name="confirm_password" placeholder="Confirm Password" onChange={this.handleInputChange} />
								{ errors.password && 
									<HelpBlock>{errors.password}</HelpBlock> 
								}
							</FormGroup>
							<Button type="submit" className="button-colors chngpasswbtn" bsStyle="primary">Submit</Button>
						</form>
					</Panel.Body>
				</Panel>
			</div>
		);
	}
}


const mapDispatchToProps = dispatch => ({
	changePassword: (data) => dispatch(changePassword(data))
})
  
export default connect(null, mapDispatchToProps)(ChangePasswordComponent);