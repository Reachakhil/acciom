import React, { Component } from 'react';
import{ connect } from 'react-redux';
import {CopyToClipboard} from 'react-copy-to-clipboard';
import { Row, Button, FormGroup, FormControl, ControlLabel, HelpBlock, Panel } from 'react-bootstrap';
import { generateToken } from '../actions/loginActions';

class AuthToken extends Component{
	constructor(props){
		super(props);
		this.state = {
			isToken: false,
			value: '',
			copied: false,
		}
	}

	onGenerateButtonClick = (e) => {
		e.preventDefault();
		let accessTokenObj = {
			'message': 'this is for test'
		}
		this.setState({isToken : true});
		this.props.generateToken(JSON.stringify(accessTokenObj));
	}

	render(){
		return(
			<div className=''>
				<Panel>
					<Panel.Heading className="accesstknheader">
						<h5 className="msginline">Message</h5>
						<input className= "needTokeneditbox" placeholder="Why you need this Token ?"></input>
					</Panel.Heading >
					<Panel.Body className="panelheight"><h5>Personal Access Token</h5>
						<Button title="Click here for Generate Token" bsStyle="primary" className="gentokenButton button-colors" onClick={(e) => {this.onGenerateButtonClick(e)}}>Generate Token</Button>                  
					</Panel.Body>
					{this.state.isToken ? (
						<Panel.Body className="tokenpanelBackground">
							<div>Make sure to copy your new personal access token now. You won’t be able to see it again!</div><br></br>
							<input className="tokenField" value={this.props.accessToken} onChange={({target: {value}}) => this.setState({value, copied: false})} />
							<CopyToClipboard text={this.props.accessToken} onCopy={() =>this.setState({copied: true})}>
								<i class="fas fa-copy fa-lg clipboardOnhover"></i>
							</CopyToClipboard>
						</Panel.Body>
					) : null}
				</Panel>
			</div>
		);
	}
}

const mapStateToProps = (state) => {
	return {
		accessToken: state.loginData.accessToken
	};
};

const mapDispatchToProps = dispatch => ({
	generateToken: (data) => dispatch(generateToken(data))
})

// export default AuthToken;
export default connect(mapStateToProps, mapDispatchToProps)(AuthToken);